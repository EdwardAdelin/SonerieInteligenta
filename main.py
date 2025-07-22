import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
from tkinter import ttk
import json
import os
import threading
import time
import datetime
import pygame
import random
from pathlib import Path

class BellRingerApp:
    def __init__(self, root):
        self.root = root
        self.alarms = []
        self.system_running = False
        self.current_playing = None
        self.alarm_thread = None
        self.audio_files = []
        self.config_file = "alarms_config.json"
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load configuration
        self.load_alarms()
        self.load_audio_files()
        
        self.setup_ui()
        self.start_time_checker()
        
    def setup_ui(self):
        self.root.title("Sonerie Inteligenta")
        self.root.configure(bg="#1e1e2f")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#1e1e2f")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Sistem Sonerie Inteligenta",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="#1e1e2f"
        )
        title_label.pack(pady=(0, 30))
        
        # System status
        self.status_label = tk.Label(
            main_frame,
            text="Sistem OPRIT",
            font=("Helvetica", 16, "bold"),
            fg="#ff6b6b",
            bg="#1e1e2f"
        )
        self.status_label.pack(pady=(0, 20))
        
        # START-STOP button
        self.start_stop_button = tk.Button(
            main_frame,
            text="PORNIRE SISTEM",
            command=self.toggle_system,
            font=("Helvetica", 18, "bold"),
            bg="#51cf66",
            fg="white",
            activebackground="#69db7c",
            activeforeground="white",
            relief="flat",
            padx=30,
            pady=15,
            cursor="hand2"
        )
        self.start_stop_button.pack(pady=(0, 40))
        
        # Current time display
        self.time_label = tk.Label(
            main_frame,
            text="",
            font=("Helvetica", 16),
            fg="#74c0fc",
            bg="#1e1e2f"
        )
        self.time_label.pack(pady=(0, 20))
        self.update_time_display()
        
        # Alarms management section
        alarms_frame = tk.Frame(main_frame, bg="#1e1e2f")
        alarms_frame.pack(fill=tk.BOTH, expand=True)
        
        # Alarms title and buttons
        alarms_header = tk.Frame(alarms_frame, bg="#1e1e2f")
        alarms_header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            alarms_header,
            text="Intervale de Timp",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(side=tk.LEFT)
        
        buttons_frame = tk.Frame(alarms_header, bg="#1e1e2f")
        buttons_frame.pack(side=tk.RIGHT)
        
        tk.Button(
            buttons_frame,
            text="Adauga Interval",
            command=self.add_alarm,
            font=("Helvetica", 12, "bold"),
            bg="#3e8ed0",
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            buttons_frame,
            text="Sterge Selectat",
            command=self.delete_selected_alarm,
            font=("Helvetica", 12, "bold"),
            bg="#ff6b6b",
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(side=tk.LEFT)
        
        # Alarms list
        list_frame = tk.Frame(alarms_frame, bg="#2a2a3d", relief="ridge", bd=2)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable listbox
        self.alarms_listbox = tk.Listbox(
            list_frame,
            font=("Helvetica", 14),
            bg="#2a2a3d",
            fg="white",
            selectbackground="#3e8ed0",
            relief="flat",
            bd=0,
            height=10
        )
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.alarms_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.alarms_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.alarms_listbox.yview)
        
        # Update the alarms display
        self.refresh_alarms_display()
    
    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        half_width = screen_width // 2
        half_height = screen_height // 2
        x = (screen_width - half_width) // 2
        y = (screen_height - half_height) // 2
        self.root.geometry(f"{half_width}x{half_height}+{x}+{y}")
    
    def update_time_display(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        self.time_label.config(text=f"Ora curenta: {current_time}")
        self.root.after(1000, self.update_time_display)
    
    def toggle_system(self):
        if self.system_running:
            self.stop_system()
        else:
            self.start_system()
    
    def start_system(self):
        if not self.audio_files:
            messagebox.showwarning("Atentie", "Nu s-au gasit fisiere audio in directorul 'audio'. Adaugati fisiere mp3, wav sau ogg.")
            return
            
        self.system_running = True
        self.start_stop_button.config(
            text="OPRIRE SISTEM",
            bg="#ff6b6b",
            activebackground="#ff8787"
        )
        self.status_label.config(text="Sistem PORNIT", fg="#51cf66")
        print("Sistem pornit - monitorizare activa")
    
    def stop_system(self):
        self.system_running = False
        self.start_stop_button.config(
            text="PORNIRE SISTEM",
            bg="#51cf66",
            activebackground="#69db7c"
        )
        self.status_label.config(text="Sistem OPRIT", fg="#ff6b6b")
        
        # Stop any currently playing music
        if self.current_playing:
            pygame.mixer.music.stop()
            self.current_playing = None
        
        print("Sistem oprit")
    
    def add_alarm(self):
        dialog = AlarmDialog(self.root)
        if dialog.result:
            start_time, end_time = dialog.result
            alarm_str = f"{start_time} - {end_time}"
            self.alarms.append({
                'start_time': start_time,
                'end_time': end_time,
                'display': alarm_str
            })
            self.save_alarms()
            self.refresh_alarms_display()
    
    def delete_selected_alarm(self):
        selection = self.alarms_listbox.curselection()
        if selection:
            index = selection[0]
            del self.alarms[index]
            self.save_alarms()
            self.refresh_alarms_display()
        else:
            messagebox.showinfo("Info", "Selectati un interval pentru a-l sterge.")
    
    def refresh_alarms_display(self):
        self.alarms_listbox.delete(0, tk.END)
        for alarm in self.alarms:
            self.alarms_listbox.insert(tk.END, alarm['display'])
    
    def load_alarms(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.alarms = json.load(f)
        except Exception as e:
            print(f"Eroare la incarcarea configuratiei: {e}")
            self.alarms = []
    
    def save_alarms(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.alarms, f, indent=2)
        except Exception as e:
            print(f"Eroare la salvarea configuratiei: {e}")
    
    def load_audio_files(self):
        audio_dir = Path("audio")
        if audio_dir.exists():
            supported_formats = ['.mp3', '.wav', '.ogg']
            self.audio_files = [
                str(f) for f in audio_dir.iterdir() 
                if f.is_file() and f.suffix.lower() in supported_formats
            ]
        print(f"Fisiere audio gasite: {len(self.audio_files)}")
    
    def start_time_checker(self):
        def check_time():
            while True:
                if self.system_running:
                    current_time = datetime.datetime.now().strftime("%H:%M")
                    
                    for alarm in self.alarms:
                        start_time = alarm['start_time']
                        end_time = alarm['end_time']
                        
                        if current_time == start_time and not self.current_playing:
                            self.play_bell_music(start_time, end_time)
                        elif current_time == end_time and self.current_playing:
                            self.stop_bell_music()
                
                time.sleep(10)  # Check every 30 seconds
        
        self.alarm_thread = threading.Thread(target=check_time, daemon=True)
        self.alarm_thread.start()
    
    def play_bell_music(self, start_time, end_time):
        if not self.audio_files:
            return
        
        # Select random audio file
        audio_file = random.choice(self.audio_files)
        
        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play(0)  # Play once, don't loop
            self.current_playing = {
                'start': start_time, 
                'end': end_time, 
                'file': audio_file,
                'playlist': self.audio_files.copy()  # Copy of all available files
            }
            
            # Remove current song from playlist to avoid immediate repetition
            if audio_file in self.current_playing['playlist']:
                self.current_playing['playlist'].remove(audio_file)
            
            print(f"Inceput redare: {os.path.basename(audio_file)} pentru intervalul {start_time} - {end_time}")
            
            # Start monitoring for song end
            self.monitor_music_end()
            
        except Exception as e:
            print(f"Eroare la redarea audio: {e}")

    def monitor_music_end(self):
        """Monitor when current song ends and play next random song"""
        def check_music_status():
            while self.current_playing and self.system_running:
                # Check if music is still playing
                if not pygame.mixer.music.get_busy():
                    # Song ended, check if we're still in the break period
                    current_time = datetime.datetime.now().strftime("%H:%M")
                    end_time = self.current_playing['end']
                    
                    # If we haven't reached the end time yet, play another song
                    if current_time < end_time:
                        self.play_next_random_song()
                    else:
                        # Break period ended, stop playing
                        self.stop_bell_music()
                        break
                
                time.sleep(2)  # Check every 2 seconds
        
        # Start monitoring in a separate thread
        monitor_thread = threading.Thread(target=check_music_status, daemon=True)
        monitor_thread.start()

    def play_next_random_song(self):
        """Play next random song from the remaining playlist"""
        if not self.current_playing or not self.current_playing['playlist']:
            # If playlist is empty, refill it (excluding current song if possible)
            self.current_playing['playlist'] = self.audio_files.copy()
            current_file = self.current_playing['file']
            if len(self.current_playing['playlist']) > 1 and current_file in self.current_playing['playlist']:
                self.current_playing['playlist'].remove(current_file)
        
        # Select random song from remaining playlist
        if self.current_playing['playlist']:
            next_song = random.choice(self.current_playing['playlist'])
            self.current_playing['playlist'].remove(next_song)
            self.current_playing['file'] = next_song
            
            try:
                pygame.mixer.music.load(next_song)
                pygame.mixer.music.play(0)  # Play once
                print(f"Redare urmatoare: {os.path.basename(next_song)}")
            except Exception as e:
                print(f"Eroare la redarea urmatorului fisier audio: {e}")
                # Try to play another song if this one fails
                if self.current_playing['playlist']:
                    self.play_next_random_song()

    def stop_bell_music(self):
        if self.current_playing:
            pygame.mixer.music.stop()
            print(f"Oprire redare pentru intervalul {self.current_playing['start']} - {self.current_playing['end']}")
            self.current_playing = None

class AlarmDialog:
    def __init__(self, parent):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Adauga Interval de Timp")
        self.dialog.geometry("400x250")
        self.dialog.configure(bg="#1e1e2f")
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create form
        main_frame = tk.Frame(self.dialog, bg="#1e1e2f")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame,
            text="Adauga Interval de Sonat",
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(0, 20))
        
        # Start time
        tk.Label(
            main_frame,
            text="Ora de inceput (HH:MM):",
            font=("Helvetica", 12),
            fg="white",
            bg="#1e1e2f"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.start_time_entry = tk.Entry(
            main_frame,
            font=("Helvetica", 12),
            width=10
        )
        self.start_time_entry.pack(pady=(0, 15))
        
        # End time
        tk.Label(
            main_frame,
            text="Ora de sfarsit (HH:MM):",
            font=("Helvetica", 12),
            fg="white",
            bg="#1e1e2f"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.end_time_entry = tk.Entry(
            main_frame,
            font=("Helvetica", 12),
            width=10
        )
        self.end_time_entry.pack(pady=(0, 20))
        
        # Buttons
        buttons_frame = tk.Frame(main_frame, bg="#1e1e2f")
        buttons_frame.pack(fill=tk.X)
        
        tk.Button(
            buttons_frame,
            text="Anuleaza",
            command=self.cancel,
            font=("Helvetica", 12),
            bg="#6c757d",
            fg="white",
            relief="flat",
            padx=20,
            pady=10
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(
            buttons_frame,
            text="Adauga",
            command=self.ok,
            font=("Helvetica", 12),
            bg="#3e8ed0",
            fg="white",
            relief="flat",
            padx=20,
            pady=10
        ).pack(side=tk.RIGHT)
        
        # Focus on first entry
        self.start_time_entry.focus()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def validate_time(self, time_str):
        try:
            time.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
    
    def ok(self):
        start_time = self.start_time_entry.get().strip()
        end_time = self.end_time_entry.get().strip()
        
        if not self.validate_time(start_time) or not self.validate_time(end_time):
            messagebox.showerror("Eroare", "Format invalid de timp. Folositi formatul HH:MM (ex: 08:30)")
            return
        
        # Convert to datetime for comparison
        start_dt = datetime.datetime.strptime(start_time, "%H:%M")
        end_dt = datetime.datetime.strptime(end_time, "%H:%M")
        
        if start_dt >= end_dt:
            messagebox.showerror("Eroare", "Ora de sfarsit trebuie sa fie dupa ora de inceput.")
            return
        
        self.result = (start_time, end_time)
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BellRingerApp(root)
    root.mainloop()

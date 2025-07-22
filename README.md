# Sonerie Inteligenta - Smart Bell System

## Descriere
Acest sistem automat de sonerie este proiectat pentru școli, oferind posibilitatea programării intervalelor de timp pentru redarea muzicii.

## Funcționalități

### 🎵 Sistem de Redare Audio
- Redă muzică din folderul `audio/`
- Suportă formatele: MP3, WAV, OGG
- Selecție aleatorie a melodiilor
- Redare continuă pe timpul intervalului programat

### ⏰ Gestionare Intervale de Timp
- Adăugare intervale personalizate (HH:MM - HH:MM)
- Ștergere intervale selectate
- Salvare automată a configurației
- Încărcare automată la pornirea aplicației

### 🎮 Control Sistem
- Buton START/STOP pentru activarea/dezactivarea sistemului
- Status vizual al sistemului (PORNIT/OPRIT)
- Afișare ora curentă în timp real
- Mod fullscreen pentru afișare clară

## Utilizare

### Instalare
1. Activați mediul virtual:
   ```bash
   source env/bin/activate
   ```

2. Instalați dependințele (pygame este deja instalat):
   ```bash
   pip install pygame
   ```

### Adăugare Muzică
1. Creați folderul `audio/` în directorul principal
2. Adăugați fișiere audio (MP3, WAV, OGG) în acest folder
3. Aplicația va detecta automat fișierele

### Pornire Aplicație
```bash
python main.py
```

### Funcționare
1. **Pornire Sistem**: Apăsați butonul "PORNIRE SISTEM"
2. **Adăugare Interval**: Apăsați "Adauga Interval" și introduceți ora de început și sfârșit
3. **Ștergere Interval**: Selectați un interval din listă și apăsați "Sterge Selectat"
4. **Ieșire din Fullscreen**: Apăsați tasta ESC

### Exemple de Intervale
- `08:00 - 08:15` - Primul clopoțel
- `10:00 - 10:05` - Pauza mare
- `12:00 - 12:10` - Pauza de masă
- `14:00 - 14:05` - Sfârșitul programului

## Caracteristici Tehnice

### Verificare Timp
- Sistemul verifică timpul la fiecare 30 de secunde
- Comparația se face doar cu minutul (HH:MM)
- Redarea începe exact la ora programată

### Salvare Configurație
- Intervalele sunt salvate în `alarms_config.json`
- Încărcare automată la următoarea pornire
- Format JSON pentru ușurința editării manuale

### Audio
- Utilizează pygame pentru redare
- Redare în buclă pentru toată durata intervalului
- Oprire automată la sfârșitul intervalului

## Structura Proiectului
```
sonerie-app/
├── main.py                 # Aplicația principală
├── alarms_config.json      # Configurația salvată
├── audio/                  # Folderul cu muzică
│   ├── clopot1.mp3
│   ├── clopot2.wav
│   └── ...
├── env/                    # Mediul virtual Python
└── README.md              # Acest fișier
```

## Dependințe
- Python 3.12+
- tkinter (inclus în Python)
- pygame (pentru redare audio)
- json (inclus în Python)
- threading (inclus în Python)

## Note Importante
⚠️ **Adăugați fișiere audio în folderul `audio/` înainte de utilizare**

⚠️ **Sistemul trebuie să fie PORNIT pentru funcționarea automată**

⚠️ **Folosiți formatul HH:MM pentru orele de început și sfârșit**

## Suport
Pentru probleme sau întrebări, verificați consolele pentru mesajele de eroare și asigurați-vă că:
1. Pygame este instalat corect
2. Folderul audio conține fișiere valide
3. Formatele audio sunt suportate (MP3/WAV/OGG)

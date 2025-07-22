# Sonerie audio liceu

Acest fisier reprezinta instructiunile pentru soneria audio inteligenta. Programul a fost scris si proiectat pentru a functiona pe sisteme de operare Linux.

## Introducere pentru un utilizator nou

Inainte de a incerca sa folositi aplicatia, sigurati-va ca utilizati Python, versiunea Python 3.12.3. Pentru a verifica daca aveti Python instalat, deschideti aplicatia "Terminal" din Linux si introduceti urmatoarea comanda:

```bash
python --version
```

( puteti deschide "Terminal" inclusiv apasand simultan tastele CTRL + ALT + T )

## Informatii utile pentru programatori

Pentru programatori, in cazul modificarii aplicatiei, puteti realiza un VENV utilizand comanda in terminal:
```bash
python3 -m venv env
```

Activarea unui VENV se realizeaza prin comanda:
```bash
source env/bin/activate
```

## Necesare

Instaleaza pygame pentru audio:

```bash
pip install pygame
```

cd /home/pc/sonerie-app && source env/bin/activate && pip install pygame --upgrade

## License

[MIT](https://choosealicense.com/licenses/mit/)
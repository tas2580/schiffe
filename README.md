# Schiffe Versenken (Terminal, Python)

Ein kleines **Schiffe-Versenken-Spiel** für Linux ohne zusätzliche Abhängigkeiten.

## Voraussetzungen

- Python 3.10+ (meist schon auf Linux installiert)

## Start

```bash
python3 schiffe_versenken.py
```

## Steuerung

- Gib Koordinaten wie `A1`, `C5` oder `H8` ein.
- `X` = Treffer
- `o` = Fehlschuss
- `~` = unbekanntes Wasser

## Spielregeln (in dieser Version)

- Spielfeldgröße: 8x8
- Schiffe werden zufällig platziert.
- Schiffe berühren sich nicht, auch nicht diagonal.
- Du spielst gegen den Computer, der zufällig auf freie Felder schießt.

Viel Spaß!

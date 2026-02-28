# Schiffe Versenken (Linux, Python)

Jetzt in zwei Varianten:

1. **GUI-Version (empfohlen)** mit Tkinter (klickbar, farbig)
2. **Terminal-Version** ohne GUI

## Voraussetzungen

- Python 3.10+
- Für GUI: Tkinter (auf vielen Linux-Distributionen bereits enthalten, sonst Paket `python3-tk`)

## Start

### GUI (anständige Grafik)

```bash
python3 schiffe_versenken_gui.py
```

### Terminal

```bash
python3 schiffe_versenken.py
```

## Steuerung

### GUI

- Klicke auf ein Feld im gegnerischen Raster, um zu schießen.
- Farben zeigen Treffer, Fehlschüsse und eigene Schiffe.
- Button **„Neues Spiel“** startet direkt neu.

### Terminal

- Gib Koordinaten wie `A1`, `C5` oder `H8` ein.
- `X` = Treffer
- `o` = Fehlschuss
- `~` = unbekanntes Wasser

## Spielregeln

- Spielfeldgröße: 8x8
- Flotte: `4, 3, 3, 2, 2, 2`
- Schiffe werden zufällig platziert.
- Schiffe berühren sich nicht, auch nicht diagonal.
- Du spielst gegen den Computer.

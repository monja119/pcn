# Détermination du PCN d'une chaussée souple (Tkinter)

Ce projet propose une application simple en Python pour calculer le **PCN** d'une chaussée souple, à partir de :

- `e` : épaisseur de la chaussée
- `CBR` : valeur CBR
- `H(CBR)` : donnée principale d'entrée

Le calcul suit la logique :

- `PCN = H(CBR) × RSI`
- `RSI = (e² / 1000) × (6.12 / D)`
- `D = 4.231 - 5.013·log10(CBR/0.6) + 2.426·(log10(CBR/0.6))² - 0.473·(log10(CBR/0.6))³`

## Architecture

Structure orientée **Clean Architecture** :

- `domain` : règles métier pures (formules et validations)
- `application` : cas d'usage (orchestration)
- `presentation` : interface Tkinter

## Lancement

Depuis la racine du projet :

```bash
python3 main.py
```

## Notes

- Aucune dépendance externe n'est nécessaire (utilise seulement la bibliothèque standard).
- `CBR` doit être strictement positif.
- Le dénominateur `D` ne doit pas être nul.

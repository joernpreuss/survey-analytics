# Survey Analytics Dashboard

Streamlit-Dashboard zur Analyse von Kundenzufriedenheit in der Luftfahrt. Basiert auf dem [Airline Passenger Satisfaction](https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction) Datensatz von Kaggle (~130.000 Befragte).

## Features

- **Zufriedenheitsübersicht** — KPI-Karten, Balkendiagramme nach Klasse/Reisegrund/Kundentyp, interaktive Filter
- **Treiberanalyse** _(noch nicht implementiert)_ — Logistische Regression auf 14 Zufriedenheitsdimensionen, Importance-Performance-Matrix
- **Segmentierung** _(noch nicht implementiert)_ — K-Means-Clustering mit Radardiagrammen und Segmentprofilen

## Setup

```bash
uv run streamlit run app/dashboard.py
```

Datensatz (`data/survey.csv`) ist im Repo enthalten — Kaggle train.csv und test.csv zusammengeführt, Index- und id-Spalten entfernt.

## Stack

- Python 3.13
- Streamlit, Pandas, Plotly
- statsmodels (Treiberanalyse), scikit-learn (Segmentierung)

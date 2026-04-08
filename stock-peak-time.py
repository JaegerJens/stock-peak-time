import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

def analysiere_aktien_metrik(ticker_symbol):
    # 1. Daten herunterladen (letzte 5 Jahre für den Kontext)
    df = yf.download(ticker_symbol, period="5y", multi_level_index=False)
    if df.empty: return "Keine Daten gefunden."

    # 2. Aktuellen Kurs und Allzeithoch (ATH) ermitteln
    aktueller_kurs = float(df['Close'].iloc[-1])
    ath_datum = df['Close'].idxmax()
    ath_kurs = df['Close'].max()

    # 3. Den Punkt VOR dem ATH suchen, der dem aktuellen Kurs entspricht
    vor_peak_df = df.loc[:ath_datum]
    # Finde den Index mit der geringsten Differenz zum heutigen Preis
    paritaet_index = (vor_peak_df['Close'] - aktueller_kurs).abs().idxmin()
    paritaet_datum = paritaet_index.date()

    # 4. Zeitdifferenz berechnen
    heute_datum = df.index[-1].date()
    zeit_differenz = (heute_datum - paritaet_datum).days

    # 5. Visualisierung
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Aktienkurs', color='blue', alpha=0.5)
    
    # Markierungen
    plt.scatter(paritaet_index, aktueller_kurs, color='green', label=f'Paritätspunkt ({paritaet_datum})', zorder=5)
    plt.scatter(ath_datum, ath_kurs, color='red', label=f'Höchstpunkt ({ath_datum.date()})', zorder=5)
    plt.scatter(df.index[-1], aktueller_kurs, color='orange', label=f'Aktuell ({heute_datum})', zorder=5)

    # Verbindungslinie (die Zeitdifferenz)
    plt.hlines(y=aktueller_kurs, xmin=paritaet_index, xmax=df.index[-1], color='black', linestyle='--')
    plt.text(paritaet_index, aktueller_kurs * 1.05, f' {zeit_differenz} Tage Differenz', fontweight='bold')

    plt.title(f'Symmetrie-Metrik für {ticker_symbol}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    return zeit_differenz

# Beispielaufruf für eine Aktie (z.B. Microsoft)
tage = analysiere_aktien_metrik("MSFT")
print(f"Die Zeitdifferenz beträgt {tage} Tage.")

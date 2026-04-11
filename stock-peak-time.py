import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use('QtAgg')

def analysiere_aktien_metrik(ticker_symbol):
    # 1. Daten herunterladen (letzte 5 Jahre für den Kontext)
    df = yf.download(ticker_symbol, period="5y", multi_level_index=False)
    if df.empty: return "Keine Daten gefunden."

    # 2. Aktuellen Kurs und Allzeithoch (ATH) ermitteln
    aktueller_kurs = float(df['Close'].iloc[-1])
    ath_datum = df['Close'].idxmax()
    ath_kurs = df['Close'].max()

    # Kursverlust zum ATH berechnen
    verlust_prozent = ((ath_kurs - aktueller_kurs) / ath_kurs) * 100

    # 3. Den Punkt VOR dem ATH suchen, der dem aktuellen Kurs entspricht (innerhalb des Tagesbereichs Low-High)
    vor_peak_df = df.loc[:ath_datum]
    # Finde Tage, wo der aktuelle Kurs zwischen Low und High liegt
    mask = (vor_peak_df['Low'] <= aktueller_kurs) & (vor_peak_df['High'] >= aktueller_kurs)
    if mask.any():
        # Wähle den Punkt, der am nächsten zum ATH ist (der letzte in der gefilterten Liste)
        paritaet_index = vor_peak_df[mask].index[-1]
    else:
        # Fallback: Verwende den Index mit der geringsten Differenz zum Close (wie vorher)
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
    plt.text(paritaet_index, aktueller_kurs * 0.95, f' {zeit_differenz} Tage Differenz', fontweight='bold')

    # Senkrechte durch ATH bis zur Verbindungslinie
    plt.vlines(x=ath_datum, ymin=aktueller_kurs, ymax=ath_kurs, color='purple', linestyle='--', label='ATH zu aktueller Kurs')
    plt.text(ath_datum, ath_kurs, f' {verlust_prozent:.2f}% Verlust', fontweight='bold', ha='left', va='center')

    plt.title(f'Symmetrie-Metrik für {ticker_symbol}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    return zeit_differenz, verlust_prozent

# Beispielaufruf für eine Aktie (z.B. Microsoft)
tage, verlust = analysiere_aktien_metrik("MSFT")
print(f"Die Zeitdifferenz beträgt {tage} Tage.")
print(f"Der aktuelle Kursverlust zum ATH beträgt {verlust:.2f}%.")

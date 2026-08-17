import time
import requests
import serial
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ===== CONFIGURAZIONE SPOTIFY =====
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://127.0.0.1:8888/callback"

SCOPE = "user-read-currently-playing user-read-playback-state"

# ===== CONFIGURAZIONE AWS API =====
API_URL = "https://jao66nq5bb.execute-api.eu-west-1.amazonaws.com/countartist"

# ===== CONFIGURAZIONE ARDUINO =====
PORTA_ARDUINO = "COM3"
BAUDRATE = 9600

# ===== CONFIGURAZIONE LOOP =====
INTERVALLO_CONTROLLO = 5
GIORNI_STATISTICA = 30

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))


def apri_connessione_arduino():
    arduino = serial.Serial(PORTA_ARDUINO, BAUDRATE, timeout=1)
    time.sleep(2)
    return arduino


def leggi_canzone_corrente():
    current_track = sp.current_user_playing_track()

    if current_track is not None and current_track["is_playing"]:
        track_id = current_track["item"]["id"]
        canzone = current_track["item"]["name"]
        artista = current_track["item"]["artists"][0]["name"]

        return {
            "track_id": track_id,
            "canzone": canzone,
            "artista": artista
        }

    return None


def invia_ascolto_ad_aws(canzone, artista, giorni=30):
    response = requests.post(
        API_URL,
        json={
            "canzone": canzone,
            "artista": artista,
            "giorni": giorni
        },
        timeout=10
    )

    response.raise_for_status()
    return response.json()


def aggiorna_statistiche(canzone, artista):
    risultato = invia_ascolto_ad_aws(
        canzone=canzone,
        artista=artista,
        giorni=GIORNI_STATISTICA
    )

    return {
        "canzone": risultato["canzone"],
        "artista": risultato["artista"],
        "conteggio": risultato["conteggio"],
        "giorni": risultato["giorni"]
    }


def prepara_messaggio_arduino(dati_display):
    canzone = pulisci_testo(dati_display["canzone"])
    artista = pulisci_testo(dati_display["artista"])
    conteggio = str(dati_display["conteggio"])

    return f"{canzone}|{artista}|{conteggio}\n"


def pulisci_testo(testo):
    testo = testo.replace("|", "-")
    testo = testo.replace("\n", " ")
    testo = testo.replace("\r", " ")
    return testo


def invia_ad_arduino(arduino, dati_display):
    messaggio = prepara_messaggio_arduino(dati_display)
    arduino.write(messaggio.encode("utf-8"))
    print("Messaggio inviato:")
    print(messaggio)


def stampa_dati_display(dati_display):
    print(f"In riproduzione: {dati_display['canzone']}")
    print(f"Artista: {dati_display['artista']}")
    print(f"Ascolti ultimi {dati_display['giorni']} giorni: {dati_display['conteggio']}")
    print("-" * 50)


def ciclo_principale():
    ultimo_track_id = None
    arduino = None

    try:
        arduino = apri_connessione_arduino()

        print("Avvio monitoraggio Spotify...")
        print("Premi CTRL+C per fermare il programma.")
        print("-" * 50)

        while True:
            traccia_corrente = leggi_canzone_corrente()

            if traccia_corrente is None:
                print("Nessuna canzone in riproduzione.")
                ultimo_track_id = None
                time.sleep(INTERVALLO_CONTROLLO)
                continue

            track_id = traccia_corrente["track_id"]
            canzone = traccia_corrente["canzone"]
            artista = traccia_corrente["artista"]

            if track_id != ultimo_track_id:
                print(f"Nuova canzone rilevata: {canzone} - {artista}")

                try:
                    dati_display = aggiorna_statistiche(canzone, artista)
                    stampa_dati_display(dati_display)
                    invia_ad_arduino(arduino, dati_display)

                    ultimo_track_id = track_id

                except requests.exceptions.RequestException as errore:
                    print("Errore durante la chiamata all'API AWS.")
                    print(f"Dettaglio: {errore}")
                    print("-" * 50)

                except KeyError:
                    print("Risposta API ricevuta, ma formato non valido.")
                    print("-" * 50)

                except serial.SerialException as errore:
                    print("Errore durante l'invio dati ad Arduino.")
                    print(f"Dettaglio: {errore}")
                    print("-" * 50)

            else:
                print(f"Stessa canzone ancora in riproduzione: {canzone} - {artista}")

            time.sleep(INTERVALLO_CONTROLLO)

    except KeyboardInterrupt:
        print("Programma fermato dall'utente.")

    finally:
        if arduino is not None and arduino.is_open:
            arduino.close()
            print("Connessione Arduino chiusa.")


if __name__ == "__main__":
    ciclo_principale()
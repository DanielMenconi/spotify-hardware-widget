import pymysql

HOST = "spotifydb.c9m886auylqh.eu-west-1.rds.amazonaws.com"
PORT = 3306
USER = "admin"
PASSWORD = "h8kBVMYpchFN8Bm"
DATABASE = "spotify_stats"

def conta_ascolti_artista(artista, giorni=30):
    connessione = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = connessione.cursor()
    cursor.execute(
        """
        SELECT COUNT(*) FROM ascolti
        WHERE artista = %s
        AND data_ora >= DATE_SUB(NOW(), INTERVAL %s DAY)
        """,
        (artista, giorni)
    )
    risultato = cursor.fetchone()
    connessione.close()
    return risultato[0]

def salva_ascolto(canzone, artista):
    connessione = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = connessione.cursor()
    cursor.execute(
        "INSERT INTO ascolti (canzone, artista) VALUES (%s, %s)",
        (canzone, artista)
    )
    connessione.commit()
    connessione.close()
    print(f"Salvato nel database cloud: {canzone} - {artista}")

if __name__ == "__main__":
    conteggio = conta_ascolti_artista("The Weeknd")
    print(f"Hai ascoltato The Weeknd {conteggio} volte negli ultimi 30 giorni!")
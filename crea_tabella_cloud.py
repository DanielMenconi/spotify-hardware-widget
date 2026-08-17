import pymysql

HOST = "spotifydb.c9m886auylqh.eu-west-1.rds.amazonaws.com"
PORT = 3306
USER = "admin"
PASSWORD = "h8kBVMYpchFN8Bm"  
DATABASE = "spotifydb"            

try:
    print("Connessione al database...")
    connessione = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD
    )
    cursor = connessione.cursor()

    # 1. Creiamo (se non esiste) il database e lo selezioniamo
    cursor.execute("CREATE DATABASE IF NOT EXISTS spotify_stats")
    cursor.execute("USE spotify_stats")

    # 2. Creiamo la tabella "ascolti" (sintassi MySQL)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ascolti (
            id INT PRIMARY KEY AUTO_INCREMENT,
            canzone VARCHAR(255) NOT NULL,
            artista VARCHAR(255) NOT NULL,
            data_ora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connessione.commit()
    print("Tabella 'ascolti' creata con successo nel cloud!")

    connessione.close()

except Exception as errore:
    print("ERRORE.")
    print(f"Dettaglio: {errore}")
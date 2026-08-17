import sqlite3

def crea_database():
    # Connessione al database (se il file non esiste, lo crea!)
    conn = sqlite3.connect('spotify_stats.db')
    cursor = conn.cursor()
    
    # Creiamo la tabella "ascolti"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ascolti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            canzone TEXT NOT NULL,
            artista TEXT NOT NULL,
            data_ora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database creato con successo!")

if __name__ == "__main__":
    crea_database()
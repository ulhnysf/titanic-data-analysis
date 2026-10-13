import sqlite3


conn = sqlite3.connect('titanicdeneme.db')  # 'titanicdeneme.db' adında bir veritabanı dosyası oluşturduk.

# Veritabanı bağlantısını kapattık.
conn.close()

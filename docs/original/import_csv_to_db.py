import sqlite3
import pandas as pd

# CSV dosyasının tam yolu
csv_file_path = r'tested.csv'  

# CSV dosyasını pandas ile okuduk.
df = pd.read_csv(csv_file_path)


conn = sqlite3.connect('titanicdeneme.db')  # 'titanicdeneme.db' adında bir SQLite veritabanı dosyasına bağlandım.
cursor = conn.cursor()

# Veritabanında tablo oluştururuz (eğer tablo yoksa)
df.to_sql('tested', conn, if_exists='replace', index=False)  # 'tested' adında bir tablo oluşturdum.

# Değişiklikleri kaydettim.
conn.commit()

# Bağlantıyı kapattım
conn.close()


"""Depodaki doğrulanmış CSV'den yerel SQLite veritabanını oluşturur."""
from data_access import DB_PATH, DataValidationError, build_database

if __name__ == '__main__':
    try:
        print(f'{build_database()} kayıt aktarıldı: {DB_PATH}')
    except (DataValidationError, OSError) as exc:
        raise SystemExit(f'Veri aktarımı başarısız: {exc}') from exc

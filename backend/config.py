DB_USER = "root"
DB_PASSWORD = "123456"
DB_HOST = "localhost"
DB_NAME = "warehouse_db"

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
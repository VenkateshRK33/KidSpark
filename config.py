class Config:
    SECRET_KEY = 'kidspark_super_secret_2024'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123venkatesh'
    MYSQL_DB = 'kidspark_db'
    MYSQL_CURSORCLASS = 'DictCursor'
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 2592000  # 30 days in seconds (only if remember me is checked)

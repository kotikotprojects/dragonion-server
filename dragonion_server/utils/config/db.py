import sqlitedict


class ConfigDatabase(sqlitedict.SqliteDict):
    def __init__(self, tablename):
        super().__init__(
            filename='data.storage',
            tablename=tablename,
            autocommit=True
        )


config = ConfigDatabase('config')
services = ConfigDatabase('services')

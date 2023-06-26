import sqlitedict


class AuthFile(sqlitedict.SqliteDict):
    def __init__(self, service):
        super().__init__(
            filename=f'{service}.auth',
            tablename='auth',
            autocommit=True
        )

class DBIntegrityException(Exception):
    pass


class DBDataException(Exception):
    pass


class DBUserExists(Exception):
    pass


class DBUserNotExists(Exception):
    pass

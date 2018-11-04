NONE = ''

INT = 'INT'
INTEGER = 'INTEGER'
TINYINT = 'TINYINT'
SMALLINT = 'SMALLINT'
MEDIUMINT = 'MEDIUMINT'
BIGINT = 'BIGINT'
UNSIGNED_BIG_INT = 'UNISGNED BIG INT'
INT2 = 'INT2'
INT8 = 'INT8'


def CHARACTER(length):
    return 'CHARACTER({length})'.format(length=length)


def VARCHAR(length):
    return 'VARCHAR({length})'.format(length=length)


def VARYING_CHARACTER(length):
    return 'VARYING CHARACTER({length})'.format(length=length)


def NCHAR(length):
    return 'NCHAR({length})'.format(length=length)


def NATIVE_CHARACTER(length):
    return 'NATIVE CHARACTER({length})'.format(length=length)


def NVCHAR(length):
    return 'NVCHAR({length})'.format(length=length)


TEXT = 'TEXT'
CLOB = 'CLOB'

BLOB = 'BLOB'

REAL = 'REAL'
DOUBLE = 'DOUBLE'
DOUBLE_PRECISION = 'DOUBLE_PRECISION'
FLOAT = 'FLOAT'

NUMERIC = 'NUMERIC'


def DECIMAL(x, y):
    return 'DECIMAL({x}, {y})'.format(x=x, y=y)


BOOLEAN = 'BOOLEAN'
DATE = 'DATE'
DATETIME = 'DATETIME'

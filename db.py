import bull

DATABASE_NAME = 'a'
LOG_TABLE = 'log'

bull.Database.connect(DATABASE_NAME).execute('CREATE TABLE IF NOT EXISTS log(id INT PRIMARY KEY, number CHAR(10), transcription TEXT, datetime TEXT, sentiment, DECIMAL)')

def new_log(caller, transcription, datetime, sentiment):
    db = bull.Database.connect(DATABASE_NAME)

    db.insert(LOG_TABLE, {
        'number': caller[2:],
        'transcription': transcription,
        'datetime': datetime,
        'sentiment': sentiment})

def get_logs():
    db = bull.Database.connect(DATABASE_NAME)

    return db.select(LOG_TABLE, '*')

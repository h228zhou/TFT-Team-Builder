import sqlite3

conn = sqlite3.connect('tft.db')
c = conn.cursor()

# Create Champions table
c.execute('''
    CREATE TABLE champion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cost INTEGER
    )
''')

# Create Traits table
c.execute(
    '''
    CREATE TABLE trait (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        synergy TEXT
    )
    '''
)

# Create the Chapmion_trait junction table
c.execute(
    '''
    CREATE TABLE champion_trait (
        champion_id INTEGER,
        trait_id INTEGER,
        PRIMARY KEY (champion_id, trait_id),
        FOREIGN KEY (champion_id) REFERENCES champion(id),
        FOREIGN KEY (trait_id) REFERENCES trait(id)
    )
    '''
)

# Create augments table
c.execute(
    '''
    CREATE TABLE augment (
        augment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        tactics_id TEXT NOT NULL
    )
    '''
)

conn.commit()

conn.close()
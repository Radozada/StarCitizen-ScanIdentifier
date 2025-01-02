import sqlite3

# Step 1: Connect to a new SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('data/scsi_database.db')  # 'scsi_database.db' is the database file name

# Step 2: Create a cursor object to interact with the database
cursor = conn.cursor()

# Step 3: Create a table (if it doesn't already exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT
    )
''')

# Step 4: Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully!")

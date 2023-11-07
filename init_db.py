import sqlite3

conn = sqlite3.connect('Blog.db')

cursor = conn.cursor()

cursor.execute('''
PRAGMA foreign_keys = ON;
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Article (
                  article_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title VARCHAR(256),
                  slug VARCHAR(256),
                  content TEXT,
                  author VARCHAR(64)
               );
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Comment(
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(256),
    content TEXT,
    article_id INTEGER,
    FOREIGN KEY (article_id)
        REFERENCES Article (article_id)
);
''')

conn.commit()
conn.close()

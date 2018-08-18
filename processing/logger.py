import sqlite3
from os.path import join, dirname, realpath

PATH = join(dirname(realpath(__file__)), '../logs.db')

database = sqlite3.connect(PATH, check_same_thread=False)
cursor = database.cursor()

cursor.execute("SELECT name from sqlite_master WHERE type='table' AND name='logs'")
		
if cursor.fetchone() == None:
	cursor.execute('''CREATE TABLE logs (username, hard text, simple text, time, stats, current time)''')

def log(username, hard_text, simple_text, time, stats, current_time):
	cursor.execute('INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)', (username, hard_text, simple_text, time, stats, current_time))
	database.commit()

def fetch(username):
	cursor.execute('SELECT * FROM logs WHERE username=?', (username,))
	return cursor.fetchall()
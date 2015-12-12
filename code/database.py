import sqlite3


def create_tables(conn):
	c = conn.cursor()
	c.execute('''CREATE TABLE if not exists docs
				(id text primary key, labels text, term_freq text, tfidf text)''')
	c.execute('''CREATE TABLE if not exists labels (id text primary key, docs text, centroid text)''')
	c.execute('''CREATE TABLE if not exists terms (id text primary key, docs text, idf real)''')
	conn.commit()

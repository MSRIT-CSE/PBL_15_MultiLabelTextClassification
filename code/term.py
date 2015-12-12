import sqlite3
from collections import defaultdict
import math


# term1 -> doc1, doc2, ... docn
def write_terms_to_db(conn):
	terms = defaultdict(list)
	c = conn.cursor()
	print "Creating term index now. [term1] -> [doc1, doc2, ... docn]"
	for doc in c.execute("SELECT * FROM docs"):
		doc_id = doc[0]
		freq_info = doc[2].split()
		for each_item in freq_info:
			term_id = each_item.split(":")[0]
			terms[term_id] = doc_id

	print "Terms created. Writing to db now."

	for term, docs in terms.iteritems():
		docs_text = ""
		for each_doc in docs:
			docs_text += each_doc
		docs_text = docs_text[:-1]
		c.execute("INSERT INTO terms VALUES ('%s','%s', -1)" % (term, docs_text))
	conn.commit()
	print "Terms successfully written to db"


def compute_idf(conn):
	BETA = 5.0
	idfs = defaultdict(float)
	c = conn.cursor()
	print "Starting to compute IDF for each term"
	# Counting the total number of documents in the db
	c.execute('''SELECT COUNT(*) FROM docs''')
	N = int(c.fetchone()[0])

	for term in c.execute("SELECT * FROM terms"):
		term_id = term[0]
		docs = term[1]
		count = len(docs)
		idf = BETA + math.log(N / (count + 1))
		idfs[term_id] = idf
	print "Computation of IDFs done"
	return idfs


def write_idf_to_db(idfs, conn):
	print "Starting to write terms to db"
	c = conn.cursor()
	for term, idf in idfs.iteritems():
		c.execute("UPDATE terms SET idf = '%f' WHERE id = '%s'" % (idf, term))
	conn.commit()
	print "IDF values successfully written to db [terms table]"


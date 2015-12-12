import math
import sqlite3
import time
import csv


class Document:
	id = -1
	labels = []			# This document belongs to these labels			
	term_freq = {}
	tfidf = {}

	def __init__(self, id, labels, term_freq):
		self.id = id
		self.term_freq = term_freq
		self.labels = labels


def write_docs_to_db(path_to_csv, conn):
	print "Fetching docs line by line and writing to db ..."
	c = conn.cursor()
	i = 0
	start_time = time.clock()
	with open(path_to_csv, 'rb') as csv_file:
		csv_reader = csv.reader(csv_file)
		for row in csv_reader:
			labels_text = ""
			term_freq_text = ""
			for val in row:
				if ":" in val:
					for subval in val.split():		# term-id:term-frequency
						if ":" in subval:
							term_freq_text += subval + " "
						else:
							labels_text += subval.strip() + " "

				else:
					labels_text += val.strip() + " "

			if i % 100000 == 0:
				print str(i) + " documents written to db"

			# Removing the extra space at the end
			labels_text = labels_text[:-1]
			term_freq_text = term_freq_text[:-1]
			c.execute("INSERT INTO docs VALUES ('%s','%s','%s','%s')" % (str(i), labels_text, term_freq_text, ""))
			i += 1
	end_time = time.clock()
	print "Writing documents to DB took " + str(end_time - start_time) + " seconds"
	conn.commit()


# Returns tfidf[doc_id] = "term1:tfidf1 term2:tfidf2 ..."
def compute_tfidf(conn):
	tfidf_vectors = {}
	c = conn.cursor()
	print "Starting to compute TFIDF values. [for each term in each doc]"
	i = 0
	c.execute("SELECT * FROM docs")
	for doc in c.fetchall():
		doc_id = doc[0]
		tfidf_text = ""
		term_freqs_info = doc[2].split()
		for item in term_freqs_info:
			term_id = item.split(":")[0]
			freq = int(item.split(":")[1])
			c.execute("SELECT idf from terms where id = '%s'" % (term_id))
			idf = float(c.fetchone()[0])
			tfidf = math.log(freq + 1) * idf
			tfidf_text += term_id + ":" + str(tfidf) + " "
		tfidf_text = tfidf_text[:-1]
		tfidf_vectors[doc_id] = tfidf_text
		i += 1

		# Debug statement
		if i % 25000 == 0:
			print "Tfidf vectors computed for " + str(i) + " documents"
	print "Computation of TFIDF done"
	return tfidf_vectors


def write_tfidf_vectors_to_db(tfidf_vectors, conn):
	c = conn.cursor()
	print "Writing TFIDF values to db. [docs table]"
	i = 0
	for doc_id, tfidf_vector in tfidf_vectors.iteritems():
		c.execute("UPDATE docs SET tfidf = '%s' WHERE id = '%s'" % (tfidf_vector,doc_id))
		
		i += 1
		# Debug statement
		if i % 25000 == 0:
			print "Tfidf vectors updated in DB for " + str(i) + " documents"
	conn.commit()
	print "TFIDF values successfully written to db"






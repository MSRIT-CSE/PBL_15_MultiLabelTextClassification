import sqlite3
import sys
import document, label, term
import database


# Give path to CSV file as argument
if __name__ == "__main__":
	conn = sqlite3.connect('docs.db')
	database.create_tables(conn)
	path_to_csv = sys.argv[1]

	# Fetch details of all documents and write to db
	document.write_docs_to_db(path_to_csv, conn)

	# Read from db and create a label index
	label.write_labels_to_db(conn)

	# Fetch terms from 'docs' table and create a 'terms' table
	term.write_terms_to_db(conn)

	# compute idf and write them to 'terms' table
	idfs = term.compute_idf(conn)
	term.write_idf_to_db(idfs, conn)

	# compute tfidf for each term in each document and write to 'docs' table
	tfidf_vectors = document.compute_tfidf(conn)
	document.write_tfidf_vectors_to_db(tfidf_vectors, conn)

	# Compute and write centroids of labels to db
	label.write_label_centroids(conn)

	conn.close()
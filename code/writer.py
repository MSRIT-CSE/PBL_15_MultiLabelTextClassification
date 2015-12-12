
def write_centroids(centroids):
	f = open("centroids", "w")
	for label, vector in centroids.iteritems():
		f.write(str(label) + " ")
		for term, val in vector.iteritems():
			f.write(str(term) + ":" + str(val) + " ")
		f.write("\n")
	f.close()

def write_tfidf(documents):
	f = open("tfidf", "w")
	for each_doc in documents:
		f.write(each_doc.id + " ")
		for each_term, tf in each_doc.term_freq.iteritems():
			each_doc.tfidf[each_term] = math.log(tf + 1) * idfs[each_term]
			f.write(str(each_term) + ":" + str(each_doc.tfidf[each_term]) + " ")
		f.write("\n")
	f.close()


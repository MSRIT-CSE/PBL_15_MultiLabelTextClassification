
def get_centroids(label_index, doc_tfidf):
	centroid_collection = {}
	for label_id, docs in label_index.iteritems():
		centroid = {}
		for doc_id in docs:
			size = len(docs)
			for term, tfidf in doc_tfidf[int(doc_id)].iteritems():
				if term in centroid.keys():
					centroid[term] += float(tfidf)/size
				else:
					centroid[term] = float(tfidf)/size
		centroid_collection[label_id] = centroid
	return centroid_collection
import pycuda.autoinit
import pycuda.driver as drv
import numpy, csv, operator
import rocchio

from pycuda.compiler import SourceModule
mod = SourceModule("""
	__global__ void find_distance(float dist, float *a, float *b, int n)
{
  int k=0;
  const int i = threadIdx.x;
  dist=0.0;
  for (k=0; k<n; k++) 
  	dist += (a-b)*(a-b);
}
""")

find_distance = mod.get_function("find_distance")

n=1250000
path_to_csv = sys.argv[1]
with open(path_to_csv, 'rb') as csv_file:
	csv_reader = csv.reader(csv_file)
	for row in csv_reader:
		a=[0]*n
		b=[0]*n
		distances=[]	
		doc_id=row[0]
		terms=[x.split(':') for x in row[1].split()]
		for term in terms:
			term_id=int(term[0])
			tf=int(term[1])
			a[term_id]=tf
			a=numpy.array(a)
			## GET CENTROID DICT - b should be initialized here -- FOR LOOP STARTS 
			find_distance(drv.Out(dist), drv.In(a), drv.In(b), drv.In(n),block=(400,1,1), grid=(1,1))
			distances['centroid_id']=dist #centroid_id is not known
		sorted_d = sorted(distances.items(), key=operator.itemgetter(1))
		print 'Document ' + doc_id + ' is classified into: '
		for x in xrange (0,3):
			print "Category ID: " + str(sorted_d[x][0]) + '(distance: ' + str(sorted_d[x][1]) + ')'
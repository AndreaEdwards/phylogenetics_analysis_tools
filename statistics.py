from scipy import stats
import util
import cPickle as pickle

def LoadPkl(file_name):
	print "Loading %s..." % file_name
	open_file = open(file_name, 'rb')
	output_dictionary = pickle.load(open_file)
	open_file.close()
	print "Length of %s dictionary: %d" % (file_name, len(output_dictionary))
	return output_dictionary

def FilterByShapiroWilk(dictionary):
	filtered_dictionary = {}
	for key in dictionary:
		result = stats.shapiro(dictionary[key])
		if float(result[1]) > 0.001:
			filtered_dictionary[key] = dictionary[key]
	print "The distribution of distances of all pairs were tested for normality using a Shapiro-Wilk test"
	print "The organism pair dictionary has been filtered based on distributions that tested positive for normality"
	print "The resulting dictionary has a length of: %d" % len(filtered_dictionary)
	return filtered_dictionary
		
def main():
	dist_dictionary = LoadPkl('filtered_dist_dictionary.pkl')
	filtered_by_shapiro = FilterByShapiroWilk(dist_dictionary)

main()
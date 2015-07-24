import os
import subprocess
import cPickle as pickle
import itertools
import numpy
from util import FileHandlers

class PickleFasta:
	def __init__(self):
		self.file_handlers = FileHandlers()

	def _get_fasta_files(self):
		file_paths = self.file_handlers.search_directory()
		fasta_files = self.file_handlers.find_files(file_paths, 'faa')
		print "There are %d .faa files in this directory" % len(fasta_files)
		return fasta_files

	def pickle_organism_fasta(self):
		fasta_files = self._get_fasta_files()
		fasta_dictionary = {}
		for fasta_file in fasta_files:
			file_name = self.file_handlers.get_file_name(fasta_file)
			name_list = file_name.split('.')
			Data = open(fasta_file)
			D = Data.readlines()
			Data.close()
			for d in D:
				if d.startswith('>'):
					d_list = d.split(' ')
					if name_list[0] in fasta_dictionary:
						fasta_dictionary[name_list[0]].append(d_list[0].lstrip('>'))
					else:
						fasta_dictionary[name_list[0]] = [d_list[0].lstrip('>')]
				else:
					pass
		return fasta_dictionary

def get_dm_files():
	file_handlers = FileHandlers()
	file_paths = file_handlers.search_directory()
	dm_files = file_handlers.find_files(file_paths, 'dm')
	return dm_files


class dmDictionary:
	def __init__(self):
		self.mapping_dictionary = {}
		self.distance_dictionary = {}
		self.organism_pairs = {}

	def individual_dm_dictionary(self, distance_file, file_name):
		dm_dictionary = {}
		data = open(distance_file)
		D = data.readlines()
		data.close()
		for d in D:
			d = d.strip().split(' ')
			key = str(d[0]) + ' : ' + str(d[1])
			dm_dictionary[key] = d[-1]
		return dm_dictionary
	
	def init_mapping_dictionary(self, fasta_dictionary):
		for keyA in fasta_dictionary:
			self.mapping_dictionary[keyA] = []

	def build_mapping_dictionary(self, fasta_dictionary, dm_dictionary):
		for key in dm_dictionary:
			enzymes = key.split(' : ')
			enz1 = enzymes[0]
			enz2 = enzymes[1]
			for key in fasta_dictionary:
				if enz1 in fasta_dictionary[key]:
					self.mapping_dictionary[key].append(enz1)
					print "Found %s in %s" % (enz1, key)
					print "Updated mapping_dictionary for %s", key
					print self.mapping_dictionary[key]
				else:
					pass
				if enz2 in fasta_dictionary[key]:
					self.mapping_dictionary[key].append(enz2)
					print "Found %s in %s" % (enz2, key)
					print "Updated mapping_dictionary for %s", key
					print self.mapping_dictionary[key]
				else:
					pass
		return self.mapping_dictionary

		#enzyme_dictionary = {}
		#for keyB in dm_dictionary:
		#	enzymes = keyB.split(' : ')
		#	enzyme_dictionary[enzymes[0]] = 0
		#for keyC in enzyme_dictionary:
		#	for keyA in fasta_dictionary:
		#		if keyC in fasta_dictionary[keyA]:
		#			self.mapping_dictionary[keyA].append(keyA + "_" + keyC)
		#return self.mapping_dictionary


	def generate_combinations(self, iterable):
		pairs = itertools.combinations(iterable, 2)
		for pair in pairs:
			self.organism_pairs[pair] = []
		return self.organism_pairs



def build_distance_dict(dm_files, inverse_mapping_dict, organism_pairs):
	file_handlers = FileHandlers()
	for dm_file in dm_files:
		file_name = file_handlers.get_file_name(dm_file)
		print "Opening %s...." % file_name
		data = open(dm_file)
		D = data.readlines()
		data.close()
		for d in D:
			data = d.strip().split(' ')
			enz1 = data[0]
			enz2 = data[1]
			distance = data[-1]
			for key in organism_pairs:
				if enz1 in inverse_mapping_dict and enz2 in inverse_mapping_dict:
					if inverse_mapping_dict[enz1] in key and inverse_mapping_dict[enz2] in key:
						#print inverse_mapping_dict[enz1], inverse_mapping_dict[enz2], key
						organism_pairs[key].append(distance)
						#print organism_pairs[key]
						#print "Length of distance list is %d" % len(organism_pairs[key])
				else:
					print "Could not find %s and %s in mapping_dict" % (enz1, enz2)
		print "Finished parsing %s...." % file_name
	return organism_pairs


def compute_average_distance(distance_dict):
	average_distances = {}
	for key in distance_dict:
		average_distances[key] = numpy.mean(distance_dict[key])
	return average_distances





def main():
	## THIS WORKED, DON'T ERASE
	## Save organism data to pickled dictionary
	#pickle_fasta = PickleFasta()
	#fasta_dictionary = pickle_fasta.pickle_organism_fasta()
	#print "There are %d entries in the fasta_dictionary" % len(fasta_dictionary)
	#pickle.dump(fasta_dictionary, open('organism_dictionary.pkl', 'wb'))
	
	file_handlers = FileHandlers()
	dm_files = get_dm_files()

	# Load the dictionary back from the pickle file
	print "Loading fasta_dictionary..."
	open_fasta = open('organism_dictionary.pkl', 'rb')
	fasta_dictionary = pickle.load(open_fasta)
	open_fasta.close()
	print "Length of fasta dictionary: ", len(fasta_dictionary)

	## THIS WORKED, DON'T ERASE
	## Build mapping dictionary and pickle
	dm_processing = dmDictionary()
	dm_processing.init_mapping_dictionary(fasta_dictionary)
	for path in dm_files:
		file_name = file_handlers.get_file_name(path)
		print "Opening %s..." % file_name
		dm_dictionary = dm_processing.individual_dm_dictionary(path, file_name)
		print "Length of dm_dictionary for %s is %d" % (file_name, len(dm_dictionary))
		mapping_dictionary = dm_processing.build_mapping_dictionary(fasta_dictionary, dm_dictionary)
	
	open_mapping = open('mapping_dictionary.pkl', 'wb')
	pickle.dump(mapping_dictionary, open_mapping)
	open_mapping.close()
	print mapping_dictionary
#
#	print "Opening mapping_dictionary...."
#	open_mapping = open('mapping_dictionary.pkl', 'rb')
#	mapping_dict = pickle.load(open_mapping)
#	open_mapping.close()
#
#	print "Opening inverse mapping dictionary......"
#	open_inverse_mapping = open('inverse_mapping_dictionary.pkl', 'rb')
#	inverse_mapping_dict = pickle.load(open_inverse_mapping)
#	open_inverse_mapping.close()
#
#	dm_files = get_dm_files()
#
#	organism_pairs = dm_processing.generate_combinations(mapping_dict)
#
#	distance_dict = build_distance_dict(dm_files, inverse_mapping_dict, organism_pairs)
#
#	avg_dist_dict = compute_average_distance(distance_dict)
#
#	open_avg_dist = open('avg_dist_dictionary.pkl', 'wb')
#	pickle.dump(avg_dist_dict, open_avg_dist)
#	open_avg_dist.close()
#
#	print avg_dist_dict

	





main()
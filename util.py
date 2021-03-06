"""
I/O utils (:mod:`skeng.io.util`)
================================

.. currentmodule:: skeng.io.util

This module provides utility functions to deal with files and I/O in
general.

Functions
---------

class FileHandlers
	methods = [
		search_directory,
		find_files,
		filter_files,
		clean,
		build_dict]
	
"""
import os

class FileHandlers:
	def __init__(self):
		self.directory = os.getcwd()
		self.file_paths = []
		self.new_file_list = []
		self.cleaned = []
		self.filtered_list = []


	def search_directory(self):
		"""Search current working directory for files
		
		Useful for finding all files in the current directory of a particular 
		type

		Parameters
		----------
		none

		Returns
		-------
		list
			List of strings. Each string is the root path to each file in the 
			current working directory 

    	Examples
    	--------
    	>>> file_handlers = FileHandlers()
    	>>> file_paths = file_handlers.search_directory()
    	>>> print file_paths
	
		"""
		for root, self.directory, file_list in os.walk(self.directory):
			for file_name in file_list:
				path = root + os.sep + file_name
				self.file_paths.append(path)
		return self.file_paths


	def find_files(self, file_list, extension):
		"""Find all files with a specified extension (.txt, .png, .py, etc)

		Useful for getting particular files before parsing

		Parameters
		----------
		file_list: list
			List of strings to loop through. Each string corresponds to a file
			path.
		extension: string
			String corresponding to the file extension to search for.

		Returns
		-------
		list
			List of strings. Each string is the root path to each file within
			the current working directory that also contains the specified
			file extension. 

		Examples
		--------
		>>> file_handlers = FileHandlers()
    	>>> file_paths = file_handlers.search_directory()
    	>>> fasta_files = file_handlers.find_files(file_paths, 'fasta')
    	>>> print fasta_files
		"""
		self.new_file_list = []
		for file_path in file_list:
			new_list = file_path.split('.')
			if new_list[-1] == extension:
				self.new_file_list.append(file_path)
			else:
				pass
		return self.new_file_list

	def get_file_name(self, file_path):
		"""Retrieve the file name from a sting corresponding to the file path

		Useful for printing out file names

		Parameters
		----------
		file_path: string
			String corresponds to a file

		Returns
		-------
		string
			String corresponds to region of the input string following the 
			last backslash character 

		Examples
		--------
		>>> file_handlers = FileHandlers()
    	>>> file_paths = file_handlers.search_directory()
    	>>> fasta_files = file_handlers.find_files(file_paths, 'fasta')
    	>>> for i in range(len(fasta_files)):
    	...    print get_file_name(fasta_files[i])
		"""
		path_as_list = file_path.split('/')
		return path_as_list[-1]


	def filter_files(self, file_list, character):
		"""Filter a list of files by excluding all files that contain a
		particular character.

		Useful if you know that a certain file will never contain a particular
		character on the first line. For example you may want to filter out
		all .txt files in a list that do not contain \t character on the first 
		line and keep all the .txt files that contain tab delimited format

		Parameters
		----------
		file_list: list
			List of strings. Each string is the root path to the files staged
			for filtering
		character: string
			String form of character that will be searched for. i.e. if you
			want to filter out all files that do not contain tab delimited
			format, then character = '\t'

		Returns
		-------
		list
			List of strings. Each string is the root path to each file within
			the current working directory that does not contain the specified
			character. 

		Examples
		--------
		>>> file_handlers = FileHandlers()
		>>> file_paths = file_handlers.search_directory()
		>>> txt_files = file_handlers.find_files(file_paths, 'txt')
		>>> files_to_annotate = file_handlers.filter_files(txt_files, '\t')
		"""
		for file in file_list:
			for line in open(file):
				if '\t' not in line:
					break
				else:
					self.filtered_list.append(file)
					break
		return self.filtered_list


	def clean(self, values):
		"""Removes whitespace (including \n) from front and back of items in a 
		list.

		Useful for parsing csv files

		Parameters
		----------
		values: list
			List of strings that need to be cleaned of whitespace on front and
			back

		Returns
		-------
		list
			List of strings with no whitespace at beginning or end of string.
			Will not contain \n characters at beginning or end of string.

		Examples
		--------
		>>> test_file = '/path/to/test.csv'
		>>> for line in open(test_file):
		... 	file_handlers = FileHandlers()
		... 	fields = line.split(",")
		... 	print fields
		... 	cleaned = file_handlers.clean(fields)
		... 	print cleaned
		"""
		for field in values:
			self.cleaned.append(field.strip())  # strip() takes out white space from front and back of line
		return(self.cleaned)

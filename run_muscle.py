import subprocess
from util import FileHandlers


def run_muscle(path, file_name):
	name_list = file_name.split('.')
	out_file = ''.join(name_list[0] + '_out.fasta')
	cmd = ['muscle -in ' + path + ' -out ' + out_file]
	subprocess.call(cmd, shell=True)


def main():
	file_handlers = FileHandlers()
	file_paths = file_handlers.search_directory()
	pep_files = file_handlers.find_files(file_paths, 'pep')
	for pep_file in pep_files:
		file_name = file_handlers.get_file_name(pep_file)
		run_muscle(pep_file, file_name)

main()

#fasta_files = file_handlers.find_files(file_paths, 'fasta')
#for path in fasta_files:
#	file_name = file_handlers.get_file_name(path)
#	name_list = file_name.split('.')
#	derep_out_file = ''.join(name_list[0] + '_uniques.fasta')
#	dm_out_file = ''.join(name_list[0] + '_dm.txt')
#	cmd = ['usearch -derep_fulllength ' + path + ' -fastaout ' + derep_out_file]
#	subprocess.call(cmd, shell=True)
	











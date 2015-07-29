import subprocess
from util import FileHandlers


def get_dm_raxml(path, file_name, number_cores):
	name_list = file_name.split('_')
	out_file = ''.join(name_list[0] + '_dm')
	cmd = ['raxmlHPC-PTHREADS-AVX -s ' + path + ' -n ' + out_file + ' -m PROTGAMMABLOSUM62 -T ' + str(number_cores) + ' -p 7 -f x']
	subprocess.call(cmd, shell=True)


def main():
	file_handlers = FileHandlers()
	file_paths = file_handlers.search_directory()
	fasta_files = file_handlers.find_files(file_paths, 'fasta')
	for path in fasta_files:
		file_name = file_handlers.get_file_name(path)
		get_dm_raxml(path, file_name, 4)


main()










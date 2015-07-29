import os
import subprocess
from util import FileHandlers


file_handlers = FileHandlers()
file_paths = file_handlers.search_directory()
fasta_files = file_handlers.find_files(file_paths, 'faa')
print len(fasta_files)

for path in fasta_files:
	cmd = ['perl ./Scripts/MarkerScanner.pl -Bacteria ' + path]
	subprocess.call(cmd, shell=True)

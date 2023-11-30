# This allows imports from the parent directory
import sys
sys.path.append('..')
import signo as signo

file = signo.csvFile("./test.csv")

print(file.count())
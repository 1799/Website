import sys
from shutil import copyfile

fopen = open(sys.argv[1] + '.txt')
for line in fopen:
    line = line.rstrip()
    try:
        copyfile(sys.argv[1] + '/'+ line + '.mp3',
        '../Vocabulary/' + sys.argv[1] + '/' + line + '.mp3')
    except:
        print('Audio is not exist: ' + line)

import json
import math
import os
import sys
import threading
import shutil
import time
from threading import Thread
from shutil import copyfile
# import requests

TITLE_COLOR = '#37003C'
TEXT_COLOR = '#333300'
RED_COLOR = '#FF0000'
TITLE_FONT_SIZE = '28px'
SECTION_FONT_SIZE = '22px'
TEXT_FONT_SIZE = '16px'
HL_FONT_SIZE = '16px'
BOLD_BEGIN = '<strong>'
BOLD_END = '</strong>'
HIGHLIGHT_BEGIN = '<u>'
HIGHLIGHT_END = '</u>'
ITALIC_BEGIN = '<em>'
ITALIC_END = '</em>'
SECTION_HEIGHT = '0'

def check_character(character, line):
    if character in line:
        return line.find(character)
    else:
        return -1

def open_file(file):
    fopen = open(file + '.txt')
    fopen_json = open(file + '.html', "w+")
    fopen_json.truncate()
    fopen_json.write('<!DOCTYPE html>\n' + '<html>\n' + '<body>\n')
    fopen_json.write('<head>\n')
    fopen_json.write('<meta charset="UTF-8">\n')
    # fopen_json.write('<style>\n')
    # fopen_json.write('padding: 35px;\n')
    # fopen_json.write('</style>')
    fopen_json.write('</head>\n')
    for line in fopen:
        line = line.rstrip()
        if line.startswith('~'):
            fopen_json.write('<p style="text-align: center;">' \
                            + '<span style="font-size: ' + TITLE_FONT_SIZE \
                            + '; color: ' + TITLE_COLOR + ';">'\
                            + BOLD_BEGIN + line[1:] + BOLD_END + '</span></p>' + '\n')
        elif line.startswith('`'):
            fopen_json.write('<p style="text-align: justify;">' + '<span style="font-size: ' + SECTION_FONT_SIZE \
                            + '; color: ' + TITLE_COLOR + ';' \
                            + 'line-height: ' + SECTION_HEIGHT + ';">' \
                            + BOLD_BEGIN + HIGHLIGHT_BEGIN + line[1:] \
                            + HIGHLIGHT_END + BOLD_END + '</span>')
        elif line.startswith('!'):
            fopen_json.write('<p>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                            + '; color: ' + TITLE_COLOR + ';">' \
                            + BOLD_BEGIN + HIGHLIGHT_BEGIN + line[1:] \
                            + HIGHLIGHT_END + BOLD_END + '</span></p>\n')
        elif line.startswith('@'):
            fopen_json.write('<p>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                                + '; color: ' + TEXT_COLOR + ';">' + BOLD_BEGIN + line[1:] + BOLD_END + '</span></p>\n')
        elif line.startswith('- '):
            check = check_character(':', line)
            if check == -1:
                fopen_json.write('<p>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                                + '; color: ' + TEXT_COLOR + ';">' + BOLD_BEGIN + '-' + line[1:] + BOLD_END + '</span></p>\n')
            else:
                fopen_json.write('<p>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                                + '; color: ' + TEXT_COLOR + ';">' + BOLD_BEGIN + '-' + line[1:check] + BOLD_END + line[check:] + '</span></p>\n')

        elif line.startswith(' + '):
            check = check_character(':', line)
            if check == -1:
                fopen_json.write('<p>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                                + '; color: ' + TEXT_COLOR + ';">' + '&nbsp;&nbsp;' \
                                + BOLD_BEGIN + '&bull;' + line[2:] + BOLD_END + '</span></p>\n')
            else:
                fopen_json.write('<p>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                                + '; color: ' + TEXT_COLOR + ';">' + '&nbsp;&nbsp;' \
                                + BOLD_BEGIN + '&bull;' + line[2:check] + BOLD_END + line[check:] + '</span></p>\n')

        elif line.startswith('   '):
            fopen_json.write('<p>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                            + '; color: ' + TEXT_COLOR + ';">' \
                            + ITALIC_BEGIN + '&nbsp;&nbsp;&nbsp;&nbsp;' + '&rArr;' + line + ITALIC_END + '</span></p>\n')
        elif line.startswith('  '):
            fopen_json.write('<p>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                            + '; color: ' + TEXT_COLOR + ';">' \
                            + ITALIC_BEGIN + '&nbsp;&nbsp;&nbsp;' + '&rArr;'  + line + ITALIC_END + '</span></p>\n')

        # elif line.startswith('---'):
        #     fopen_json.write('</p>' + "\n")
        else:
            print('Missing line' + line + " " + file)
    fopen_json.write('</body>\n' + '</html>\n')
    fopen_json.close()
    fopen.close()

def convert_file():
    fopen = open('../Grammar/' + sys.argv[1] + '.html', "w+")



def main():
    # create json file
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".txt"):
            # print(os.path.splitext(filename)[0])
            open_file(os.path.splitext(filename)[0])
         # print(os.path.join(directory, filename))
            continue
        else:
            continue
    print(check_character('i', 'abcdefgh'))

if __name__ == '__main__':
    main()

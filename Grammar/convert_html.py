import json
import math
import os
import sys
import threading
import shutil
import time
from threading import Thread
from shutil import copyfile
import requests

TITLE_COLOR = '#37003C'
TEXT_COLOR = '#333300'
RED_COLOR = '#FF0000'
TITLE_FONT_SIZE = '30px'
SECTION_FONT_SIZE = '24px'
TEXT_FONT_SIZE = '18px'
HL_FONT_SIZE = '20px'
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

def open_file():
    fopen = open(sys.argv[1] + '.txt')
    fopen_json = open(sys.argv[1] + '.html', "w+")
    fopen_json.truncate()
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
            fopen_json.write('<br>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                            + '; color: ' + TITLE_COLOR + ';">' \
                            + BOLD_BEGIN + HIGHLIGHT_BEGIN + line[1:] \
                            + HIGHLIGHT_END + BOLD_END + '</span>')
        elif line.startswith('@'):
            fopen_json.write('<br>' + '<span style="font-size: ' + HL_FONT_SIZE \
                            + '; color: ' + RED_COLOR + ';">' \
                            + '&nbsp;&nbsp;&nbsp;&nbsp;' + BOLD_BEGIN + line[1:] + BOLD_END + '</span>')
        elif line.startswith('- '):
            check = check_character(':', line)
            if check == -1:
                fopen_json.write('<br>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                                + '; color: ' + TEXT_COLOR + ';">' + BOLD_BEGIN + '>&#9989;' + line[1:] + BOLD_END + '</span>')
            else:
                fopen_json.write('<br>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                                + '; color: ' + TEXT_COLOR + ';">' + BOLD_BEGIN + '>&#9989;' + line[1:check] + BOLD_END + line[check:] + '</span>')

        elif line.startswith(' + '):
            check = check_character(':', line)
            if check == -1:
                fopen_json.write('<br>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                                + '; color: ' + TEXT_COLOR + ';">' + '&nbsp;&nbsp;' \
                                + BOLD_BEGIN + '&#10146;' + line[2:] + BOLD_END + '</span>')
            else:
                fopen_json.write('<br>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                                + '; color: ' + TEXT_COLOR + ';">' + '&nbsp;&nbsp;' \
                                + BOLD_BEGIN + '&#10146;' + line[2:check] + BOLD_END + line[check:] + '</span>')

        elif line.startswith('   '):
            fopen_json.write('<br>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                            + '; color: ' + TEXT_COLOR + ';">' \
                            + ITALIC_BEGIN + '&nbsp;&nbsp;&nbsp;&nbsp;' + '&#9998;' + line + ITALIC_END + '</span>')
        elif line.startswith('  '):
            fopen_json.write('<br>' + '<span style="font-size: ' + TEXT_FONT_SIZE \
                            + '; color: ' + TEXT_COLOR + ';">' \
                            + ITALIC_BEGIN + '&nbsp;&nbsp;&nbsp;' + '&#9998;'  + line + ITALIC_END + '</span>')

        elif line.startswith('---'):
            fopen_json.write('</p>' + "\n")
        else:
            print('Missing line' + line)
    fopen_json.close()
    fopen.close()

def convert_file():
    fopen = open('../Grammar/' + sys.argv[1] + '.html', "w+")



def main():
    # create json file
    open_file()
    print(check_character('i', 'abcdefgh'))

if __name__ == '__main__':
    main()

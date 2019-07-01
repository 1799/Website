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
CURRENT_PATH = os.getcwd()
MP3_FILENAME_EXTENSION = '.mp3'
DIR_PATH = sys.argv[1] +'/'
TOTAL_THREADS = 30
DATA_FILE = sys.argv[1] +'.json'
flag = False


def download_mp3(word, url, dir_path):
    filename = os.path.join(dir_path, word + MP3_FILENAME_EXTENSION)
    with open(filename, 'wb') as file:
        file.write(requests.get(url).content)


# split a dictionary into a list of dictionaries
def split_dict_evenly(m_dict, segment_count):
    if segment_count == 1:
        return [m_dict]

    segment_length = math.ceil(len(m_dict) / segment_count)
    keys = list(m_dict.keys())
    key_groups = [keys[segment_length * i: segment_length * (i + 1)] for i in range(segment_count)]
    return [{key: m_dict[key] for key in group} for group in key_groups]


# a single downloader thread
class DownloadWorker(Thread):
    # 'pairs' is a dictionary
    def __init__(self, pk, pairs, dir_path, statistics):
        Thread.__init__(self)
        self.pk = pk
        self.pairs = pairs
        self.dir_path = dir_path
        self.statistics = statistics

    def run(self):
        for word, url in self.pairs.items():
            # if os.path.exists(os.path.join(self.dir_path, word + MP3_FILENAME_EXTENSION)):
            #     self.statistics.decrease_total()
            #     continue
            current = self.statistics.increase_current()
            print('(' + str(current) + '/' + str(self.statistics.total) + ') ' + word)
            try:
                download_mp3(word, url, self.dir_path)
            except:
                print("Failed")

# provide a mutex on a shared integer representing current progress
class Statistics:
    # pass in the total number in the constructor
    def __init__(self, total):
        self.total = total
        self.current = 0
        self.total_lock = threading.Lock()
        self.current_lock = threading.Lock()

    # an atom operation to increase the current progress
    def increase_current(self):
        self.current_lock.acquire()
        self.current += 1
        value = self.current
        self.current_lock.release()
        return value

    def decrease_total(self):
        self.total_lock.acquire()
        self.total -= 1
        value = self.total
        self.total_lock.release()
        return value

def create_json_file():
    global flag
    counter = 0
    json_file = open('ultimate.json', 'r')
    data = json.loads(json_file.read())
    fopen = open(sys.argv[1] + '.txt')
    fopen_json = open(sys.argv[1] + '.json', "w+")
    fopen_json.truncate()
    fopen_json.write('{\n')
    lines = fopen.read().splitlines()
    fopen = open(sys.argv[1] + '.txt')
    last_line = lines[-1]
    last_line_signal = ','
    for line in fopen:
        line = line.rstrip()
        if(line ==last_line):
            last_line_signal = ''
        try:
            object_range = len(data[line])
        except:
            object_range = 0
            flag = True
            print("Word not found: " + line)
        for i in range(object_range):
            counter = counter+1
            if(data[line][i].startswith('http://s3.amazonaws.com')):
                fopen_json.write('\t' + '"' + line + '": "'  + data[line][i] + '"' + last_line_signal +'\n')
                counter = 0
                break
            if(counter == object_range):
                counter = 0
                print("Word not found in Amazon: " + line)

    fopen_json.write('}\n')
    fopen_json.close()
    fopen.close()

def copy_audio_file():
    fopen = open(sys.argv[1] + '.txt')
    for line in fopen:
        line = line.rstrip()
        try:
            copyfile(sys.argv[1] + '/'+ line + '.mp3',
            '../Vocabulary/' + sys.argv[1] + '/' + line + '.mp3')
        except:
            print('Audio is not exist: ' + line)
def delete_folder():
    shutil.rmtree(sys.argv[1] + '/')

def main(total_threads):
    # create json file
    global flag
    flag = False
    create_json_file()
    print(flag)
    if (flag == True):
        sys.exit()
    # create directory
    if not os.path.exists(DIR_PATH):
        os.makedirs(DIR_PATH)

    # load data into dictionary
    with open(DATA_FILE, 'r') as file:
        data = json.loads(file.read())

    # split dictionary into a list of dictionaries, each for a thread
    data_segments = split_dict_evenly(data, total_threads)

    # initialize shared object statistics
    statistics = Statistics(len(data))

    # start downloader threads
    for i in range(total_threads):
        worker = DownloadWorker(i + 1, data_segments[i], DIR_PATH, statistics)
        worker.start()
    time.sleep(10)
    copy_audio_file()
    delete_folder()


if __name__ == '__main__':
    argument = 30
    main(argument)

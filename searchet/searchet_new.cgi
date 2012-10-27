#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# this script serves to act as the gate
# to search different sources
#
# @author Yuan Jin
# @contact jinyuan@baidu.com
# @created Aug. 1, 2012
# @updated Sept. 27, 2012
#

# imports and CONSTANTS
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import cgi
import string
import tesseract
import threading

import Queue
queue = Queue.Queue()

from srdispatcher import QueryDispatcher


def text_process(keywords):
    '''string process'''
    def text_to_lower_capitalized(keyword):
        # the key might be all lower-cased letters
        lower_cased = '_'.join(token.strip() for token in keyword.lower().split())
        # or capitalized
        capitalized = '_'.join(token.strip() for token in keyword.title().split())
        return lower_cased, capitalized

    output_lower = []
    output_capitalized = []
    output_plain = []
    for key in keywords:
        whitelist = string.letters + string.digits + ' '
        keyword = re.sub("[^0-9a-zA-Z]", " ", keywords[key]).strip()

        lower, capitalized = text_to_lower_capitalized(keyword)
        output_lower.append(lower)
        output_capitalized.append(capitalized)
        output_plain.append(keyword.strip())

    return  ' '.join(output_plain)

class OCR_Thread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            file_path = self.queue.get()
            f = open('/var/www/cgi-bin/%s' % file_path).read()
            screenshots[file_path] = tesseract.ProcessPagesBuffer(f, len(f), api)
            self.queue.task_done()

def ocr(files):
    # thread pool
    global api
    api = tesseract.TessBaseAPI()
    api.Init(".", "eng", tesseract.OEM_DEFAULT)

    number_of_tasks = len(screenshots)
    number_of_threads = 5
    if number_of_tasks > 5:
        number_of_threads = 5
    else:
        number_of_threads = number_of_tasks
    for t in xrange(number_of_threads):
        ot = OCR_Thread(queue)
        ot.setDaemon(True)
        ot.start()
    queue.join()
    return screenshots

def read_http(environ):
    'read binary image file and write to local disk'
    global screenshots
    screenshots = {}
    bin_data = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    for key in bin_data.keys():
        f = open('/var/www/cgi-bin/%s.jpg' % key, 'wb')
        f.write(bin_data[key].value)
        f.close()
        screenshots['%s.jpg' % key] = ''
        queue.put('%s.jpg' % key)
    return screenshots

def application(environ, start_response):
    try:
        files = read_http(environ)
        ocr_texts = ocr(files)
        tokens = text_process(ocr_texts)
        dispatcher = QueryDispatcher(tokens)
        output = str(dispatcher.dispatch())

        if output is None:
            raise Exception('Void output!')
        header = [('Content-type', 'text/html'), ('Content-Length', str(len(output)))]

        f = open('/var/www/cgi-bin/index.html', 'w')
        f.write(output)
        f.close()
        start_response("200 OK", header)
        return [output]
    except Exception, e:
        header = [('Content-type', 'text/html'), ('Content-Length', str(len(str(e))))]
        start_response("200 OK", header)
        return [str(e)]


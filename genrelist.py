#!/usr/bin/python

import os
import sys
import errno
import logging
import re
import argparse
import mysql.connector
import mutagen
import contextdef
import logging as log


class Context(object):
    def __init__(self):
        self.name = 'context'
        db = None
        trace = None
        current_band = None
        current_album = None
        printd = None

    def __str__(self):
        # return ; .join([, .join([x, getattr(self, x)]) for x in vars(self)])
        return str(vars(self))


prog_descrip = """
    Creates a list of subdirectories sorted by genre
    Parameters are:"""


def main():
    global context, mylog, tfile
    context = Context()
    mylog = None
    tfile = None

    proc_args()
    context.db = {'source': os.path.split(context.directory)[1], 'bands': {}}

    walk_dir(proc_directory, proc_file)


def proc_args():
    '''Processes the command line arguments'''
    global context, mylog
    parser = argparse.ArgumentParser(description=prog_descrip)
    parser.add_argument('-d', '--directory', default='.', help='Root directory for music files. Defaults to current directory.')
    parser.add_argument('-i', '--indent', type=int, default=3, help='Set the number of spaces for each level of indent. Defaults to 3')
    parser.add_argument('-p', '--printd', action='store_true', help='Print a list of directories and files. Defaults to false.')
    parser.add_argument('-g', '--group', default=None)
    parser.add_argument('-e', '--extensions', default=['mp3', 'flac'], nargs='+', type=ascii, help='File extensions to process. Default is mp3 and flac')
    parser.add_argument('-a', '--all', action='store_false', help='Process all files, regardless of extension. Default is false')

    parser.add_argument('-l', '--logname', default='glist.log', help='Optional path for logfile.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Optional.  Increases the amount of status output from the program.')

    parser.add_argument('-t', '--trace', action='store_true', help='Optional.  Enables creating a trace file for debugging')

    parser.parse_args(namespace=context)

    if context.directory == '.':
        context.directory = os.getcwd()

    ''' Logging configuration and setup '''
    # Set up logging, including level of logging and log file
    llevel = [logging.WARNING, logging.INFO, logging.DEBUG]
    ll = llevel[min(len(llevel)-1, context.verbose)]

    formatter = logging.Formatter('%(asctime)-8s %(levelname)-8s %(message)s')

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(ll)
    consoleHandler.setFormatter(formatter)

    fileHandler = logging.FileHandler(context.logname)
    fileHandler.setLevel(ll)
    fileHandler.setFormatter(formatter)

    context.log = logging.getLogger()
    context.log.setLevel(ll)
    context.log.addHandler(consoleHandler)
    context.log.addHandler(fileHandler)

    mylog = context.log
    mylog.info(f'Set log to {context.logname}')
    mylog.info('Command arguments read')
    mylog.debug(f"Setting logging level to {ll}")


    ''' Trace setup and configuration '''
    if context.trace is True:
        tfile = open('trace.txt', 'w', encoding='UTF-8')
        sys.settrace(tracefunc)


def proc_directory(dirName, depth=0):
    if depth == 1:
        band = os.path.split(dirName)[1]
        mylog.info(f'Found band {band}')
        context.db['bands'][band] = {}
        context.current_band = context.db['bands'][band]
        context.current_band['genre'] = set()
        context.current_band['path'] = dirName
    elif depth == 2:
        album_name = os.path.split(dirName)[1]
        mylog.info(f'  Found album {album_name}')

        context.current_band[album_name] = {
            'genre': set(),
            'songs': [],
            'path': dirName,
        }
        context.current_album = context.current_band[album_name]
    else:
        mylog.debug(f'In directory level greater than 3: {dirName}\n')
    return

    if context.printd:
        indent = ' '*context.indent*depth
        mylog.warning(f'{indent}Found directory: %s' % dirName)
    elif context.group is not None:
        pass


def proc_file(dirName, fileName, depth=0):
    if os.path.splitext(fileName)[1] in context.extensions:
        song = mutagen.File(fileName)
        context.current_album['genre'].add(song['genre'])
        context.current_band['genre'].add(song['genre'])
        context.current_album['songs'].append(song['Title'])
    return

    if not context.all and os.path.splitext()[1] not in context.extensions:
        return

    if context.printd:
        indent = ' '*context.indent*(depth + 1)
        mylog.warning(f'{indent}Found file: %s' % fileName)
    elif context.group is not None:
        pass


def walk_dir(dfunc, ffunc):
    init_depth = context.directory.count(os.sep)
    for dirName, subdirList, fileList in os.walk(context.directory):
        depth = dirName.count(os.sep) - init_depth
        if dfunc:
            dfunc(dirName, depth)
            for fname in fileList:
                if ffunc:
                    ffunc(dirName, fname, depth)


def tracefunc(frame, event, arg, indent=[0]):
    ''' Creates trace of script execution for debugging. '''
    fname = frame.f_code.co_filename
    if not re.search('lib64', fname):
        fpath = fname + ", " + frame.f_code.co_name
        if event == "call":
            indent[0] += 2
            tfile.write("-" * indent[0] + "> call function " + fpath + "\r")
        elif event == "return":
            tfile.write("<" + "-" * indent[0] + "exit function " + fpath + "\r")
            indent[0] -= 2
    return tracefunc


if __name__ == '__main__':
    main()

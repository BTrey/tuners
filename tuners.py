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

logger = None
context = None

prog_descrip = """
    tuners - music library tool
    Parameters are:"""


def main():
    global context, my_args, tfile, db
    context = contextdef.Context()
    db = None
    tfile = None
    my_args = proc_args()

    # Set music directory
    try:
        my_args.directory
    except NameError:
        try:
            my_args.directory = sys.argv[1]
        except IndexError:
            my_args.directory = '.'

    if(my_args.list):
        walk_dir(print_dir, print_file)

    if(my_args.genre):
        if context.cursor is None:
            init_db()
        get_genre(my_args.genre)


def proc_args():
    '''Processes the command line arguments'''
    global context, logger
    parser = argparse.ArgumentParser(description=prog_descrip)
    parser.add_argument('-l', '--list', action='store_true', help='Optional. Walk the directory and print each folder and file name')
    parser.add_argument('-d', '--directory', help='Optional. Set the root directory for music files')

    parser.add_argument('-s', '--server', help='Hostname or ip of the server hosting the database')
    parser.add_argument('-u', '--user', help='username for logging into the database')
    parser.add_argument('-p', '--password', help='password for database user')
    parser.add_argument('-n', '--dbname', help='name of the database')

    parser.add_argument('-g', '--genre', help='Get ID of genre')

    parser.add_argument('-L', '--log', help='Optional path for logfile.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Optional.  Increases the amount of status output from the program.')

    parser.add_argument('-t', '--trace', action='store_true', help='Optional.  Enables creating a trace file for debugging')

    cl_args = parser.parse_args()

    ''' Logging configuration and setup '''
    # Set up logging, including level of logging and log file
    llevel = [logging.WARNING, logging.INFO, logging.DEBUG]
    ll = llevel[min(len(llevel)-1, cl_args.verbose)]

    formatter = logging.Formatter('%(asctime)-8s %(levelname)-8s %(message)s')

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(ll)
    consoleHandler.setFormatter(formatter)

    if cl_args.log:
        log_file = cl_args.log
    else:
        log_file = 'tuners.log'

    fileHandler = logging.FileHandler(log_file)
    fileHandler.setLevel(ll)
    fileHandler.setFormatter(formatter)

    context.log = logging.getLogger()
    context.log.addHandler(consoleHandler)
    context.log.addHandler(fileHandler)

    logger = context.log

    logger.info('Command arguments read')

    ''' Trace setup and configuration '''
    if(cl_args.trace is True):
        tfile = open('trace.txt', 'w')
        sys.settrace(tracefunc)

    '''Database Configuration '''
    if(cl_args.server is True):
        context['host'] = cl_args.host

    if(cl_args.user):
        context['user'] = cl_args.host

    if(cl_args.password):
        context['password'] = cl_args.password

    if(cl_args.dbname):
        context['dbname'] = cl_args.dbname

    return cl_args


def init_db():
    logger.info('Initiating database.')
    context.connector = mysql.connector.connect(
        host=context.host,
        user=context.user,
        password=context.password,
        database=context.dbname,
    )
    context.cursor = context.connector.cursor()


def print_dir(dirName):
    print('Found directory: %s' % dirName)


def print_file(dirName, fileName):
    print('\tFound file: %s' % fileName)


def walk_dir(dfunc, ffunc):
    for dirName, subdirList, fileList in os.walk(my_args.directory):
        if dfunc:
            dfunc(dirName)
            for fname in fileList:
                if ffunc:
                    ffunc(dirName, fname)


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


def scan_tags(file_path):
    mutagen.File(file_path)


def get_genre(value):
    query_select = 'SELECT id FROM genres WHERE NAME = "{}"'.format(value)
    context.cursor.execute(query_select)
    id = context.cursor.fetchone()
    if id is None:
        query_insert = 'INSERT INTO genres (name) VALUES ("{}")'.format(value)
        context.cursor.execute(query_insert)
        context.cursor.execute(query_select)
        id = context.cursor.fetchone()
    return id


if __name__ == '__main__':
    main()

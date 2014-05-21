# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import tempfile
import shutil
import os

import core
from core import Smush

class Smusher:
    def __init__(self, temp_dir = None):
        if temp_dir is None:
            self.temp_dir = tempfile.gettempdir()
        else:
            self.temp_dir = temp_dir
        self.exclude = ['.bzr', '.git', '.hg', '.svn']
        pass

    def process(self, input_src, output = None, strip_jpg_meta = False, 
            exclude = [], recursive = True, list_only = False, quiet = True,
            identify_mime = False):
        '''Prepare image on a temporary location and optimizes it
        
        Keyword arguments:
        input_src -- a tuple (img_data_buffer, mime), a string with a file path or a list with tuples or strings (can be mixed)
        output -- a path for a directory to save the optimized files.
        strip_jpg_meta -- Boolean: Strip all meta-data from JPEGs (Default False)
        exclude -- list of files to ignore (Default ['.bzr', '.git', '.hg', '.svn'])
        recursive -- process directories recursively (Default True)
        list_only -- Perform a trial run with no output (Default False)
        quiet -- Don't print optimisation statistics at the end (Default True)
        identify_mime -- Fast identify image files via mimetype (Default False)

        Output:
        None if argument output is not None. A list of byte buffer otherwise.

        Remarks:
        The original buffer or files are untouched
        '''

        return_data = None

        if quiet:
            logging.basicConfig(
                level=logging.WARNING,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
        else:
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')

        exclude_list = self.exclude + exclude
        smush = Smush(strip_jpg_meta=strip_jpg_meta, exclude=exclude_list,
            list_only=list_only, quiet=quiet, identify_mime=identify_mime)

        work_temp_dir = self._prepare_input(input_src)

        smush.process(work_temp_dir, True)

        if output is not None:
            if os.path.exists(output) and os.path.isdir(output):
                for item in os.listdir(work_temp_dir):
                    if os.path.exists(item):
                        if os.path.isdir(item):
                            shutil.rmtree(item)
                        else:
                            os.remove(item)
                    shutil.move('%s/%s'%(work_temp_dir, item), output)
            else:
                shutil.move(work_temp_dir, output)
        else:
            return_data = []
            for root, _, files in os.walk(work_temp_dir):
                for fname in files:
                    fullpath = os.path.join(root, fname)
                    f = open(fullpath, 'r+b')
                    return_data.append(f.read())
                    f.close()

        if os.path.exists(work_temp_dir):
            shutil.rmtree(work_temp_dir)

        return return_data


    def _prepare_input(self, input_src):
        list_input = []

        if isinstance(input_src, list):
            list_input += input_src
        else:
            list_input.append(input_src)

        current_temp_dir = tempfile.mkdtemp(dir=self.temp_dir)
        for i in list_input:
            if isinstance(i, str) and os.path.exists(i):
                if os.path.isdir(i):
                    cpdir_basename = os.path.basename(os.path.abspath(i))
                    cpdir = os.path.normpath('%s/%s' % (current_temp_dir, 
                        cpdir_basename))
                    shutil.copytree(i, cpdir)
                elif os.path.isfile(i):
                    shutil.copy(i, current_temp_dir)
            elif isinstance(i, tuple):
                buff, mime = i
                temp_file = tempfile.NamedTemporaryFile(
                    dir = current_temp_dir, suffix = '.%s' % mime, 
                    delete = False)
                temp_file.write(buff)

        return current_temp_dir

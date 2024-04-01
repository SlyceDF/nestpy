from enum import Enum as _Enum
from glob import glob as _glob
from os import mkdir as _mkdir
from os import path as _path
from os import remove as _remove
from os import walk as _walk
from shutil import copyfile as _copyfile
from shutil import rmtree as _rmtree

from . import main as _m

slashConverter = str.maketrans('\\','/')
def _getAllFilePaths(dirPath):
    return [
        _path.join(dirpath,f).translate(slashConverter) for (
            dirpath, dirnames, filenames
        ) in _walk(dirPath) for f in filenames
    ]

def _filterByFileExt(files, fileExt):
    passed = []
    failed = []
    for file in files:
        if _path.splitext(file)[-1] == fileExt:
            passed.append(file)
            continue
        failed.append(file)
    return passed, failed

def ncompile_to(file, new_file=None, indent_amount=1, replace_previous=False):
  if new_file is None:
    new_file = file.rsplit('.', 1)[0] + '.py'
  def compile(file):
    print(f'> compiling {file}')
    with (
      open(file, 'r') as f, 
      open(new_file, 'w') as fn):
        fn.write(_m.ncompile(f.read(), indent_amount))
  if not _path.isfile(new_file) or replace_previous:
    compile(file)
  else:
    i = input(
      f'File \'{file}\' already exists. Would you like to overwrite it? [y/(n)]: ')
    if i.lower() == 'y':
      compile(file)

def nbuild(dir, new_dir, indent_amount=1, erase_dir=False, 
           replace_previous=False, transfer_other_files=True):
    if _path.isdir(new_dir):
      def remove():
        _rmtree(new_dir)
        _mkdir(new_dir)
      if erase_dir:
        remove()
      else:
        i = input(
          f'Directory \'{new_dir}\' already exists. Would you like to erase it? [y/(n)]: ')
        if i.lower() == 'y':
          remove()
    else:
      _mkdir(new_dir)
    compilable, leaveBe = _filterByFileExt(_getAllFilePaths(dir), '.npy')
    for file in compilable:
      ncompile_to(file, f'{new_dir}/{file.split("/")[-1].rsplit(".", 1)[0]}.py', 
               indent_amount, replace_previous)
    if transfer_other_files:
      for file in leaveBe:
        print(f'> transferring {file}')
        _copyfile(file, f'{new_dir}/{file.split("/")[-1]}')

def ncompile(file, indent_amount=1):
  with open(file, 'r') as f:
    return _m.ncompile(f.read(), indent_amount)

def nexec(file):
  exec(ncompile(file))

from enum import Enum as _Enum
from glob import glob as _glob
from os import mkdir as _mkdir
from os import path as _path
from os import remove as _remove
from os import walk as _walk
from os import scandir as _scandir
from os import chdir as _chdir
from os import getcwd as _getcwd
from shutil import copyfile as _copyfile
from shutil import rmtree as _rmtree

from . import main as _m

_slashConverter = str.maketrans('\\','/')
def _getAllFilePaths(dirPath):
    return [
        _path.join(dirpath,f).translate(_slashConverter) for (
            dirpath, dirnames, filenames
        ) in _walk(dirPath) for f in filenames
    ]

def _getFilesDirs(dirPath):
    oldDir=_getcwd()
    _chdir(dirPath)
    a = []
    b = []
    for f in _scandir():
        g = f.path.translate(_slashConverter).removeprefix('./')
        if f.is_dir():
            b.append(g)
        else:
            a.append(g)
    _chdir(oldDir)
    return a, b

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


def nbuild(dir, new_dir, indent_amount=1, erase_dir=None,
           replace_previous=False, transfer_other_files=True):
 subpath = ''
 def subbuild():
    nonlocal dir
    nonlocal subpath
    nonlocal new_dir
    nonlocal indent_amount
    nonlocal erase_dir
    nonlocal replace_previous
    nonlocal transfer_other_files
    if _path.isdir(f'{new_dir}/{subpath}'):
      def remove():
        _rmtree(f'{new_dir}/{subpath}')
        _mkdir(f'{new_dir}/{subpath}')
      match erase_dir:
        case True:
          remove()
        case None:
          i = input(
            f'Directory \'{new_dir}/{subpath}\' already exists. Would you like to erase it? [y/(n)]: ')
          if i.lower() == 'y':
            remove()

    else:
      _mkdir(f'{new_dir}/{subpath}')
    compilable, leaveBe = _filterByFileExt(_getFilesDirs(f'{dir}/{subpath}')[0], '.npy')
    print(_getFilesDirs(f'{dir}/{subpath}'))
    for file in compilable:
      ncompile_to(f'{dir}/{subpath}/{file}', f'{new_dir}/{subpath}/{file.rsplit("/", 1)[-1].rsplit(".", 1)[0]}.py',
               indent_amount, replace_previous)
    if transfer_other_files:
      for file in leaveBe:
        print(f'> transferring {dir}/{subpath}/{file}')
        _copyfile(f'{dir}/{subpath}/{file}', f'{new_dir}/{subpath}/{file.rsplit("/", 1)[-1].lstrip("/")}')
    for subdir in _getFilesDirs(f'{dir}/{subpath}')[~0]:
        subpath += subdir
        subbuild()

 subbuild()

def ncompile(file, indent_amount=1):
  with open(file, 'r') as f:
    return _m.ncompile(f.read(), indent_amount)

def nexec(file):
  exec(ncompile(file))

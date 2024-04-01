from os import path as osp, system as runcmd
import argparse

def read(filename):
    return open(osp.join(osp.dirname(__file__), filename)).read()


parser = argparse.ArgumentParser()

parser.add_argument('--version', type=str,
                    help='version of distribution')

parser.add_argument('--test', action='store_true',
                    help='testpypi vs. pypi upload')

args = parser.parse_args()

version = '0.0.0'


param = eval(read('core/param.i'))


try:
    version = args.version
except IndexError:
    pass

if version == '.':
    version = param['version']

test = args.test

with open('core/param.i', 'w') as f:
    f.write(str({'test': test, 'version': version}))

runcmd(read('setup.bat'))

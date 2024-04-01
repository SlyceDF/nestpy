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

try:
    version = args.version
except IndexError:
    pass

test = args.test

f = open('core/param.i', 'w')
f.write(str({'test': test, 'version': version}))
f.close()

runcmd(read('setup.bat'))

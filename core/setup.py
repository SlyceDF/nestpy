from setuptools import find_packages, setup
from os import path as osp, system as runcmd

def read(filename):
    return open(osp.join(osp.dirname(__file__), filename)).read()


param = eval(read('param.i'))

version = param['version']
test = param['test']
setup(
    name='nestpy',
    packages=find_packages(include=['nestpy']),
    version=version,
    description='python with braces.',
    author='slycedf',
    license='MIT',
    long_description=read('README.md'),
    classifiers=["Development Status :: 3 - Alpha"]
)

token = open(f'D:/slycefolder/ins/all/{ {True: "tt", False: "tr"}[test]}', 'r').read()

runcmd(
    f'pause & twine upload --repository { {True: "testpypi", False: "pypi"}[test]} dist/*{version}* -u __token__ -p {token} --verbose')

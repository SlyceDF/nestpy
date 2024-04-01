from setuptools import find_packages, setup
from os import path as osp, system as runcmd

def read(filename):
    return open(osp.join(osp.dirname(__file__), filename)).read()


param = eval(read('param.i'))

version = param['version']
test = param['test']
setup(
    name='nestpython',
    packages=find_packages(include=['nestpy']),
    version=version,
    description='python with braces.',
    author='slycedf',
    license='MIT',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta"
    ]
)

token = open(f'D:/slycefolder/ins/nsp/{ {True: "tt", False: "tr"}[test]}', 'r').read()

runcmd(
    f'pause & twine upload --repository { {True: "testpypi", False: "pypi"}[test]} dist/*{version}* -u __token__ -p {token} --verbose')

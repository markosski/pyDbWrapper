
from pydbwrapper import __version__
from distutils.core import setup

setup(
    name='pyDbWrapper',
    version=__version__,
    author='Marcin Kossakowski',
    author_email='marcin.kossakowski@gmail.com',
    packages=['pydbwrapper'],
    url='git://github.com/martez81/pyDbWrapper.git',
    license='LICENSE.txt',
    description='MySQL python driver wrapper',
    long_description=open('README.txt').read(),
    install_requires = ["MySQL-python >= 1.2.2"]
)
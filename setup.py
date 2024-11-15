import io
from datetime import datetime
from setuptools import setup, find_packages

now = datetime.now()

setup(
    name='app',
    version='0.1.0',
    long_description=io.open('README.md', 'r').read(),
    platforms=['POSIX', 'MacOS'],
    author='Perica Prokic',
    author_email='pprokic22@gmail.com',
    maintainer='Perica Prokic',
    maintainer_email='pprokic22@gmail.com',
    packages=find_packages(),
)

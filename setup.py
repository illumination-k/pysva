import os, sys
from setuptools import setup, find_packages

def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join('.', 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements

setup(
    name='ngsutils',
    version='0.0.1',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='illumination-k',
    author_email='illumination.k.27@gmail.com',
    install_requires=read_requirements(),
    url='https://github.com/illumination-k/pysva',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='test'
)
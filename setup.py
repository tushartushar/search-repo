from os import path
from setuptools import setup, find_packages

with open('requirements.txt') as reqs_file:
    requirements = reqs_file.read().splitlines()

long_description = 'The package searches repositories on GitHub using GraphQL API. One may specify parameters such as programming language, start date, and number of stars to get a list of GitHub repositories modified on or after the specified start date and satisfying other filters.'

setup(
    name='search-repo',
    description='Search repositories on GitHub',
    long_description=long_description,
    author='Tushar Sharma',
    author_email='000.tushar@gmail.com',
    version='1.0.0',
    packages=find_packages('.'),
    url='https://github.com/tushartushar/search-repo',
    license='Apache License',
    package_dir={'search-repo': 'search-repo'},
    python_requires='>=3.7',
    install_requires=requirements,
    classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Software Development :: Libraries :: Python Modules',
            "Operating System :: OS Independent",
            "Operating System :: POSIX",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS :: MacOS X",
            ]
)
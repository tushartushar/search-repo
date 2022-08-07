import os

from setuptools import setup, find_packages

with open('requirements.txt') as reqs_file:
    requirements = reqs_file.read().splitlines()

long_description = '''
The package searches repositories on GitHub using GraphQL API. One may specify parameters such as programming language, start date, and number of stars to get a list of GitHub repositories modified on or after the specified start date and satisfying other filters.

## Parameters
- `--api-token`: GitHub API token or Personal Access Token
- `--out-file`: Output file path
- `--start-date`: Start date for search in dd-mm-yyyy
- `--lang`: Primary programming language of the repositories (optional, default=Java)
- `--min-stars`: Minimum star count (optional, default=0)
- `--verbose`: Verbose mode (optional, default=false)

## Example
```shell
python3 searchrepo.py --api-token 51ec41929c6f48c23482a734534327d308 --out-file 'repos.csv' --start-date '06-08-2022'
```
'''

setup(
    name='searchgithubrepo',
    description='Search repositories on GitHub',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Tushar Sharma',
    author_email='000.tushar@gmail.com',
    version='1.0.3',
    packages=find_packages('.'),
    url='https://github.com/tushartushar/search-repo',
    license='Apache License',
    py_modules=["searchrepo"],
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
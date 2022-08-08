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
- `--lang`: Primary programming language of the repositories 
- `--min-stars`: Minimum star count 
- `--verbose`: Verbose mode 

## Example
Install `searchgithubrepo` package using `pip` and use it in your program.
```python
from searchrepo import search_repo

one_day_old_date = (datetime.datetime.now().date() - datetime.timedelta(days=1))
search_repo(start_date=one_day_old_date,
            out_file='repos.csv',
            api_token='51ec41929c6f48c23482a734534327d308',
            stars=100,
            lang='Java', 
            verbose=True)
```
'''

setup(
    name='searchgithubrepo',
    description='Search repositories on GitHub',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Tushar Sharma',
    author_email='000.tushar@gmail.com',
    version='1.0.8',
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
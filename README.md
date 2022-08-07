# Search GitHub repositories
The script/package searches repositories on GitHub using GraphQL API. 

## Parameters
- `--api-token`: GitHub API token or Personal Access Token
- `--out-file`: Output file path
- `--start-date`: Start date for search in dd-mm-yyyy
- `--lang`: Primary programming language of the repositories (optional, default=Java)
- `--min-stars`: Minimum star count (optional, default=0)
- `--verbose`: Verbose mode (optional, default=false)

## Example
```shell
python3 main.py --api-token 51ec41929c6f48c23482a734534327d308 --out-file 'repos.csv' --start-date '06-08-2022'
```
import datetime
import json
import time

import requests
import argparse

URL = 'https://api.github.com/graphql'
MIN_REPO_SIZE = "100"  # in KBs
PAGE_LIMIT = 99  # maximum permitted is 100 but keep it 99 or below to satisfy 1000 node Pagination limit

count = 1
duplicate_count = 0
name_with_owner_list = []
local_name_with_owner_list = []

failed_dates = []
repo_count_exceed_case_dates = []


def _my_print(msg):
    if is_verbose:
        print(msg)


def _extract_name_with_owner_list(data):
    global duplicate_count
    global local_name_with_owner_list
    local_name_with_owner_list = []
    for edge in data['data']['search']['edges']:
        if edge['node']['nameWithOwner'] in name_with_owner_list:
            duplicate_count = duplicate_count + 1
            print("Duplicate = " + str(duplicate_count))
        else:
            if edge['node'] is not None:
                if edge['node']['nameWithOwner'] is not None and edge['node']['primaryLanguage'] is not None and \
                        edge['node']['pushedAt'] is not None:
                    if edge['node']['primaryLanguage']['name'] is not None:
                        local_name_with_owner_list.append(str(edge['node']['nameWithOwner']) + " " +
                                                      str(edge['node']['primaryLanguage']['name']) + " "
                                                      + str(edge['node']['pushedAt']))
                        name_with_owner_list.append(str(edge['node']['nameWithOwner']) + " " +
                                        str(edge['node']['primaryLanguage']['name']) + " " +
                                        str(edge['node']['pushedAt']))


# lang = 'Java' or 'Csharp'
def _get_json_query(repo_size, current_date, after_cursor, stars=0, lang='Java'):
    json_query = {'query': """{
                    search(query: "stars:>=""" + str(stars) + " language:""" + lang + """ size:""" + repo_size + """ pushed:""" + str(
        current_date) + """", type: REPOSITORY, first:  """ + str(PAGE_LIMIT)
                           + str(after_cursor) + """) {
                      edges {
                        node {
                          ... on Repository {
                            id
                            nameWithOwner
                            primaryLanguage {
                              name
                            }
                            pushedAt
                          }
                        }
                      }
                      repositoryCount

                      pageInfo {
                        hasNextPage
                        endCursor
                      }
                    }
                    rateLimit {
                      cost
                      limit
                      nodeCount
                      remaining
                      resetAt
                    }
                  }"""
                  }
    # print(json_query)
    return json_query


def _iterate_over_pages_and_append_file(out_file, api_token, stars, lang, size, possible, current_date, cursor):
    global count
    global duplicate_count
    global local_name_with_owner_list
    with open(out_file, 'a') as fi:
        while possible:
            after_cursor = ', after: "' + cursor + '"' if not str(cursor) == "" else ""
            json_data = _get_json_query(size, current_date, after_cursor, stars, lang)

            headers = {'Authorization': 'token %s' % api_token}
            r = requests.post(url=URL, json=json_data, headers=headers)
            data = json.loads(r.text)

            if r.status_code == 200:
                if data.get("data") is None:
                    failed_dates.append(current_date)
                    break
                _my_print("Repo Count: " + str(data['data']['search']['repositoryCount']))
                if data['data']['search']['repositoryCount'] > 1000:
                    _repo_count_exceeded(out_file, api_token, stars, lang, current_date, cursor, possible, size)
                    break
                _extract_name_with_owner_list(data)
                count = count + 1

                _my_print("Writing results from page " + str(count))
                for _ in local_name_with_owner_list:
                    fi.write(_ + '\n')

                page_info = data['data']['search']["pageInfo"]
                rate_limit_info = data['data']['rateLimit']
                _my_print("Call cost: " + str(rate_limit_info))
                _my_print("Page limit: " + str(page_info))

                if rate_limit_info['remaining'] == 0:
                    duration = (datetime.datetime.strptime(
                        rate_limit_info['resetAt'], '%Y-%m-%dT%H:%M:%SZ') -
                                datetime.datetime.utcnow()).total_seconds() + 1
                    _my_print("Limit exhausted. Sleep for "+ str(duration) + " secs")
                    time.sleep(duration)
                    continue

                if page_info['hasNextPage']:
                    cursor = page_info['endCursor'] if page_info['endCursor'] is not None else ""
                else:
                    possible = False

            else:
                _my_print("Request failed. Response: " + str(r.text))
                failed_dates.append(current_date)
                possible = False


def _repo_count_exceeded(out_file, api_token, stars, lang, current_date, cursor, possible, cur_size):
    _my_print("Repo count exceeded; searching for smaller scope ...")
    if cur_size[0] == ">":
        new_size = cur_size[1:] + ".." + str(int(cur_size[1:]) + 100)
        _iterate_over_pages_and_append_file(out_file, api_token, stars, lang, new_size, possible, current_date, cursor)
        new_size = ">" + str(int(cur_size[1:]) + 100)
        _iterate_over_pages_and_append_file(out_file, api_token, stars, lang, new_size, possible, current_date, cursor)
    elif cur_size[0] == "<":
        new_size = str(int(cur_size[1:]) - 100) + ".." + cur_size[1:]
        _iterate_over_pages_and_append_file(out_file, api_token, stars, lang, new_size, possible, current_date, cursor)
        new_size = "<" + str(int(cur_size[1:]) - 100)
        _iterate_over_pages_and_append_file(out_file, api_token, stars, lang, new_size, possible, current_date, cursor)
    else:
        split = cur_size.split("..")
        upper_limit = int(split[1])
        lower_limit = int(split[0])
        mid_limit = int((upper_limit + lower_limit) / 2)
        new_size = str(lower_limit) + ".." + str(mid_limit)
        _iterate_over_pages_and_append_file(out_file, api_token, stars, lang, new_size, possible, current_date, cursor)
        new_size = str(mid_limit) + ".." + str(upper_limit)
        _iterate_over_pages_and_append_file(out_file, api_token, stars, lang, new_size, possible, current_date, cursor)
    repo_count_exceed_case_dates.append(current_date)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-token', dest='api_token', required=True,
                        help='GitHub API token or Personal Access Token')
    parser.add_argument('--out-file', dest='out_file', required=True,
                        help='Output file path')
    parser.add_argument('--start-date', dest='start_date', required=True,
        type=lambda s: datetime.datetime.strptime(s, '%d-%m-%Y'),
                        help='Start date for search in dd-mm-yyyy')
    parser.add_argument('--lang', dest='lang', default='Java',
                        help='Primary programming language of the repositories')
    parser.add_argument('--min-stars', dest='stars', default=0, type=int,
                        help='Minimum star count')
    parser.add_argument('--verbose', dest='verbose', action='store_true')
    return parser.parse_args()


def search_repo(start_date, out_file, api_token, stars, lang, verbose=False):
    _my_print('Starting the repository search ...')
    current_date = start_date
    is_verbose = verbose
    while not current_date > datetime.datetime.now().date():
        _my_print("Processing search for date: " + str(current_date))
        possible = True
        cursor = ""
        size = ">" + MIN_REPO_SIZE  # Default limit can be set here
        _iterate_over_pages_and_append_file(out_file, api_token, stars, lang, size, possible, current_date, cursor)
        current_date = (current_date + datetime.timedelta(days=1))
    _my_print('Done.')


if __name__ == "__main__":
    args = parse_arguments()
    global is_verbose
    is_verbose = args.verbose
    search_repo(args.start_date.date(), args.out_file, args.api_token, args.stars, args.lang)


# GitHubApi567-hw3a

Takes a GitHub user ID and prints each repo name with the number of commits.

Run locally:


Tester’s perspective:
Network calls are isolated so tests mock requests.get. Output formatting is a pure function to assert exact text. Tests cover happy paths and a 404 error. Pagination is ignored per the assignment’s simple “count the returned list” rule.

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/lakshyaveg/GitHubApi567-hw3a/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/lakshyaveg/GitHubApi567-hw3a/tree/main)

# brycekage's LLM
![doctests](https://github.com/brycekage/Python-LLM/actions/workflows/doctests.yml/badge.svg)
![integration-tests](https://github.com/brycekage/Python-LLM/actions/workflows/integration-tests.yml/badge.svg)
![flake8](https://github.com/brycekage/Python-LLM/actions/workflows/flake8.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/cmc-csci040-brycekage-pythonllm)](https://pypi.org/project/cmc-csci040-brycekage-pythonllm/)
[![codecov](https://codecov.io/gh/brycekage/Python-LLM/branch/agents/graph/badge.svg)](https://codecov.io/gh/brycekage/Python-LLM)

An AI-powered terminal chat agent that lets you explore and query local files using natural language, powered by Groq.

## Examples

![demo](LLMEXAMPLE2.gif)

This example shows how the agent can look at other files in the directory

```
$ cd test_projects/brycekage.github.io
$ chat
chat> /ls

chat> Tell me about these files

```

This example shows how the agent cant read the content of files in a folder (ex: README.md) and return a summary

```
$ cd test_projects/markdown-compiler
$ chat
chat> what does this project do
This project is a Markdown to HTML compiler. It can convert Markdown files to HTML, and also includes an option to add CSS formatting. The compiler can be used from the command line, and it supports basic usage as well as the addition of CSS with the --add_css flag.
```

This example shows how the agent can read and output specific details about the project, such as Python libraries

```
$ cd testProjects/ebayWebscraper
$ chat
chat> /cat ebay-dl.py
chat> what python imports does this project use
The project uses the following Python imports:

- `argparse`
- `json`
- `csv`
- `playwright.sync_api`
- `bs4`
- `undetected_playwright`
```

This example shows how you can create, edit, remove, and commit files using the chat

```
$ chat
chat> can you create a hello.txt file and write "hello world" in it
The `hello.txt` file has been added and the changes have been committed.
chat> can you remove the hello.txt file
The `hello.txt` file has been removed and the changes have been committed.

```

# brycekage's LLM
![doctests](https://github.com/brycekage/Python-LLM/actions/workflows/doctests.yaml/badge.svg)
![integration-tests](https://github.com/brycekage/Python-LLM/actions/workflows/integration-tests.yaml/badge.svg)
![flake8](https://github.com/brycekage/Python-LLM/actions/workflows/flake8.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/cmc-csci040-brycekage-pythonllm/0.1.2/)](https://pypi.org/project/cmc-csci040-brycekage-pythonllm/0.1.2/)
[![codecov](https://codecov.io/gh/brycekage/Python-LLM/branch/main/graph/badge.svg)](https://codecov.io/gh/brycekage/Python-LLM)

An AI LLM chat REPL powered by Groq operated through the terminal 

Install with `pip install cmc-csci040-brycekage-pythonllm==0.1.2`

## Usage of the LLM

### Running Example

![Demo](output.gif)

### Slash Commands


Any tool name that starts with '/' will run directly.


`/ls` should give you all the files in a specific folder:
```
chat> /ls tools
tools/calculate.py tools/cat.py tools/grep.py tools/ls.py tools/screenshot.png tools/utils.py
chat> what files are in the tools folder?
The files in the tools folder are: calculate.py, cat.py, compact.py, grep.py, ls.py, and safehelp.py.
```

`/calculate` should give you the answers to math expressions:
```
chat> /calculate 2*6
12
```

`/grep` searches your codebase with regex and feeds the output into the conversation:
```
chat> /grep ^def test_projects/project001/markdown_compiler/__main__.py
def main():
```

`/cat` returns the raw files:
```
chat> /cat tools/calculate.py
def calculate(self):
    """
    Evaluate a mathematical expression.
...
```

`/compact` summarizes the entire conversation:
```

```

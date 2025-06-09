import re
import requests
from config import GEMINI_API_KEY

PY_KEYWORDS = [
    # Core syntax & types
    "python", "int", "float", "str", "bool", "complex", "bytes", "bytearray", "memoryview", "None",
    "list", "tuple", "dict", "set", "frozenset", "range", "slice",
    "variable", "constant", "assignment", "expression", "statement",

    # Operators
    "and", "or", "not", "is", "in", "not in", "==", "!=", "<", ">", "<=", ">=",
    "+", "-", "*", "/", "//", "%", "**", "|", "&", "^", "~", "<<", ">>",

    # Control flow
    "if", "elif", "else", "match", "case", "for", "while", "break", "continue", "pass",

    # Functions
    "def", "return", "lambda", "yield", "global", "nonlocal", "del", "assert",

    # Classes & OOP
    "class", "object", "self", "__init__", "super", "inheritance", "polymorphism",
    "encapsulation", "abstraction", "__str__", "__repr__", "__len__", "__getitem__",
    "__setitem__", "__delitem__", "__call__", "__iter__", "__next__",

    # Error handling
    "try", "except", "finally", "raise", "BaseException", "Exception", "ValueError", "TypeError",
    "KeyError", "IndexError", "AttributeError", "ZeroDivisionError", "ImportError", "NameError",

    # Iterators & Generators
    "iterator", "iter", "next", "StopIteration", "generator", "yield", "send",

    # Asynchronous programming
    "async", "await", "asyncio", "Task", "Future", "event loop", "concurrent", "threading", "multiprocessing",

    # Built-in functions
    "print", "input", "len", "range", "map", "filter", "reduce", "zip", "enumerate",
    "sorted", "reversed", "max", "min", "sum", "abs", "round", "pow", "all", "any",
    "id", "type", "isinstance", "callable", "dir", "vars", "help", "exec", "eval", "compile",

    # File handling
    "open", "read", "write", "close", "with", "seek", "tell", "file", "encoding", "text", "binary",

    # Environment & packaging
    "pip", "venv", "virtualenv", "requirements", "setup.py", "pyproject.toml", "build", "install", "uninstall",

    # CLI & arguments
    "argparse", "sys.argv", "click", "fire", "optparse", "getopt",

    # Logging & debugging
    "logging", "debug", "info", "warning", "error", "critical", "traceback", "pdb", "breakpoint",

    # Static typing
    "typing", "TypeVar", "Generic", "List", "Dict", "Tuple", "Union", "Optional", "Literal", "Protocol", "mypy", "pyright",

    # Testing
    "unittest", "pytest", "doctest", "mock", "patch", "fixture", "assertRaises",

    # Data structures
    "collections", "deque", "Counter", "defaultdict", "OrderedDict", "namedtuple", "ChainMap",
    "heapq", "queue", "PriorityQueue",

    # Date and time
    "datetime", "date", "time", "calendar", "timedelta", "timezone", "pytz",

    # Regex
    "re", "match", "search", "findall", "sub", "compile", "pattern", "group",

    # OS & system
    "os", "sys", "platform", "shutil", "glob", "pathlib", "getcwd", "listdir", "walk",

    # Subprocesses
    "subprocess", "Popen", "run", "call", "PIPE", "check_output",

    # JSON & data
    "json", "csv", "xml", "yaml", "pickle", "marshal", "configparser",

    # Math and statistics
    "math", "cmath", "statistics", "random", "decimal", "fractions", "factorial", "sqrt", "pi", "e",

    # Functional programming
    "functools", "partial", "reduce", "lru_cache", "wraps", "itertools", "product", "permutations", "combinations", "chain",

    # Web frameworks
    "flask", "django", "fastapi", "jinja2", "tornado", "bottle", "cherrypy", "uvicorn", "gunicorn", "starlette",

    # Web scraping
    "requests", "httpx", "urllib", "beautifulsoup", "bs4", "selenium", "scrapy", "mechanize", "lxml",

    # APIs
    "rest", "api", "http", "json", "get", "post", "put", "delete", "status_code", "jwt", "oauth",

    # Databases
    "sqlite3", "mysql", "postgresql", "sqlalchemy", "orm", "alembic", "peewee", "mongodb", "pymongo", "redis", "firebase",

    # Data science & ML
    "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly", "sklearn", "tensorflow", "keras", "pytorch",
    "xgboost", "lightgbm", "statsmodels", "labelencoder", "onehotencoder", "pipeline", "train_test_split",

    # Visualization
    "matplotlib", "seaborn", "plotly", "bokeh", "altair", "holoviews", "dash", "streamlit",

    # Notebooks
    "jupyter", "ipython", "nbconvert", "nbformat", "colab",

    # DevOps & CI
    "docker", "compose", "makefile", "github", "actions", "workflow", "lint", "black", "flake8", "prettier", "coverage", "tox",

    # Tools & IDEs
    "vscode", "pycharm", "thonny", "repl.it", "spyder", "idle", "anaconda", "poetry", "pipenv",

    # AI/LLM
    "openai", "chatgpt", "transformers", "langchain", "llama", "huggingface", "gemini", "bert", "gpt", "prompt", "embedding",

    # Misc
    "f-string", "format", "docstring", "comment", "PEP8", "refactor", "design pattern", "singleton", "factory"
]


def is_python_question(text: str) -> bool:
    text_low = text.lower()
    if any(kw in text_low for kw in PY_KEYWORDS):
        return True
    # Optional: AI-assisted classifier
    try:
        resp = requests.post("https://api.openai.com/v1/chat/completions", json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Reply strictly 'yes' or 'no' to whether the user's question is about Python programming."},
                {"role": "user", "content": text}
            ],
            "temperature": 0
        }, headers={"Authorization": f"Bearer {GEMINI_API_KEY}"})
        label = resp.json()["choices"][0]["message"]["content"].strip().lower()
        return label == "yes"
    except Exception:
        return False

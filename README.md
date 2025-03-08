# plover-python-dictionary-cmd

[![PyPI](https://img.shields.io/pypi/v/plover-python-dictionary-cmd?style=flat)](https://pypi.python.org/pypi/plover-python-dictionary-cmd/)

Execute arbitrary command from a Python dictionary.

**Warning**: While this plugin can do everything what a command plugin can, this should
only be used for personal usage. If the usage is sufficiently general, it's recommended to make
a Plover command plugin instead.

See also: [`plover-run-shell`](https://github.com/user202729/plover_run_shell), [`plover-run-py`](https://github.com/user202729/plover-run-py), [`plover-open-url`](https://github.com/user202729/plover-comment).

## What problem does this plugin solve?

First, this assumes you know what a [Python dictionary](https://github.com/openstenoproject/plover_python_dictionary) is.

Maybe you want to write a dictionary that looks like this:

```python
LONGEST_KEY = 1

def lookup(key):
    if key == ("SKWR-F",):
        return "{PLOVER:OPEN_URL:https://www.openstenoproject.org/}"
```

The `{PLOVER:OPEN_URL:…}` obviously opens the said URL, using [Plover Open URL plugin](https://github.com/nsmarkop/plover_open_url).

Problem: what if the task you want to do is not already covered by some command plugin?

While you can certainly write a new command plugin, that is rather time-consuming.

The following **will not work**:

```python
import webbrowser

LONGEST_KEY = 1

def lookup(key):
    if key == ("SKWR-F",):
        webbrowser.open("https://www.openstenoproject.org/")
```
It's because the dictionary may be looked up **multiple times**.

## The solution

Write the plugin like the following.

```python
import webbrowser
import plover_python_dictionary_cmd

LONGEST_KEY = 1

@plover_python_dictionary_cmd.register
def f(engine):
    webbrowser.open("https://www.openstenoproject.org/")

def lookup(key):
    if key == ("SKWR-F",):
        return str(f)  # or: f.str_with_args()
```

As an extra bonus, you get access to the `engine` object inside the function `f` above.

## Extra

`f.str_with_args()` works as follows:
`f.str_with_args(1, 2)` returns a string, which when interpreted as a Plover command
and executed, will call `f(engine, 1, 2)`.

As such, you can also modify the code above as follows:

```python
@plover_python_dictionary_cmd.register
def f(engine, url):
    webbrowser.open(url)

def lookup(key):
    if key == ("SKWR-F",):
        return f.str_with_args("https://www.openstenoproject.org/")
```

## Internal implementation detail

It uses a global lookup table to store the reference to the function `f`. Then `str(f)` as above
returns something like `{plover:python_dictionary_cmd:123456}` where `123456` is some unique ID.

Don't rely on this implementation detail.

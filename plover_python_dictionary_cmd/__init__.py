"""
Main file.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass
from base64 import b64decode, b64encode
from pickle import dumps, loads

if TYPE_CHECKING:
	from typing import Callable
	from plover.engine import StenoEngine  # type: ignore


lookup: dict[int, Callable[['StenoEngine'], None]] = {}  # may have memory leak

def cmd(engine: 'StenoEngine', id_: str)->None:
	"""
	Command function.
	"""
	if ":" in id_:
		id_, args = id_.split(":", maxsplit=1)
		args, kwargs = loads(b64decode(args))
		lookup[int(id_)](engine, *args, **kwargs)
	else:
		lookup[int(id_)](engine)


@dataclass
class register:
	func: Callable[['StenoEngine'], None]

	def __post_init__(self)->None:
		global lookup
		lookup[id(self.func)] = self.func

	def __call__(self, engine: 'StenoEngine')->None:
		self.func(engine)

	def __str__(self)->str:
		return "{plover:python_dictionary_cmd:" + str(id(self.func)) + "}"

	def __repr__(self)->str:
		return f"register({self.func})"

	def str_with_args(self, *args, **kwargs)->str:
		return "{plover:python_dictionary_cmd:" + str(id(self.func)) + ":" + b64encode(dumps((args, kwargs))).decode() + "}"

"""
Main file.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
	from typing import Callable
	from plover.engine import StenoEngine  # type: ignore


lookup: dict[int, Callable[['StenoEngine'], None]] = {}  # may have memory leak


def cmd(engine: 'StenoEngine', id_: str)->None:
	"""
	Command function.
	"""
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

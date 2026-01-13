"""Yasashii Anki - Japanese Dictionary Lookup Tool for Anki Card Creation

A CLI and GUI tool for looking up Japanese word definitions using JMDict
and automatically creating Anki flashcards with readings, meanings,
example sentences, and audio pronunciation.
"""

from .logging import ColorfulLogger, logger
from .japanese_word import JapaneseWord
from .anki_client import AnkiClient

__version__ = "0.1.0"
__author__ = "Yasashii Anki"

__all__ = ["ColorfulLogger", "logger", "JapaneseWord", "AnkiClient"]

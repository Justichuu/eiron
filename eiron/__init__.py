"""eiron: a decision engine for irony, and the paper it generates."""
from .engine import classify, summary, TRUE, FALSE, UNKNOWN  # noqa: F401
from .kinds import KINDS, QUESTIONS  # noqa: F401

__version__ = "0.1.0"

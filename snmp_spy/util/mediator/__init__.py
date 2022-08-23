"""Exposes base classes, mediator class (:class:`Mediator`),
and a global instance of a mediator
"""
from .base_classes import Handler, Request, Response
from .mediator import Mediator

__all__ = ["Request", "Handler", "Response", "Mediator", "mediator"]

mediator = Mediator()

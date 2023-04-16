"""
Дата классы
"""
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class LinkA:
    """
    Дата класс Link, используется совместно с Schema при сериализация данных
    """

    href: str
    title: str

from abc import ABC, abstractmethod


class Shape(ABC):
    """
    Abstract base class for geometric shapes
    """

    @abstractmethod
    def area(self):
        pass
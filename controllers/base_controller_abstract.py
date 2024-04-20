from flask import views
from abc import ABC, abstractmethod

class BaseController(views.MethodView, ABC):
    @abstractmethod
    def get(self):
        """Retrieve resources."""
        pass

    @abstractmethod
    def post(self):
        """Create or update resources."""
        pass

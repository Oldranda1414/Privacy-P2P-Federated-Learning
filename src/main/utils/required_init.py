def requires_initialization(method):
    """Decorator to ensure object is initialized before calling method"""
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_initialized') or not self._initialized:
            raise RuntimeError(f"{self.__class__.__name__} must be initialized before calling {method.__name__}()")
        return method(self, *args, **kwargs)
    return wrapper

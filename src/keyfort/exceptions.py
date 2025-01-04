class NotCreatedException(Exception):
    def __init__(self):
        super().__init__("Error creating secret")


class NotFoundException(Exception):
    def __init__(self):
        super().__init__("Error fetching entity")


class DuplicateEntityException(Exception):
    def __init__(self):
        super().__init__("Entity under provided name already exists")
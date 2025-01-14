class NotCreatedException(Exception):
    def __init__(self):
        super().__init__("Error creating secret")


class NotFoundException(Exception):
    def __init__(self):
        super().__init__("Error fetching entity")


class DuplicateEntityException(Exception):
    def __init__(self, msg: str):
        super().__init__("Duplicate entity error: {}".format(msg))

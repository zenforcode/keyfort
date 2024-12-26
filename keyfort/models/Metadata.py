import time


class Metadata():
    def __init__(self, is_active: bool = True, created_at: str = time.time(), updated_at: str = time.time()):
        self.is_active = True
        self.created_at = time.time()
        self.updated_at = None

    def deactivate(self):
        self.is_active = False
        return self

    def updateTimestamp(self):
        self.updated_at = time.time()
        return self

    def __str__(self):
        return "is_active:" + self.is_active + "\ncreated_at:" + self.created_at + "\nupdated_at:" + self.updated_at

    def __repr__(self):
        return "is_active:" + self.is_active + "\ncreated_at:" + self.created_at + "\nupdated_at:" + self.updated_at

class InvalidNodeDirectionError(Exception):
    def __init__(self):
        self.msg = 'Invalid node direction! Value must be "src" or "dst".'

    def __str__(self):
        return repr(self.msg)

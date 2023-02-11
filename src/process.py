class Process:
    def __init__(self, output=None, **kwargs):
        self.args = kwargs['args']
        self.response = None
        self.error = None
        self.return_code = None

    @property
    def return_code(self):
        return self.return_code

    @property
    def response(self):
        return self.response

    @property
    def error(self):
        return self.error
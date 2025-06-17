class RequestError(Exception):
    """Custom exception for detailed request errors."""
    def __init__(self, message, line_number=None, context=None, file_name=None):
        self.message = message
        self.line_number = line_number
        self.context = context
        self.file_name = file_name
        super().__init__(self.message)

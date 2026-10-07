class ErrorTracker:
    def __init__(self):
        self.errors = []

    def record_error(self, error_type, message, line):
        self.errors.append({
            "type": error_type,
            "message": message,
            "line": line
        })

    def get_errors(self):
        return self.errors

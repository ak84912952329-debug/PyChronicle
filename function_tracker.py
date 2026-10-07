class FunctionTracker:
    def __init__(self):
        self.events = []

    def record_call(self, function_name, line):
        self.events.append({
            "type": "call",
            "function": function_name,
            "line": line
        })

    def record_return(self, function_name, line):
        self.events.append({
            "type": "return",
            "function": function_name,
            "line": line
        })

    def get_events(self):
        return self.events

from dataclasses import dataclass


@dataclass
class ExecutionState:
    step: int
    line: int
    function: str
    source: str
    variables: dict
    event: str = "line"
    error: dict = None


class History:
    def __init__(self):
        self.states = []
        self.current_index = -1

    def add(self, state):
        self.states.append(state)

    def get(self, index):
        if 0 <= index < len(self.states):
            return self.states[index]
        return None

    def previous(self):
        if self.current_index > 0:
            self.current_index -= 1
        return self.get(self.current_index)

    def next(self):
        if self.current_index < len(self.states) - 1:
            self.current_index += 1
        return self.get(self.current_index)

    def jump_to(self, index):
        if 0 <= index < len(self.states):
            self.current_index = index
            return self.states[index]
        return None

    def __len__(self):
        return len(self.states)

    def to_dict(self):
        return [state.__dict__ for state in self.states]

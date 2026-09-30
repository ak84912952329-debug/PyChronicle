
from dataclasses import dataclass


@dataclass
class ExecutionState:
    step: int
    line: int
    function: str
    source: str
    variables: dict


class History:
    def __init__(self):
        self.states = []

    def add(self, state):
        self.states.append(state)

    def get(self, index):
        return self.states[index]

    def __len__(self):
        return len(self.states)

    def to_dict(self):
        return [state.__dict__ for state in self.states]

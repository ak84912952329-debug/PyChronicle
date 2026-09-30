
import sys
import copy
import linecache

from .history import ExecutionState


class ExecutionTracer:
    def __init__(self):
        self.history = []
        self.step = 0

    def _trace(self, frame, event, arg):
        if event == "line":
            self.step += 1

            variables = {}

            for name, value in frame.f_locals.items():
                try:
                    variables[name] = copy.deepcopy(value)
                except Exception:
                    variables[name] = repr(value)

            source = linecache.getline(
                frame.f_code.co_filename,
                frame.f_lineno
            ).strip()

            state = ExecutionState(
                step=self.step,
                line=frame.f_lineno,
                function=frame.f_code.co_name,
                source=source,
                variables=variables
            )

            self.history.append(state)

        return self._trace

    def start(self):
        self.history = []
        self.step = 0
        sys.settrace(self._trace)

    def stop(self):
        sys.settrace(None)

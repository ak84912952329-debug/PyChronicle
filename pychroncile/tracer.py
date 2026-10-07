import sys
import copy
import linecache

from .history import ExecutionState, History
from .function_tracker import FunctionTracker
from .error_tracker import ErrorTracker


class ExecutionTracer:

    def __init__(self):
        self.history = History()
        self.function_tracker = FunctionTracker()
        self.error_tracker = ErrorTracker()
        self.step = 0

    def _snapshot(self, frame):
        variables = {}

        for name, value in frame.f_locals.items():
            try:
                variables[name] = copy.deepcopy(value)
            except Exception:
                variables[name] = repr(value)

        return variables

    def _trace(self, frame, event, arg):

        if event == "call":
            self.function_tracker.record_call(
                frame.f_code.co_name,
                frame.f_lineno
            )

        elif event == "line":
            self.step += 1

            source = linecache.getline(
                frame.f_code.co_filename,
                frame.f_lineno
            ).strip()

            state = ExecutionState(
                step=self.step,
                line=frame.f_lineno,
                function=frame.f_code.co_name,
                source=source,
                variables=self._snapshot(frame),
                event="line"
            )

            self.history.add(state)

        elif event == "return":
            self.function_tracker.record_return(
                frame.f_code.co_name,
                frame.f_lineno
            )

        elif event == "exception":
            exception_type, exception_value, _ = arg

            self.error_tracker.record_error(
                exception_type.__name__,
                str(exception_value),
                frame.f_lineno
            )

        return self._trace

    def start(self):
        sys.settrace(self._trace)

    def stop(self):
        sys.settrace(None)

    def get_history(self):
        return self.history

    def get_function_events(self):
        return self.function_tracker.get_events()

    def get_errors(self):
        return self.error_tracker.get_errors()

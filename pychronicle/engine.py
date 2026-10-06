
import runpy
import sys

from .ast_analyzer import ASTAnalyzer
from .tracer import ExecutionTracer
from .history import History


class PyChronicle:
    def __init__(self, source_file):
        self.source_file = source_file
        self.history = History()

    def analyze_source(self):
        with open(self.source_file, "r", encoding="utf-8") as file:
            source_code = file.read()

        analyzer = ASTAnalyzer(source_code)
        return analyzer.analyze()

    def run(self):
        tracer = ExecutionTracer()

        tracer.start()

        try:
            runpy.run_path(self.source_file, run_name="__main__")
        finally:
            tracer.stop()

        for state in tracer.history:
            self.history.add(state)

        return self.history

    def summary(self):
        return {
            "source_file": self.source_file,
            "execution_states": len(self.history),
        }

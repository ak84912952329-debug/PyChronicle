from .ast_analyzer import ASTAnalyzer
from .tracer import ExecutionTracer


class PyChronicle:
    def __init__(self):
        self.ast_analyzer = ASTAnalyzer()
        self.tracer = ExecutionTracer()

    def analyze(self, source):
        return self.ast_analyzer.analyze(source)

    def run(self, source, filename="<string>"):
        analysis = self.analyze(source)

        self.tracer.start()

        try:
            code = compile(source, filename, "exec")
            exec(code, {})
        finally:
            self.tracer.stop()

        return {
            "analysis": analysis,
            "history": self.tracer.get_history(),
            "function_events": self.tracer.get_function_events(),
            "errors": self.tracer.get_errors()
        }

    def get_history(self):
        return self.tracer.get_history()

    def get_function_events(self):
        return self.tracer.get_function_events()

    def get_errors(self):
        return self.tracer.get_errors()

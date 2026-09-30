from pychronicle.engine import PyChronicle


def main():
    source_file = "examples/sample.py"

    debugger = PyChronicle(source_file)

    print("=" * 50)
    print("       PyChronicle - Time-Travel Debugger")
    print("=" * 50)

    # AST analysis
    statements = debugger.analyze_source()

    print("\nAST Analysis:")
    print(f"Total statements: {len(statements)}")

    for statement in statements:
        print(
            f"Line {statement['line']}: "
            f"{statement['type']}"
        )

    # Execute program and record states
    print("\nProgram Output:")
    history = debugger.run()

    print("\nExecution History:")

    for state in history.states:
        print(
            f"Step {state.step} | "
            f"Line {state.line} | "
            f"{state.source}"
        )

        print(f"Variables: {state.variables}")

    print("\n" + "=" * 50)
    print("Total execution states:", len(history))
    print("=" * 50)


if __name__ == "__main__":
    main()

from pychronicle.engine import PyChronicle


def main():
    source_file = "examples/sample.py"

    debugger = PyChronicle(source_file)

    print("=" * 55)
    print("       PyChronicle - Time-Travel Debugger")
    print("=" * 55)

    # AST Analysis
    statements = debugger.analyze_source()

    print("\nAST Analysis")
    print("-" * 30)
    print(f"Total statements: {len(statements)}")

    for statement in statements:
        print(
            f"Line {statement['line']}: "
            f"{statement['type']}"
        )

    # Run program and record execution states
    print("\nProgram Output")
    print("-" * 30)

    history = debugger.run()

    print("\nExecution History")
    print("-" * 30)

    for state in history.states:
        print(
            f"Step {state.step} | "
            f"Line {state.line} | "
            f"{state.source}"
        )
        print(f"Variables: {state.variables}")

    # Time-travel navigation
    print("\nTime-Travel Navigation")
    print("-" * 30)

    first_state = history.jump_to(0)

    if first_state:
        print(
            f"Jump to Step {first_state.step}: "
            f"{first_state.source}"
        )

    next_state = history.next()

    if next_state:
        print(
            f"Next Step {next_state.step}: "
            f"{next_state.source}"
        )

    previous_state = history.previous()

    if previous_state:
        print(
            f"Previous Step {previous_state.step}: "
            f"{previous_state.source}"
        )

    print("\n" + "=" * 55)
    print(f"Total execution states: {len(history)}")
    print("=" * 55)


if __name__ == "__main__":
    main()

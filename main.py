from pychronicle.engine import PyChronicle


def main():
    source_file = "examples/sample.py"

    with open(source_file, "r", encoding="utf-8") as f:
        source = f.read()

    debugger = PyChronicle()

    print("=" * 55)
    print("       PyChronicle - Time-Travel Debugger")
    print("=" * 55)

    # AST Analysis
    statements = debugger.analyze(source)

    print("\nAST Analysis")
    print("-" * 30)
    print(f"Total statements: {len(statements)}")

    for statement in statements:
        print(
            f"Line {statement.line}: "
            f"{statement.kind} - {statement.source}"
        )

    # Run program
    print("\nProgram Output")
    print("-" * 30)

    result = debugger.run(source, source_file)
    history = result["history"]

    # Execution History
    print("\nExecution History")
    print("-" * 30)

    for state in history.states:
        print(
            f"Step {state.step} | "
            f"Line {state.line} | "
            f"{state.source}"
        )
        print(f"Variables: {state.variables}")

    # Function tracking
    print("\nFunction Events")
    print("-" * 30)

    for event in result["function_events"]:
        print(
            f"{event['type'].upper()} | "
            f"{event['function']} | "
            f"Line {event['line']}"
        )

    # Error tracking
    print("\nErrors")
    print("-" * 30)

    if result["errors"]:
        for error in result["errors"]:
            print(
                f"{error['type']} | "
                f"Line {error['line']} | "
                f"{error['message']}"
            )
    else:
        print("No errors detected.")

    # Navigation
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

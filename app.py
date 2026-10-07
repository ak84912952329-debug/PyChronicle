import streamlit as st

from pychronicle.tracer import ExecutionTracer


st.set_page_config(
    page_title="PyChronicle",
    page_icon="⏪"
)

st.title("PyChronicle")
st.subheader("AST-Powered Time-Travel Debugger")


# Store execution history in session state
if "user_history" not in st.session_state:
    st.session_state.user_history = []


source_code = st.text_area(
    "Enter Python Code",
    """x = 10
y = 20
z = x + y
z = z * 2
print(z)
""",
    height=250
)


col1, col2 = st.columns(2)

with col1:
    run_program = st.button("Run Program")

with col2:
    clear_results = st.button("Clear Results")


# Clear previous results
if clear_results:
    st.session_state.user_history = []
    st.rerun()


if run_program:

    if not source_code.strip():
        st.warning("Please enter some Python code.")

    else:
        tracer = ExecutionTracer()

        try:
            namespace = {}

            compiled_code = compile(
                source_code,
                "<user_code>",
                "exec"
            )

            tracer.start()

            exec(compiled_code, namespace)

            tracer.stop()

            st.success("Program executed successfully.")

            # Remove internal tracer states
            user_history = [
                state for state in tracer.history
                if state.function == "<module>"
            ]

            # Save history in session state
            st.session_state.user_history = user_history

        except Exception as error:

            tracer.stop()

            st.error(f"Program error: {error}")

            st.session_state.user_history = []


# Display previous execution results
user_history = st.session_state.user_history


if user_history:

    # Execution summary
    st.subheader("Execution Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Steps",
            len(user_history)
        )

    with col2:
        st.metric(
            "Variables Captured",
            len([
                name
                for name in user_history[-1].variables
                if name != "__builtins__"
            ])
        )

    # Final variable state
    st.subheader("Final Variable State")

    final_variables = {
        name: value
        for name, value in user_history[-1].variables.items()
        if name != "__builtins__"
    }

    st.write(final_variables)

    # Execution history
    st.subheader("Execution History")

    for state in user_history:

        st.write(
            f"**Step {state.step}** | "
            f"Line {state.line} | "
            f"Function: `{state.function}`"
        )

        st.code(state.source)

        user_variables = {
            name: value
            for name, value in state.variables.items()
            if name != "__builtins__"
        }

        st.write("Variables:", user_variables)

        st.divider()

else:
    st.info("No execution results available.")
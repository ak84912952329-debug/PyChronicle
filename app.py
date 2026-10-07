import streamlit as st

from pychronicle.tracer import ExecutionTracer


st.set_page_config(
    page_title="PyChronicle",
    page_icon="⏪"
)

st.title("PyChronicle")
st.subheader("AST-Powered Time-Travel Debugger")


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


if st.button("Run Program"):

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
                    if user_history
                    else 0
                )

            # Final variable state
            st.subheader("Final Variable State")

            if user_history:
                final_variables = {
                    name: value
                    for name, value in user_history[-1].variables.items()
                    if name != "__builtins__"
                }

                st.write(final_variables)

            else:
                st.info("No variables were captured.")

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

        except Exception as error:

            tracer.stop()

            st.error(f"Program error: {error}")
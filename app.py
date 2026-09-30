import streamlit as st

from tracer import ExecutionTracer


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

            st.subheader("Execution History")

            for state in tracer.history:

                st.write(
                    f"**Step {state.step}** | "
                    f"Line {state.line} | "
                    f"Function: `{state.function}`"
                )

                st.code(state.source)

                st.write("Variables:", state.variables)

                st.divider()

        except Exception as error:

            tracer.stop()

            st.error(f"Program error: {error}")
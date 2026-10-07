import streamlit as st

from pychronicle.tracer import ExecutionTracer


st.set_page_config(
    page_title="PyChronicle",
    page_icon="⏪"
)

st.title("PyChronicle")
st.subheader("AST-Powered Time-Travel Debugger")


# Store execution history
if "user_history" not in st.session_state:
    st.session_state.user_history = []

if "selected_step" not in st.session_state:
    st.session_state.selected_step = 1


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


# Clear results
if clear_results:
    st.session_state.user_history = []
    st.session_state.selected_step = 1

    if "execution_step_slider" in st.session_state:
        del st.session_state.execution_step_slider

    st.rerun()


# Run program
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

            # Keep only user program states
            user_history = [
                state
                for state in tracer.history
                if state.function == "<module>"
            ]

            st.session_state.user_history = user_history

            # Start from first step
            st.session_state.selected_step = 1

            if "execution_step_slider" in st.session_state:
                del st.session_state.execution_step_slider

        except Exception as error:

            tracer.stop()

            st.error(f"Program error: {error}")

            st.session_state.user_history = []
            st.session_state.selected_step = 1


# Get history
user_history = st.session_state.user_history


if user_history:

    total_steps = len(user_history)


    # Make sure selected step is valid
    if st.session_state.selected_step < 1:
        st.session_state.selected_step = 1

    if st.session_state.selected_step > total_steps:
        st.session_state.selected_step = total_steps


    # Execution summary
    st.subheader("Execution Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Steps",
            total_steps
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


    # Step navigation
    st.subheader("Step Navigation")


    col1, col2, col3 = st.columns(3)


    with col1:

        if st.button(
            "⬅ Previous Step",
            disabled=st.session_state.selected_step <= 1
        ):

            st.session_state.selected_step -= 1

            # Update slider state
            st.session_state.execution_step_slider = (
                st.session_state.selected_step
            )

            st.rerun()


    with col2:

        st.write(
            f"**Current Step: "
            f"{st.session_state.selected_step} / "
            f"{total_steps}**"
        )


    with col3:

        if st.button(
            "Next Step ➡",
            disabled=st.session_state.selected_step >= total_steps
        ):

            st.session_state.selected_step += 1

            # Update slider state
            st.session_state.execution_step_slider = (
                st.session_state.selected_step
            )

            st.rerun()


    # Step slider
    selected_step = st.slider(
        "Select execution step",
        min_value=1,
        max_value=total_steps,
        value=st.session_state.selected_step,
        key="execution_step_slider"
    )


    # Save slider selection
    st.session_state.selected_step = selected_step


    # Selected state
    selected_state = user_history[
        st.session_state.selected_step - 1
    ]


    # Selected step details
    st.write(
        f"### Step {selected_state.step}"
    )

    st.write(
        f"**Line:** {selected_state.line}"
    )

    st.write(
        f"**Function:** `{selected_state.function}`"
    )


    st.write("**Source Code:**")

    st.code(selected_state.source)


    # Variables at selected step
    selected_variables = {
        name: value
        for name, value in selected_state.variables.items()
        if name != "__builtins__"
    }

    st.write("**Variables at this step:**")

    st.write(selected_variables)


    # Complete execution history
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
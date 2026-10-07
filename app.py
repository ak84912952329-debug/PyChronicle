import streamlit as st

from pychronicle.tracer import ExecutionTracer


st.set_page_config(
    page_title="PyChronicle",
    page_icon="⏪"
)

st.title("PyChronicle")
st.subheader("AST-Powered Time-Travel Debugger")
# Session State

if "user_history" not in st.session_state:
    st.session_state.user_history = []

if "selected_step" not in st.session_state:
    st.session_state.selected_step = 1

# Source Code Input

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

# Program Controls

col1, col2 = st.columns(2)

with col1:
    run_program = st.button("Run Program")

with col2:
    clear_results = st.button("Clear Results")

# Clear Results

if clear_results:

    st.session_state.user_history = []
    st.session_state.selected_step = 1

    if "execution_step_slider" in st.session_state:
        del st.session_state.execution_step_slider

    st.rerun()

# Run Program

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

            # Save execution history
            st.session_state.user_history = user_history

            # Start navigation from first step
            st.session_state.selected_step = 1

            # Reset slider widget
            if "execution_step_slider" in st.session_state:
                del st.session_state.execution_step_slider

        except Exception as error:

            tracer.stop()

            st.error(f"Program error: {error}")

            st.session_state.user_history = []
            st.session_state.selected_step = 1

# Get Execution History

user_history = st.session_state.user_history


if user_history:

    total_steps = len(user_history)

    # Validate Selected Step

    if st.session_state.selected_step < 1:
        st.session_state.selected_step = 1

    if st.session_state.selected_step > total_steps:
        st.session_state.selected_step = total_steps

    # Execution Summary

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

    # Final Variable State

    st.subheader("Final Variable State")

    final_variables = {
        name: value
        for name, value in user_history[-1].variables.items()
        if name != "__builtins__"
    }

    st.write(final_variables)

    # Step Navigation

    st.subheader("Step Navigation")

    # Execution Progress

    progress = (
        st.session_state.selected_step / total_steps
    )

    st.progress(
        progress,
        text=(
            f"Execution Progress: "
            f"Step {st.session_state.selected_step} "
            f"of {total_steps}"
        )
    )

    # Previous / Current / Next

    col1, col2, col3 = st.columns(3)


    with col1:

        if st.button(
            "⬅ Previous Step",
            disabled=st.session_state.selected_step <= 1
        ):

            st.session_state.selected_step -= 1

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

            st.rerun()
    # Step Slider

    selected_step = st.slider(
        "Select execution step",
        min_value=1,
        max_value=total_steps,
        value=st.session_state.selected_step
    )

    # Update selected step
    st.session_state.selected_step = selected_step

    # Selected State

    selected_state = user_history[
        st.session_state.selected_step - 1
    ]

    # Selected Step Details

    st.write(
        f"### Step {selected_state.step}"
    )

    st.write(
        f"**Line:** {selected_state.line}"
    )

    st.write(
        f"**Function:** `{selected_state.function}`"
    )

    # Source Code

    st.write("**Source Code:**")

    st.code(selected_state.source)

    # Variables at Selected Step

    selected_variables = {
        name: value
        for name, value in selected_state.variables.items()
        if name != "__builtins__"
    }

    st.write("**Variables at this step:**")

    st.write(selected_variables)

    # Complete Execution History

    st.subheader("Execution History")


    for state in user_history:

        # Highlight current step
        if state.step == st.session_state.selected_step:

            st.success(
                f"Currently Viewing — Step {state.step}"
            )

        else:

            st.write(
                f"**Step {state.step}**"
            )


        st.write(
            f"Line {state.line} | "
            f"Function: `{state.function}`"
        )

        st.code(state.source)


        user_variables = {
            name: value
            for name, value in state.variables.items()
            if name != "__builtins__"
        }

        st.write(
            "Variables:",
            user_variables
        )

        st.divider()


else:

    st.info("No execution results available.")
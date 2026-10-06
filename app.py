import traceback

import streamlit as st

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from agent.hr_agent import (
    build_hr_agent,
    set_authenticated_employee
)

from services.auth_service import (
    authenticate_employee
)

from services.security_service import (
    security_check
)

from services.output_security import (
    sanitize_response
)

from services.security_logger import (
    log_security_event
)


# ============================================================
# Streamlit configuration
# ============================================================

st.set_page_config(
    page_title="HR Chat Agent",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# Session state
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "employee_id" not in st.session_state:
    st.session_state.employee_id = None

if "employee_name" not in st.session_state:
    st.session_state.employee_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "hr_agent" not in st.session_state:
    st.session_state.hr_agent = None

if "last_trace" not in st.session_state:
    st.session_state.last_trace = []


# ============================================================
# Agent
# ============================================================

def get_hr_agent():

    if st.session_state.hr_agent is None:

        st.session_state.hr_agent = (
            build_hr_agent()
        )

    return st.session_state.hr_agent


# ============================================================
# Login
# ============================================================

def show_login():

    st.title("🤖 HR Chat Agent")

    st.subheader(
        "Employee Login"
    )

    st.write(
        "Login to interact with the HR Chat Agent "
        "using your employee account."
    )

    with st.form("login_form"):

        employee_id = st.text_input(
            "Employee ID",
            placeholder="Example: EMP1001"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        login_clicked = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    if login_clicked:

        employee_id = (
            employee_id
            .strip()
            .upper()
        )

        if not employee_id or not password:

            st.error(
                "Please enter Employee ID and password."
            )

            return

        employee = authenticate_employee(
            employee_id,
            password
        )

        if employee is None:

            st.error(
                "Invalid Employee ID or password."
            )

            return

        st.session_state.authenticated = True

        st.session_state.employee_id = (
            employee["employee_id"]
        )

        st.session_state.employee_name = (
            employee["name"]
        )

        st.session_state.messages = []

        st.session_state.hr_agent = None

        st.session_state.last_trace = []

        st.rerun()


# ============================================================
# Sidebar
# ============================================================

def show_sidebar():

    with st.sidebar:

        st.header("👤 Employee")

        st.write(
            f"**Name:** "
            f"{st.session_state.employee_name}"
        )

        st.write(
            f"**Employee ID:** "
            f"{st.session_state.employee_id}"
        )

        st.divider()

        st.subheader(
            "💡 Try asking"
        )

        st.caption(
            "What is my leave balance?"
        )

        st.caption(
            "What is the work from home policy?"
        )

        st.caption(
            "What is my joining date?"
        )

        st.caption(
            "Can I take 5 days casual leave next week?"
        )

        st.caption(
            "How many working days are there "
            "between October 5 and October 12?"
        )

        st.divider()

        if st.button(
            "🗑️ Clear Conversation",
            use_container_width=True
        ):

            st.session_state.messages = []

            st.session_state.last_trace = []

            st.rerun()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.authenticated = False

            st.session_state.employee_id = None

            st.session_state.employee_name = None

            st.session_state.messages = []

            st.session_state.hr_agent = None

            st.session_state.last_trace = []

            st.rerun()


# ============================================================
# Display conversation
# ============================================================

def display_messages():

    for message in st.session_state.messages:

        role = message["role"]

        content = message["content"]

        with st.chat_message(role):

            st.markdown(content)


# ============================================================
# Convert Streamlit messages to LangChain messages
# ============================================================

def build_conversation_messages():

    conversation_messages = []

    for message in st.session_state.messages:

        if message["role"] == "user":

            conversation_messages.append(
                HumanMessage(
                    content=message["content"]
                )
            )

        elif message["role"] == "assistant":

            conversation_messages.append(
                AIMessage(
                    content=message["content"]
                )
            )

    return conversation_messages


# ============================================================
# Extract final response
# ============================================================

def extract_response(result):

    if not result:

        return (
            "I couldn't generate a response "
            "for your request."
        )

    messages = result.get(
        "messages",
        []
    )

    if not messages:

        return (
            "I couldn't generate a response "
            "for your request."
        )

    final_message = None

    for message in reversed(messages):

        if isinstance(
            message,
            AIMessage
        ):

            tool_calls = getattr(
                message,
                "tool_calls",
                None
            )

            if not tool_calls:

                final_message = message

                break

    if final_message is None:

        final_message = messages[-1]

    response = final_message.content

    # Gemini can return structured content
    if isinstance(
        response,
        list
    ):

        text_parts = []

        for item in response:

            if isinstance(
                item,
                dict
            ):

                if "text" in item:

                    text_parts.append(
                        str(item["text"])
                    )

            elif isinstance(
                item,
                str
            ):

                text_parts.append(item)

        if text_parts:

            return "\n".join(
                text_parts
            )

        return str(response)

    return str(response)


# ============================================================
# Agent trace
# ============================================================

def show_agent_trace():

    trace = st.session_state.get(
        "last_trace",
        []
    )

    if not trace:

        return

    with st.expander(
        "🔍 Agent Trace",
        expanded=False
    ):

        for event in trace:

            status = event.get(
                "status",
                "success"
            )

            event_type = event.get(
                "event_type",
                "EVENT"
            )

            message = event.get(
                "message",
                ""
            )

            timestamp = event.get(
                "timestamp",
                ""
            )

            if status == "success":

                icon = "🟢"

            elif status == "blocked":

                icon = "🔴"

            elif status == "error":

                icon = "❌"

            else:

                icon = "🟡"

            st.write(
                f"{icon} "
                f"`{timestamp}` "
                f"**{event_type}** — "
                f"{message}"
            )


# ============================================================
# Process question
# ============================================================

def process_question(question):

    question = question.strip()

    st.session_state.last_trace = []

    # --------------------------------------------------------
    # Security validation
    # --------------------------------------------------------

    allowed, security_message = (
        security_check(question)
    )

    if not allowed:

        log_security_event(
            st.session_state.employee_id,
            "Blocked potentially unsafe request"
        )

        st.session_state.last_trace = [

            {
                "timestamp": "",

                "event_type": "SECURITY",

                "message": (
                    "Request blocked by "
                    "security validation"
                ),

                "status": "blocked"
            }

        ]

        return security_message

    # --------------------------------------------------------
    # Build conversation
    # --------------------------------------------------------

    conversation_messages = (
        build_conversation_messages()
    )

    conversation_messages.append(
        HumanMessage(
            content=question
        )
    )

    # --------------------------------------------------------
    # Set authenticated employee
    # --------------------------------------------------------

    try:

        set_authenticated_employee(
            st.session_state.employee_id
        )

    except Exception as exc:

        st.session_state.last_trace = [

            {
                "timestamp": "",

                "event_type": "AUTH",

                "message": (
                    f"{type(exc).__name__}: "
                    f"{str(exc)}"
                ),

                "status": "error"
            }

        ]

        return (
            "Authenticated employee context "
            "could not be established."
        )

    # --------------------------------------------------------
    # Invoke agent
    # --------------------------------------------------------

    try:

        agent = get_hr_agent()

        result = agent.invoke(
            {
                "messages": conversation_messages,

                "trace": []
            }
        )

        st.session_state.last_trace = (
            result.get(
                "trace",
                []
            )
        )

        response = extract_response(
            result
        )

    except Exception as exc:

        # Print complete traceback
        # to PowerShell / terminal.
        traceback.print_exc()

        error_type = type(
            exc
        ).__name__

        error_message = str(
            exc
        )

        log_security_event(
            st.session_state.employee_id,
            "Agent processing error: "
            + error_type
        )

        st.session_state.last_trace.append(

            {
                "timestamp": "",

                "event_type": "ERROR",

                "message": (
                    f"{error_type}: "
                    f"{error_message}"
                ),

                "status": "error"
            }

        )

        # During development, show the actual
        # error in the UI.
        response = (
            f"### ❌ Agent Error\n\n"
            f"**Error:** `{error_type}`\n\n"
            f"**Details:** `{error_message}`\n\n"
            f"Please check the PowerShell terminal "
            f"for the complete traceback."
        )

    # --------------------------------------------------------
    # Output security
    # --------------------------------------------------------

    response = sanitize_response(
        response
    )

    return response


# ============================================================
# Chat
# ============================================================

def show_chat():

    st.title(
        "🤖 HR Chat Agent"
    )

    st.caption(
        "Your AI-powered employee HR assistant"
    )

    show_sidebar()

    display_messages()

    question = st.chat_input(
        "Ask your HR question..."
    )

    if question:

        question = question.strip()

        if not question:

            return

        # ----------------------------------------------------
        # User message
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message(
            "user"
        ):

            st.markdown(
                question
            )

        # ----------------------------------------------------
        # Agent response
        # ----------------------------------------------------

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "HR Agent is working..."
            ):

                response = process_question(
                    question
                )

            st.markdown(
                response
            )

        # ----------------------------------------------------
        # Store response
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        # ----------------------------------------------------
        # Trace
        # ----------------------------------------------------

        show_agent_trace()


# ============================================================
# Main
# ============================================================

def main():

    if not st.session_state.authenticated:

        show_login()

    else:

        show_chat()


# ============================================================
# Application entry point
# ============================================================

if __name__ == "__main__":

    main()
import streamlit as st
import time

# =====================================================================
# 1. Basic Agent Implementation
# =====================================================================
class BasicAgent:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        # Simple tool registry inside the agent
        self.tools = {
            "calculator": self._tool_calculator,
            "get_status": self._tool_status,
        }

    def _tool_calculator(self, expression: str) -> str:
        try:
            # Safe evaluation for basic math expressions
            allowed_chars = "0123456789+-*/(). "
            if all(char in allowed_chars for char in expression):
                result = eval(expression)
                return f"Calculation Result: {result}"
            return "Error: Invalid characters in math expression."
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"

    def _tool_status(self, system_name: str) -> str:
        return f"System '{system_name}' is operational (Uptime: 99.9%)."

    def process_message(self, user_input: str, history: list) -> str:
        """
        Processes user query, routes to tools if needed, and returns response.
        """
        query_lower = user_input.lower()

        # Tool Routing Logic
        if "calculate" in query_lower or "compute" in query_lower:
            expr = "".join([c for c in user_input if c in "0123456789+-*/(). "]).strip()
            if expr:
                tool_output = self.tools["calculator"](expr)
                return f"🤖 **[Tool Executed - Calculator]**\n\n{tool_output}"

        if "status of" in query_lower or "check system" in query_lower:
            system_name = user_input.split("status of")[-1].strip() or "Core Service"
            tool_output = self.tools["get_status"](system_name)
            return f"🤖 **[Tool Executed - System Check]**\n\n{tool_output}"

        # General Knowledge/Conversational Routing
        return (
            f"I processed your request using the `{self.name}` model setup.\n\n"
            f"You said: *\"{user_input}\"*\n\n"
            f"*(Context Memory: {len(history)} past messages in active session)*"
        )


# =====================================================================
# 2. Streamlit UI & Session Management
# =====================================================================
st.set_page_config(
    page_title="Agent Interface",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Basic Agent Integration")
st.caption("Streamlit UI powered by a custom Python Agent engine.")

# Sidebar Configuration
with st.sidebar:
    st.header("Agent Parameters")
    agent_name = st.text_input("Agent Name", value="AssistantBot")
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful and concise AI assistant.",
        height=100
    )
    
    if st.button("Clear Conversation", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# Initialize Agent
agent = BasicAgent(name=agent_name, system_prompt=system_prompt)

# Initialize Streamlit Session Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat history from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask something (e.g., 'calculate 25 * 4' or 'status of API Gateway')..."):
    # Render user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process and render agent response
    with st.chat_message("assistant"):
        with st.spinner("Agent is reasoning..."):
            time.sleep(0.4)  # Visual feedback delay
            response = agent.process_message(prompt, st.session_state.messages[:-1])
            st.markdown(response)

    # Persist assistant response in state
    st.session_state.messages.append({"role": "assistant", "content": response})
import streamlit as st
from agent import ask

st.set_page_config(page_title="SQL Chat Agent", page_icon="🗄️")
st.title("Ask your database anything")
st.caption("Powered by Groq + LangChain · Self-healing SQL agent")

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show example questions
with st.expander("Example questions to try"):
    st.markdown("""
- How many customers do we have?
- What are the top 5 most expensive products?
- How many orders were placed in total?
- Which city has the most customers?
- What is the average order quantity?
""")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "sql" in msg:
            with st.expander("SQL query used"):
                st.code(msg["sql"], language="sql")
        if "attempts" in msg and msg["attempts"] > 1:
            st.warning(f"Self-healed after {msg['attempts']} attempts")

# Chat input
if prompt := st.chat_input("Ask a question about your data..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = ask(prompt)

        st.write(result["answer"])

        with st.expander("SQL query used"):
            st.code(result["sql"], language="sql")

        if result["attempts"] > 1:
            st.warning(f"Self-healed: fixed the query after {result['attempts']} attempts")

    # Save to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sql": result["sql"],
        "attempts": result["attempts"]
    })

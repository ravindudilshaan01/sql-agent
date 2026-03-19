import streamlit as st
from agent import ask, get_db_uri

st.set_page_config(page_title="SQL Chat Agent", page_icon="🗄️", layout="centered")

st.title("Ask your database anything")
st.caption("Self-healing SQL agent · Powered by LangChain + Groq")

# ── Database source selector ──────────────────────────────────────────────────
st.subheader("1. Choose your data source")

source = st.radio(
    "What do you want to query?",
    options=["demo", "upload", "url"],
    format_func=lambda x: {
        "demo": "Use the sample shop database",
        "upload": "Upload my own file (.db or .csv)",
        "url": "Connect via database URL"
    }[x],
    horizontal=True
)

db_uri = None
uploaded_file = None

if source == "demo":
    st.success("Using the built-in sample database with customers, orders and products.")
    db_uri = "sqlite:///shop.db"

    with st.expander("Example questions to try"):
        st.markdown("""
- How many customers do we have?
- What are the top 5 most expensive products?
- Which city has the most customers?
- What is the total revenue from all orders?
- How many orders were placed per product category?
""")

elif source == "upload":
    uploaded_file = st.file_uploader(
        "Upload a .db or .csv file",
        type=["db", "csv"]
    )
    if uploaded_file:
        db_uri = get_db_uri("upload", uploaded_file)
        st.success(f"Loaded: {uploaded_file.name}")
    else:
        st.info("Upload a file to get started.")

elif source == "url":
    url_input = st.text_input(
        "Database URL",
        placeholder="e.g. sqlite:///mydb.db  or  postgresql://user:pass@host/dbname"
    )
    if url_input:
        db_uri = url_input
        st.success("URL saved. Ask your first question below.")
    else:
        st.info("Paste your database connection URL above.")

st.divider()

# ── Chat interface ────────────────────────────────────────────────────────────
st.subheader("2. Ask a question")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_source" not in st.session_state:
    st.session_state.last_source = None

# Clear chat history when user switches data source
if source != st.session_state.last_source:
    st.session_state.messages = []
    st.session_state.last_source = source

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            if msg.get("sql"):
                with st.expander("SQL query used"):
                    st.code(msg["sql"], language="sql")
            if msg.get("attempts", 1) > 1:
                st.warning(f"Self-healed after {msg['attempts']} attempts")

# Chat input — disabled until a source is ready
if db_uri:
    prompt = st.chat_input("Ask a question about your data...")
else:
    st.chat_input("Set up a data source above first...", disabled=True)
    prompt = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = ask(prompt, db_uri)

        st.write(result["answer"])

        if result.get("sql"):
            with st.expander("SQL query used"):
                st.code(result["sql"], language="sql")

        if result.get("attempts", 1) > 1:
            st.warning(f"Self-healed after {result['attempts']} attempts")

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sql": result.get("sql", ""),
        "attempts": result.get("attempts", 1)
    })

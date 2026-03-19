import streamlit as st
from agent import ask, get_db_uri

# Page config
st.set_page_config(
    page_title="SQL Chat Agent",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stRadio > label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
    }
    .source-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
        background: #f8f9fa;
    }
    .feature-box {
        padding: 1rem;
        border-radius: 8px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 0.5rem 0;
        text-align: center;
    }
    .metric-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🗄️ SQL Chat Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">🤖 Self-healing SQL agent powered by AI · Ask anything in plain English</p>', unsafe_allow_html=True)

# Sidebar with features and info
with st.sidebar:
    st.markdown("### ✨ Features")
    st.markdown("""
    - 🔄 **Self-Healing Queries** - Automatically fixes SQL errors
    - 🎯 **Multi-Source Support** - Demo, Upload, or URL
    - 💬 **Natural Language** - Ask questions in plain English
    - 📊 **Smart Results** - AI explains the data for you
    - 🚀 **Powered by Groq** - Lightning-fast responses
    """)

    st.markdown("---")

    st.markdown("### 📚 How to Use")
    st.markdown("""
    1. **Choose** your data source
    2. **Ask** a question in plain English
    3. **Get** instant AI-powered answers
    """)

    st.markdown("---")

    st.markdown("### 🔗 Links")
    st.markdown("""
    - [GitHub Repository](https://github.com/ravindudilshaan01/sql-agent)
    - [Built with Streamlit](https://streamlit.io)
    - [Powered by Groq](https://groq.com)
    """)

    st.markdown("---")
    st.caption("Made with ❤️ using LangChain + Groq")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Step 1: Choose Your Data Source")

with col2:
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        q_count = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("Questions Asked", q_count, help="Total questions in this session")

# Data source selector with improved UI
source = st.radio(
    "Select a data source:",
    options=["demo", "upload", "url"],
    format_func=lambda x: {
        "demo": "📦 Demo Database",
        "upload": "📤 Upload File",
        "url": "🔗 Database URL"
    }[x],
    horizontal=True,
    label_visibility="collapsed"
)

db_uri = None
uploaded_file = None

# Source-specific UI
if source == "demo":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.success("✅ Using the built-in sample shop database")
        db_uri = "sqlite:///shop.db"

    with st.expander("💡 Example Questions to Try", expanded=True):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            - 👥 How many customers do we have?
            - 💰 What are the top 5 most expensive products?
            - 🏙️ Which city has the most customers?
            """)
        with col_b:
            st.markdown("""
            - 💵 What is the total revenue from all orders?
            - 📊 How many orders were placed per category?
            - 🛍️ Show me the latest 10 orders
            """)

elif source == "upload":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader(
            "Upload your database or CSV file",
            type=["db", "csv"],
            help="Supports SQLite .db files and CSV files"
        )
        if uploaded_file:
            db_uri = get_db_uri("upload", uploaded_file)
            st.success(f"✅ Successfully loaded: **{uploaded_file.name}**")
            st.info("💡 Start asking questions about your data below!")
        else:
            st.info("📁 Drag and drop a file or click to browse")

elif source == "url":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        url_input = st.text_input(
            "Enter your database connection URL",
            placeholder="sqlite:///mydb.db or postgresql://user:pass@host/db",
            help="Supports PostgreSQL, MySQL, SQLite, and more"
        )
        if url_input:
            db_uri = url_input
            st.success("✅ Connection URL saved")
            st.info("💡 Ready to query! Ask your first question below.")
        else:
            st.info("🔗 Paste your database connection string above")

st.markdown("---")

# Chat interface
st.markdown("### 💬 Step 2: Ask Your Questions")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_source" not in st.session_state:
    st.session_state.last_source = None

# Clear chat history when switching sources
if source != st.session_state.last_source:
    st.session_state.messages = []
    st.session_state.last_source = source

# Display chat history with improved styling
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

        if msg["role"] == "assistant":
            if msg.get("sql"):
                with st.expander("🔍 View SQL Query", expanded=False):
                    st.code(msg["sql"], language="sql")

            if msg.get("attempts", 1) > 1:
                st.warning(f"⚡ Self-healed after {msg['attempts']} attempts")

# Chat input
if db_uri:
    prompt = st.chat_input("💭 Ask a question about your data...", key="chat_input")
else:
    st.info("👆 Please select and configure a data source above to start asking questions")
    prompt = None

# Handle new message
if prompt:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🔮 Analyzing your question and generating SQL..."):
            result = ask(prompt, db_uri)

        st.markdown(result["answer"])

        if result.get("sql"):
            with st.expander("🔍 View SQL Query", expanded=False):
                st.code(result["sql"], language="sql")

        if result.get("attempts", 1) > 1:
            st.warning(f"⚡ Self-healed: Fixed the query after {result['attempts']} attempts!")

    # Save to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sql": result.get("sql", ""),
        "attempts": result.get("attempts", 1)
    })

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🚀 **Fast & Reliable**")
    st.caption("Powered by Groq AI")
with col2:
    st.markdown("🔒 **Secure**")
    st.caption("Your data stays private")
with col3:
    st.markdown("🎯 **Accurate**")
    st.caption("Self-healing SQL queries")

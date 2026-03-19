import streamlit as st
from agent import ask, get_db_uri

# Page config
st.set_page_config(
    page_title="SQL Chat Agent",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS
st.markdown("""
<style>
    .main {
        background-color: #050E3C;
    }
    .stApp {
        background-color: #050E3C;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .sub-header {
        color: #e0e0e0;
        font-size: 1rem;
        margin-bottom: 2.5rem;
    }
    h4 {
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 48px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        transform: translateY(-2px);
        border: none;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    div[data-testid="stMetric"] label {
        color: white !important;
    }
    div[data-testid="stMetric"] div {
        color: white !important;
    }
    .info-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        color: #e0e0e0;
        background-color: transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(102, 126, 234, 0.3);
        color: white;
    }
    .element-container {
        color: #e0e0e0;
    }
    p, .stMarkdown {
        color: #e0e0e0;
    }
    /* User messages - Blue gradient */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    /* Assistant messages - Purple gradient */
    .stChatMessage[data-testid="assistant-message"] {
        background: linear-gradient(135deg, #6b21a8 0%, #a855f7 100%);
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3);
    }
    /* Alternative: Target by position */
    div[data-testid="stChatMessageContent"] {
        color: #ffffff !important;
    }
    /* Style for user avatar messages */
    .stChatMessage:has([alt="👤"]) {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
        border-left: 4px solid #60a5fa;
    }
    /* Style for assistant avatar messages */
    .stChatMessage:has([alt="🤖"]) {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%) !important;
        border-left: 4px solid #c084fc;
    }
    .stChatMessage {
        margin: 0.5rem 0;
        border-radius: 15px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Compact sidebar
with st.sidebar:
    st.markdown("### Features")
    st.markdown("🔄 Self-Healing SQL")
    st.markdown("🎯 Multi-Source")
    st.markdown("⚡ Fast AI responses")
    st.markdown("---")
    st.markdown("### About")
    st.caption("Built with LangChain + Groq")
    st.caption("[GitHub](https://github.com/ravindudilshaan01/sql-agent)")

# Header
st.markdown('<h1 class="main-header">🗄️ SQL Chat Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ask questions in plain English · Get instant answers from your data</p>', unsafe_allow_html=True)

# Compact layout
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("#### Choose Data Source")
with col2:
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        q_count = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("Questions", q_count)

# Modern tabs for source selection
tab1, tab2, tab3 = st.tabs(["📦 Demo", "📤 Upload", "🔗 URL"])

db_uri = None
uploaded_file = None

with tab1:
    st.success("Sample shop database loaded")
    db_uri = "sqlite:///shop.db"
    source = "demo"

    st.markdown("#### Try These Questions")
    col1, col2, col3 = st.columns(3)

    example_questions = [
        "How many customers do we have?",
        "Top 5 most expensive products",
        "Which city has most customers?",
        "Total revenue from orders",
        "Orders by product category",
        "Show latest 10 orders"
    ]

    for i, question in enumerate(example_questions):
        col = [col1, col2, col3][i % 3]
        with col:
            if st.button(question, key=f"q_{i}"):
                st.session_state.example_clicked = question

with tab2:
    uploaded_file = st.file_uploader(
        "Upload Database or CSV",
        type=["db", "csv"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        db_uri = get_db_uri("upload", uploaded_file)
        source = "upload"
        st.success(f"Loaded: **{uploaded_file.name}**")
    else:
        st.info("Drop your file here")

with tab3:
    url_input = st.text_input(
        "Database Connection URL",
        placeholder="sqlite:///mydb.db or postgresql://user:pass@host/db",
        label_visibility="collapsed"
    )
    if url_input:
        db_uri = url_input
        source = "url"
        st.success("Connected")
    else:
        st.info("Enter connection string")

st.markdown("---")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_source" not in st.session_state:
    st.session_state.last_source = None

# Clear chat when switching sources
if 'source' in locals() and source != st.session_state.last_source:
    st.session_state.messages = []
    st.session_state.last_source = source

# Chat interface
st.markdown("#### Conversation")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

        if msg["role"] == "assistant" and msg.get("sql"):
            with st.expander("View SQL"):
                st.code(msg["sql"], language="sql")

            if msg.get("attempts", 1) > 1:
                st.caption(f"⚡ Self-healed ({msg['attempts']} attempts)")

# Handle example question button click
if "example_clicked" in st.session_state:
    prompt = st.session_state.example_clicked
    del st.session_state.example_clicked

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analyzing..."):
            result = ask(prompt, db_uri)

        st.markdown(result["answer"])

        if result.get("sql"):
            with st.expander("View SQL"):
                st.code(result["sql"], language="sql")

        if result.get("attempts", 1) > 1:
            st.caption(f"⚡ Self-healed ({result['attempts']} attempts)")

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sql": result.get("sql", ""),
        "attempts": result.get("attempts", 1)
    })
    st.rerun()

# Chat input
if db_uri:
    prompt = st.chat_input("Ask anything about your data...")
else:
    st.info("👆 Select a data source to begin")
    prompt = None

# Handle user input
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analyzing..."):
            result = ask(prompt, db_uri)

        st.markdown(result["answer"])

        if result.get("sql"):
            with st.expander("View SQL"):
                st.code(result["sql"], language="sql")

        if result.get("attempts", 1) > 1:
            st.caption(f"⚡ Self-healed ({result['attempts']} attempts)")

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sql": result.get("sql", ""),
        "attempts": result.get("attempts", 1)
    })

# Minimal footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("⚡ Powered by Groq")
with col2:
    st.caption("🔒 Secure & Private")
with col3:
    st.caption("🎯 AI-Powered")

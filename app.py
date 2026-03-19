import streamlit as st
from agent import ask, get_db_uri

# Page config
st.set_page_config(
    page_title="SQL Chat Agent",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': 'https://github.com/ravindudilshaan01/sql-agent',
        'About': 'SQL Chat Agent with self-healing AI queries'
    }
)

# Add mobile viewport meta tag
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
""", unsafe_allow_html=True)

# Professional CSS matching the desired layout
st.markdown("""
<style>
    /* Base styles */
    .main {
        background-color: #2D2D30;
    }
    .stApp {
        background-color: #2D2D30;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        margin-top: 0;
    }

    /* Sidebar styling - compact left panel */
    .css-1d391kg {
        width: 240px !important;
        min-width: 240px !important;
        max-width: 240px !important;
        background-color: #f8f9fa !important;
        padding: 1rem !important;
    }

    /* Sidebar content styling */
    .css-1d391kg h4 {
        color: #333333 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }

    .css-1d391kg .stMarkdown {
        color: #555555 !important;
        font-size: 0.9rem !important;
    }

    /* Data source section */
    .stRadio > div {
        background-color: transparent !important;
        border: none !important;
        padding: 0.5rem 0 !important;
    }

    .stRadio label {
        color: #333333 !important;
        font-size: 0.9rem !important;
    }

    /* File uploader styling */
    .stFileUploader {
        background-color: #ffffff;
        border: 2px dashed #cccccc;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
    }

    /* Connection status badges */
    .success-badge {
        background-color: #d4edda;
        color: #155724;
        padding: 0.3rem 0.6rem;
        border-radius: 4px;
        font-size: 0.8rem;
        text-align: center;
        margin: 0.3rem 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .connected-dot {
        width: 6px;
        height: 6px;
        background-color: #28a745;
        border-radius: 50%;
        margin-right: 6px;
    }

    /* Tables section */
    .table-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.3rem;
        margin: 0.5rem 0;
    }

    .table-chip {
        background-color: #007bff;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    /* Session statistics */
    .stats-container {
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
    }

    .stat-box {
        background-color: #343a40;
        color: white;
        padding: 0.8rem;
        border-radius: 6px;
        text-align: center;
        flex: 1;
    }

    .stat-number {
        font-size: 1.5rem;
        font-weight: bold;
        display: block;
    }

    .stat-label {
        font-size: 0.75rem;
        opacity: 0.8;
    }

    /* Main chat area */
    .stChatMessage {
        margin: 0.5rem 0;
        border-radius: 8px;
        padding: 1rem;
    }

    /* User messages - Blue */
    .stChatMessage:has([alt="👤"]) {
        background-color: #007bff !important;
        color: white !important;
        margin-left: 2rem;
    }

    .stChatMessage:has([alt="👤"]) .stMarkdown {
        color: white !important;
    }

    /* AI messages - Dark Gray */
    .stChatMessage:has([alt="🤖"]) {
        background-color: #495057 !important;
        color: white !important;
        margin-right: 2rem;
    }

    .stChatMessage:has([alt="🤖"]) .stMarkdown {
        color: white !important;
    }

    /* SQL query expander */
    .stExpander {
        background-color: #6c757d;
        border-radius: 6px;
        margin: 0.5rem 0;
    }

    .stExpander summary {
        color: white !important;
        font-size: 0.9rem !important;
    }

    /* Self-heal badge */
    .heal-badge {
        background-color: #ffc107;
        color: #212529;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
        display: inline-block;
        margin: 0.25rem 0;
    }

    /* Example buttons at bottom */
    .example-section {
        margin: 1rem 0;
    }

    .example-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }

    .stButton button {
        background-color: #6c757d !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.9rem !important;
        height: auto !important;
        min-height: 36px !important;
        transition: all 0.2s ease !important;
    }

    .stButton button:hover {
        background-color: #5a6268 !important;
        transform: translateY(-1px) !important;
    }

    /* Chat input */
    .stChatInput input {
        border-radius: 25px !important;
        border: 1px solid #ced4da !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        background-color: white !important;
    }

    /* Main content text */
    .main .stMarkdown {
        color: #ffffff;
    }

    /* Button in sidebar */
    .css-1d391kg .stButton button {
        background-color: #007bff !important;
        color: white !important;
        width: 100% !important;
        font-size: 0.85rem !important;
        padding: 0.5rem !important;
        margin: 0.25rem 0 !important;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar - Compact Left Panel
with st.sidebar:
    st.markdown("### 🗄️ Data Source")

    # Source selector
    source = st.radio(
        "Choose your database:",
        options=["demo", "upload", "url"],
        format_func=lambda x: {
            "demo": "📦 Demo Shop DB",
            "upload": "📤 Upload File",
            "url": "🔗 Remote URL"
        }[x],
        label_visibility="collapsed"
    )

    db_uri = None
    uploaded_file = None

    # Database connection handling
    if source == "demo":
        st.markdown('<div class="success-badge"><span class="connected-dot"></span>Connected</div>', unsafe_allow_html=True)
        db_uri = "sqlite:///shop.db"

        # Tables found section
        st.markdown("**Tables Found:**")
        st.markdown('<div class="table-chips"><span class="table-chip">customers</span><span class="table-chip">products</span><span class="table-chip">orders</span></div>', unsafe_allow_html=True)

    elif source == "upload":
        uploaded_file = st.file_uploader(
            "Drop files here",
            type=["db", "csv"],
            label_visibility="collapsed"
        )
        if uploaded_file:
            db_uri = get_db_uri("upload", uploaded_file)
            st.markdown('<div class="success-badge"><span class="connected-dot"></span>Connected</div>', unsafe_allow_html=True)

            # Show uploaded file info
            file_name = uploaded_file.name
            table_name = file_name.split('.')[0].replace(" ", "_").lower()
            st.markdown("**Tables Found:**")
            st.markdown(f'<div class="table-chips"><span class="table-chip">{table_name}</span></div>', unsafe_allow_html=True)

    elif source == "url":
        url_input = st.text_input(
            "Database URL",
            placeholder="postgresql://user:pass@host/db",
            label_visibility="collapsed"
        )
        if url_input:
            db_uri = url_input
            st.markdown('<div class="success-badge"><span class="connected-dot"></span>Connected</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Session statistics
    st.markdown("**Session Stats:**")
    if "messages" in st.session_state:
        questions = len([m for m in st.session_state.messages if m["role"] == "user"])
        healed = len([m for m in st.session_state.messages if m["role"] == "assistant" and m.get("attempts", 1) > 1])
    else:
        questions = healed = 0

    # Stats display
    st.markdown(f'''
    <div class="stats-container">
        <div class="stat-box">
            <span class="stat-number">{questions}</span>
            <span class="stat-label">Questions</span>
        </div>
        <div class="stat-box">
            <span class="stat-number">{healed}</span>
            <span class="stat-label">Self-heals</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("---")

    # Example buttons
    if db_uri:
        st.markdown("**Try Examples:**")
        example_questions = [
            "How many customers?",
            "Top 5 products?",
            "Total revenue?"
        ]

        for question in example_questions:
            if st.button(question, key=f"sidebar_{question}", use_container_width=True):
                st.session_state.example_clicked = question

# Main Chat Area
# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_source" not in st.session_state:
    st.session_state.last_source = None

# Clear chat when switching sources
if source != st.session_state.last_source:
    st.session_state.messages = []
    st.session_state.last_source = source

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

        if msg["role"] == "assistant":
            # SQL chip (expandable)
            if msg.get("sql"):
                with st.expander("🔍 View SQL query"):
                    st.code(msg["sql"], language="sql")

            # Self-heal badge (only if attempts > 1)
            if msg.get("attempts", 1) > 1:
                st.markdown(f'<div class="heal-badge">⚡ Self-healed · {msg["attempts"]} attempts</div>', unsafe_allow_html=True)

# Example question buttons (only show if demo database and no chat history)
if source == "demo" and len(st.session_state.messages) == 0:
    st.markdown('<div class="example-section">', unsafe_allow_html=True)
    st.markdown("**💡 Try These Examples:**")

    example_questions = [
        "How many customers do we have?",
        "Top 5 most expensive products",
        "Which city has most customers?",
        "Total revenue from orders"
    ]

    # Create columns for examples
    cols = st.columns(len(example_questions))
    for i, question in enumerate(example_questions):
        with cols[i]:
            if st.button(question, key=f"example_{i}"):
                st.session_state.example_clicked = question

    st.markdown('</div>', unsafe_allow_html=True)

# Handle example clicks
if "example_clicked" in st.session_state:
    prompt = st.session_state.example_clicked
    del st.session_state.example_clicked

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI response
    with st.spinner("🔮 Analyzing and generating SQL..."):
        result = ask(prompt, db_uri)

    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sql": result.get("sql", ""),
        "attempts": result.get("attempts", 1)
    })
    st.rerun()

# Chat input
if db_uri:
    if prompt := st.chat_input("Ask a question about your data..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🔮 Analyzing and generating SQL..."):
                result = ask(prompt, db_uri)

            st.markdown(result["answer"])

            # SQL chip
            if result.get("sql"):
                with st.expander("🔍 View SQL query"):
                    st.code(result["sql"], language="sql")

            # Self-heal badge
            if result.get("attempts", 1) > 1:
                st.markdown(f'<div class="heal-badge">⚡ Self-healed · {result["attempts"]} attempts</div>', unsafe_allow_html=True)

        # Save to session
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sql": result.get("sql", ""),
            "attempts": result.get("attempts", 1)
        })
else:
    st.markdown("### 👋 Welcome to SQL Chat Agent")
    st.markdown("**Connect to a database in the sidebar to start chatting**")
    st.markdown("- 📦 Use the demo database for instant access")
    st.markdown("- 📤 Upload your own CSV or SQLite files")
    st.markdown("- 🔗 Connect to remote databases via URL")

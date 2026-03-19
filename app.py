import streamlit as st
from agent import ask, get_db_uri
from langchain_community.utilities import SQLDatabase

# Page config
st.set_page_config(
    page_title="SQL Chat Agent",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Complete CSS Implementation based on JSON specification
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* App layout - sidebar + main */
    .stApp {
        background-color: #0E1117;
        font-family: sans-serif;
    }

    .main {
        padding: 0 !important;
        margin: 0 !important;
        background-color: #0E1117;
    }

    /* SIDEBAR - 260px wide, light theme */
    .css-1d391kg {
        width: 260px !important;
        min-width: 260px !important;
        max-width: 260px !important;
        background-color: #F0F2F6 !important;
        border-right: 1px solid #E0E0E0 !important;
        padding: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        overflow-y: auto !important;
        height: 100vh !important;
    }

    /* Zone 1 - Sidebar Header */
    .sidebar-header {
        background: #1E3A5F;
        height: 60px;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .sidebar-header-content {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .sidebar-icon {
        width: 18px;
        height: 18px;
        background: #378ADD;
        border-radius: 4px;
    }

    .sidebar-title {
        font-size: 15px;
        font-weight: 500;
        color: #FFFFFF;
        margin: 0;
    }

    .version-badge {
        font-size: 10px;
        color: #AACCEE;
        background: #2A4A6F;
        border-radius: 10px;
        padding: 2px 8px;
    }

    /* Sidebar sections */
    .sidebar-section {
        background: #FFFFFF;
        padding: 14px 16px;
        border-bottom: 1px solid #E0E0E0;
    }

    .section-label {
        font-size: 11px;
        font-weight: 500;
        color: #6B7280;
        margin-bottom: 10px;
        display: block;
    }

    /* Zone 2 - Radio buttons */
    .stRadio > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        gap: 8px !important;
    }

    .stRadio label {
        font-size: 13px !important;
        color: #111827 !important;
        font-weight: 400 !important;
        display: flex !important;
        align-items: center !important;
    }

    .stRadio label:has(input:checked) {
        font-weight: 500 !important;
    }

    /* Zone 3 - File uploader */
    .upload-zone {
        border: 1.5px dashed #7F77DD;
        border-radius: 8px;
        padding: 16px;
        background: #EEEDFE;
        text-align: center;
        margin-top: 8px;
    }

    .upload-icon {
        width: 20px;
        height: 20px;
        margin: 0 auto 6px;
        background: #534AB7;
        -webkit-clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
        clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
    }

    .upload-primary {
        font-size: 12px;
        color: #534AB7;
        margin-bottom: 3px;
    }

    .upload-secondary {
        font-size: 11px;
        color: #7F77DD;
    }

    /* Zone 4 - URL input */
    .url-section .stTextInput > div > div > input {
        width: 100% !important;
        height: 34px !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        padding: 0 10px !important;
        font-size: 12px !important;
        background: #1C1C1E !important;
        color: #FFFFFF !important;
    }

    .url-section .stTextInput > div > div > input:focus {
        border-color: #378ADD !important;
    }

    .url-section .stButton > button {
        width: 100% !important;
        height: 32px !important;
        margin-top: 8px !important;
        background: #D85A30 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }

    .url-section .stButton > button:hover {
        background: #993C1D !important;
    }

    /* Zone 5 - Connection status */
    .connection-status {
        background: #E1F5EE;
        padding: 12px 16px;
        border-bottom: 1px solid #E0E0E0;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .connection-status.error {
        background: #FCEBEB;
    }

    .connection-row {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .connection-dot {
        width: 7px;
        height: 7px;
        background: #0F6E56;
        border-radius: 50%;
    }

    .connection-text {
        font-size: 12px;
        font-weight: 500;
        color: #085041;
    }

    .connection-filename {
        font-size: 11px;
        font-family: monospace;
        color: #0F6E56;
    }

    .progress-bar {
        width: 100%;
        height: 3px;
        background: #5DCAA5;
        border-radius: 2px;
        margin-top: 8px;
    }

    /* Zone 6 - Table pills */
    .tables-section {
        background: #FFFFFF;
        padding: 14px 16px;
        border-bottom: 1px solid #E0E0E0;
    }

    .tables-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 8px;
    }

    .table-pill {
        font-size: 11px;
        padding: 3px 9px;
        border-radius: 10px;
        background: #E1F5EE;
        color: #085041;
        border: 1px solid #5DCAA5;
    }

    /* Zone 7 - Session stats */
    .stats-section {
        background: #F3F4F6;
        padding: 14px 16px;
        border-bottom: 1px solid #E0E0E0;
    }

    .stats-cards {
        display: flex;
        gap: 8px;
        margin-top: 10px;
    }

    .stat-card {
        background: #1C1C1E;
        border-radius: 8px;
        padding: 8px 10px;
        width: 50%;
        text-align: center;
    }

    .stat-label {
        font-size: 10px;
        color: #9CA3AF;
        display: block;
    }

    .stat-value {
        font-size: 22px;
        font-weight: 500;
        color: #FFFFFF;
        display: block;
        margin-top: 2px;
    }

    .stat-value.amber {
        color: #EF9F27;
    }

    /* Zone 8 - Clear button */
    .clear-section {
        margin-top: auto;
        padding: 14px 16px;
        border-top: 1px solid #E0E0E0;
    }

    .clear-section .stButton > button {
        width: 100% !important;
        height: 34px !important;
        background: transparent !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        font-size: 12px !important;
        color: #6B7280 !important;
    }

    .clear-section .stButton > button:hover {
        background: #F3F4F6 !important;
    }

    /* MAIN AREA - Dark theme */
    .main-content {
        display: flex;
        flex-direction: column;
        height: 100vh;
        background: #0E1117;
    }

    /* Zone 9 - Main header */
    .main-header {
        background: #0E1117;
        height: 52px;
        padding: 0 24px;
        border-bottom: 1px solid #2A2A2A;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .main-title {
        font-size: 16px;
        font-weight: 500;
        color: #FFFFFF;
        margin: 0;
    }

    .main-caption {
        font-size: 12px;
        color: #6B7280;
        margin: 2px 0 0 0;
    }

    /* Zone 10 - Chat messages */
    .chat-container {
        flex: 1;
        background: #0E1117;
        padding: 20px 24px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .stChatMessage {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        display: flex !important;
        align-items: flex-start !important;
        gap: 6px !important;
    }

    /* User messages - right aligned */
    .stChatMessage:has([alt="👤"]) {
        justify-content: flex-end !important;
        flex-direction: row-reverse !important;
    }

    .stChatMessage:has([alt="👤"]) .stChatMessage-content {
        background: #1E3A5F !important;
        color: #FFFFFF !important;
        border-radius: 10px 10px 2px 10px !important;
        padding: 9px 13px !important;
        max-width: 65% !important;
        font-size: 13px !important;
        line-height: 1.5 !important;
    }

    /* User avatar */
    .stChatMessage:has([alt="👤"]) img {
        width: 28px !important;
        height: 28px !important;
        border-radius: 50% !important;
        background: #1E3A5F !important;
    }

    /* AI messages - left aligned */
    .stChatMessage:has([alt="🤖"]) {
        justify-content: flex-start !important;
    }

    .stChatMessage:has([alt="🤖"]) .stChatMessage-content {
        display: flex !important;
        flex-direction: column !important;
        gap: 6px !important;
        max-width: 82% !important;
    }

    /* AI avatar */
    .stChatMessage:has([alt="🤖"]) img {
        width: 28px !important;
        height: 28px !important;
        border-radius: 50% !important;
        background: #EEEDFE !important;
    }

    /* AI bubble */
    .ai-bubble {
        background: #1E1E1E;
        color: #FFFFFF;
        border-radius: 10px 10px 10px 2px;
        padding: 9px 13px;
        font-size: 13px;
        line-height: 1.5;
    }

    /* SQL Expander */
    .stExpander {
        border: 1px solid #2A2A2A !important;
        border-radius: 6px !important;
        background: #1A1A1A !important;
        margin: 0 !important;
    }

    .stExpander summary {
        height: 32px !important;
        padding: 0 12px !important;
        color: #6B7280 !important;
        font-size: 11px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
    }

    .stExpander .stCodeBlock {
        background: #1A1A1A !important;
        font-size: 12px !important;
        font-family: monospace !important;
    }

    /* Self-heal badge */
    .heal-badge {
        background: #FAEEDA;
        border: 1px solid #EF9F27;
        border-radius: 6px;
        padding: 5px 12px;
        font-size: 11px;
        font-weight: 500;
        color: #854F0B;
        display: inline-block;
        margin-top: 4px;
    }

    /* Zone 11 - Example chips */
    .chips-row {
        background: #16161A;
        height: 44px;
        padding: 0 24px;
        border-top: 1px solid #2A2A2A;
        border-bottom: 1px solid #2A2A2A;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .chips-label {
        font-size: 11px;
        color: #6B7280;
        margin-right: 4px;
    }

    .chip-button {
        padding: 5px 12px;
        border: 1px solid #2A2A2A;
        border-radius: 20px;
        background: #1A1A1A;
        font-size: 12px;
        color: #9CA3AF;
        cursor: pointer;
        transition: all 0.2s;
    }

    .chip-button:hover {
        background: #2A2A2A;
        border-color: #4A4A4A;
    }

    .chips-row .stButton > button {
        padding: 5px 12px !important;
        border: 1px solid #2A2A2A !important;
        border-radius: 20px !important;
        background: #1A1A1A !important;
        font-size: 12px !important;
        color: #9CA3AF !important;
        height: auto !important;
        min-height: auto !important;
    }

    .chips-row .stButton > button:hover {
        background: #2A2A2A !important;
        border-color: #4A4A4A !important;
    }

    /* Zone 12 - Chat input */
    .chat-input-row {
        background: #0E1117;
        height: 60px;
        padding: 0 24px;
        border-top: 1px solid #2A2A2A;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .stChatInput {
        flex: 1 !important;
    }

    .stChatInput > div {
        border: 1px solid #2A2A2A !important;
        border-radius: 20px !important;
        background: #1A1A1A !important;
    }

    .stChatInput input {
        height: 40px !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0 16px !important;
        font-size: 13px !important;
        background: #1A1A1A !important;
        color: #FFFFFF !important;
    }

    .stChatInput input::placeholder {
        color: #4B4B4B !important;
    }

    .stChatInput input:focus {
        border: 1px solid #378ADD !important;
        outline: none !important;
        box-shadow: none !important;
    }

    .stChatInput input:disabled {
        opacity: 0.4 !important;
        pointer-events: none !important;
    }

    /* File uploader styling override */
    .stFileUploader {
        margin: 0 !important;
    }

    .stFileUploader > div {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    /* Welcome message styling */
    .welcome-area {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: #FFFFFF;
        padding: 40px;
    }

    .welcome-title {
        font-size: 24px;
        font-weight: 500;
        margin-bottom: 16px;
        color: #FFFFFF;
    }

    .welcome-subtitle {
        font-size: 16px;
        color: #6B7280;
        margin-bottom: 32px;
    }

    .welcome-steps {
        display: flex;
        flex-direction: column;
        gap: 12px;
        font-size: 14px;
        color: #9CA3AF;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_source" not in st.session_state:
    st.session_state.last_source = None
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0
if "self_heals_triggered" not in st.session_state:
    st.session_state.self_heals_triggered = 0
if "prefill" not in st.session_state:
    st.session_state.prefill = ""

# Sidebar Layout
with st.sidebar:
    # Zone 1 - Sidebar Header
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-header-content">
            <div class="sidebar-icon"></div>
            <h4 class="sidebar-title">SQL Chat Agent</h4>
        </div>
        <div class="version-badge">v1.0</div>
    </div>
    """, unsafe_allow_html=True)

    # Zone 2 - Data source selector
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<span class="section-label">Data source</span>', unsafe_allow_html=True)

    source = st.radio(
        "Choose your database:",
        options=["demo", "upload", "url"],
        format_func=lambda x: {
            "demo": "Use sample shop database",
            "upload": "Upload my own file (.db or .csv)",
            "url": "Connect via database URL"
        }[x],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    db_uri = None
    uploaded_file = None
    table_names = []

    # Zone 3 - File uploader (conditional)
    if source == "upload":
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<span class="section-label">Upload file</span>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload file",
            type=["db", "csv"],
            label_visibility="collapsed"
        )

        if not uploaded_file:
            st.markdown("""
            <div class="upload-zone">
                <div class="upload-icon"></div>
                <div class="upload-primary">Drag and drop or browse</div>
                <div class="upload-secondary">.db or .csv accepted</div>
            </div>
            """, unsafe_allow_html=True)

        if uploaded_file:
            db_uri = get_db_uri("upload", uploaded_file)
            file_name = uploaded_file.name
            table_names = [file_name.split('.')[0].replace(" ", "_").lower()]

        st.markdown('</div>', unsafe_allow_html=True)

    # Zone 4 - URL input (conditional)
    elif source == "url":
        st.markdown('<div class="sidebar-section url-section">', unsafe_allow_html=True)
        st.markdown('<span class="section-label">Or connect URL</span>', unsafe_allow_html=True)

        url_input = st.text_input(
            "Database URL",
            placeholder="sqlite:///mydb.db",
            label_visibility="collapsed"
        )

        connect_clicked = st.button("Connect", use_container_width=True)

        if url_input and connect_clicked:
            db_uri = url_input
            try:
                db = SQLDatabase.from_uri(db_uri)
                table_names = db.get_usable_table_names()
            except:
                table_names = []

        st.markdown('</div>', unsafe_allow_html=True)

    # Demo database setup
    elif source == "demo":
        db_uri = "sqlite:///shop.db"
        table_names = ["customers", "products", "orders"]

    # Zone 5 - Connection status
    if db_uri:
        if source == "demo":
            filename = "shop.db"
        elif source == "upload" and uploaded_file:
            filename = uploaded_file.name
        elif source == "url" and url_input:
            filename = url_input.split("/")[-1] if "/" in url_input else url_input
        else:
            filename = ""

        st.markdown(f"""
        <div class="connection-status">
            <div class="connection-row">
                <div class="connection-dot"></div>
                <span class="connection-text">Connected</span>
            </div>
            <div class="connection-filename">{filename}</div>
            <div class="progress-bar"></div>
        </div>
        """, unsafe_allow_html=True)

    # Zone 6 - Tables found
    if table_names:
        st.markdown('<div class="tables-section">', unsafe_allow_html=True)
        st.markdown('<span class="section-label">Tables found</span>', unsafe_allow_html=True)

        pills_html = ''.join([f'<span class="table-pill">{table}</span>' for table in table_names])
        st.markdown(f'<div class="tables-pills">{pills_html}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Zone 7 - Session stats
    st.markdown('<div class="stats-section">', unsafe_allow_html=True)
    st.markdown('<span class="section-label">Session stats</span>', unsafe_allow_html=True)

    questions_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    heals_count = len([m for m in st.session_state.messages if m["role"] == "assistant" and m.get("attempts", 1) > 1])

    st.markdown(f"""
    <div class="stats-cards">
        <div class="stat-card">
            <span class="stat-label">Questions</span>
            <span class="stat-value">{questions_count}</span>
        </div>
        <div class="stat-card">
            <span class="stat-label">Self-heals</span>
            <span class="stat-value amber">{heals_count}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Zone 8 - Clear chat button (at bottom)
    st.markdown('<div class="clear-section">', unsafe_allow_html=True)
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.questions_asked = 0
        st.session_state.self_heals_triggered = 0
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Clear chat when switching sources
if source != st.session_state.last_source:
    st.session_state.messages = []
    st.session_state.questions_asked = 0
    st.session_state.self_heals_triggered = 0
    st.session_state.last_source = source

# Zone 9 - Main header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">Ask your database anything</h1>
    <p class="main-caption">Self-healing SQL agent · LangChain + Groq</p>
</div>
""", unsafe_allow_html=True)

# Zone 10 - Chat messages area
if st.session_state.messages:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
            if msg["role"] == "user":
                st.markdown(msg["content"])
            else:
                st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

                # SQL expander
                if msg.get("sql"):
                    with st.expander("View SQL query"):
                        st.code(msg["sql"], language="sql")

                # Self-heal badge
                if msg.get("attempts", 1) > 1:
                    st.markdown(f'<div class="heal-badge">self-healed · {msg["attempts"]} attempts</div>', unsafe_allow_html=True)
else:
    # Welcome message when no chat
    if not db_uri:
        st.markdown("""
        <div class="welcome-area">
            <h2 class="welcome-title">Welcome to SQL Chat Agent</h2>
            <p class="welcome-subtitle">Connect to a database to start asking questions in natural language</p>
            <div class="welcome-steps">
                <div>📦 Use the demo database for instant access</div>
                <div>📤 Upload your own CSV or SQLite files</div>
                <div>🔗 Connect to remote databases via URL</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Zone 11 - Example question chips (only when connected and no messages)
if db_uri and len(st.session_state.messages) == 0:
    st.markdown('<div class="chips-row">', unsafe_allow_html=True)
    st.markdown('<span class="chips-label">Try:</span>', unsafe_allow_html=True)

    example_questions = ["How many customers?", "Top 5 products?", "Total revenue?"]

    cols = st.columns(len(example_questions))
    for i, question in enumerate(example_questions):
        with cols[i]:
            if st.button(question, key=f"chip_{i}"):
                st.session_state.prefill = question
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Handle prefilled questions
if st.session_state.prefill and db_uri:
    prompt = st.session_state.prefill
    st.session_state.prefill = ""

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI response
    with st.spinner("🔮 Analyzing and generating SQL..."):
        result = ask(prompt, db_uri)

    # Update counters
    st.session_state.questions_asked += 1
    if result.get("attempts", 1) > 1:
        st.session_state.self_heals_triggered += 1

    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sql": result.get("sql", ""),
        "attempts": result.get("attempts", 1)
    })
    st.rerun()

# Zone 12 - Chat input
placeholder_text = "Ask a question about your data..." if db_uri else "Set up a data source on the left first..."
disabled = not bool(db_uri)

if prompt := st.chat_input(placeholder_text, disabled=disabled):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🔮 Analyzing and generating SQL..."):
            result = ask(prompt, db_uri)

        st.markdown(f'<div class="ai-bubble">{result["answer"]}</div>', unsafe_allow_html=True)

        if result.get("sql"):
            with st.expander("View SQL query"):
                st.code(result["sql"], language="sql")

        if result.get("attempts", 1) > 1:
            st.markdown(f'<div class="heal-badge">self-healed · {result["attempts"]} attempts</div>', unsafe_allow_html=True)

    # Update counters
    st.session_state.questions_asked += 1
    if result.get("attempts", 1) > 1:
        st.session_state.self_heals_triggered += 1

    # Save to session
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sql": result.get("sql", ""),
        "attempts": result.get("attempts", 1)
    })
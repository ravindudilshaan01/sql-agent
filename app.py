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

# Complete CSS Implementation based on comprehensive JSON specification
st.markdown("""
<style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Force sidebar to always be visible */
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        width: 300px !important;
        min-width: 300px !important;
        transform: none !important;
        margin-left: 0 !important;
    }

    /* Hide sidebar toggle button */
    button[kind="header"] {
        display: none !important;
    }

    /* App layout */
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
    }

    .main {
        padding: 0 !important;
        margin: 0 !important;
        background-color: #0E1117;
    }

    /* SIDEBAR - 300px wide, dark theme */
    .css-1d391kg,
    .css-1cypcdb,
    .css-17eq0hr,
    .css-1544g2n,
    section[data-testid="stSidebar"] {
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
        background-color: #161920 !important;
        border-right: 1px solid rgba(255,255,255,0.08) !important;
        padding: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        overflow-y: auto !important;
        height: 100vh !important;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #161920 !important;
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
    }

    /* Zone 1 - Sidebar Header */
    .sidebar-header {
        background: #1E3A5F;
        height: 64px;
        padding: 0 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }

    .logo-row {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .icon-box {
        width: 28px;
        height: 28px;
        background: #378ADD;
        border-radius: 6px;
    }

    .app-title {
        font-size: 15px;
        font-weight: 500;
        color: #FFFFFF;
        margin: 0;
    }

    .version-badge {
        font-size: 10px;
        font-weight: 500;
        color: #AACCEE;
        background: #2a4a6f;
        border-radius: 10px;
        padding: 2px 8px;
    }

    /* Sidebar sections */
    .sidebar-section {
        background: #161920;
        padding: 14px 16px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    .section-label {
        font-size: 11px;
        font-weight: 500;
        color: #A0A8B8;
        margin-bottom: 12px;
        display: block;
    }

    /* Radio buttons */
    .stRadio > div,
    section[data-testid="stSidebar"] .stRadio > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        gap: 10px !important;
    }

    .stRadio label,
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 13px !important;
        color: #FAFAFA !important;
        font-weight: 400 !important;
        display: flex !important;
        align-items: center !important;
    }

    .stRadio label:has(input:checked),
    section[data-testid="stSidebar"] .stRadio label:has(input:checked) {
        font-weight: 500 !important;
    }

    /* File uploader */
    .upload-zone {
        border: 1.5px dashed #7F77DD;
        border-radius: 8px;
        background: rgba(83,74,183,0.08);
        padding: 18px 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        margin-top: 8px;
    }

    .upload-icon {
        width: 20px;
        height: 20px;
        background: #534AB7;
        -webkit-clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
        clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
    }

    .upload-primary {
        font-size: 12px;
        color: #534AB7;
        font-weight: 500;
    }

    .upload-secondary {
        font-size: 11px;
        color: #7F77DD;
    }

    /* URL input section */
    .url-section .stTextInput > div > div > input {
        width: 100% !important;
        height: 36px !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 6px !important;
        padding: 0 12px !important;
        font-size: 12px !important;
        background: #21252D !important;
        color: #FAFAFA !important;
    }

    .url-section .stTextInput > div > div > input:focus {
        border-color: #378ADD !important;
    }

    .url-section .stButton > button {
        width: 100% !important;
        height: 34px !important;
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

    /* Connection status */
    .connection-status {
        background: rgba(15,110,86,0.15);
        padding: 12px 16px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    .connection-status.error {
        background: rgba(226,75,74,0.12);
    }

    .status-row {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #0F6E56;
    }

    .status-dot.error {
        background: #E24B4A;
    }

    .status-text {
        font-size: 12px;
        font-weight: 500;
        color: #5DCAA5;
    }

    .status-text.error {
        color: #F09595;
    }

    .status-filename {
        font-size: 11px;
        font-family: monospace;
        color: #0F6E56;
        margin-top: 4px;
    }

    /* Table pills */
    .tables-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 8px;
    }

    .table-pill {
        font-size: 11px;
        padding: 3px 10px;
        border-radius: 10px;
        background: rgba(15,110,86,0.15);
        color: #5DCAA5;
        border: 1px solid rgba(93,202,165,0.3);
    }

    /* Session stats */
    .stats-row {
        display: flex;
        gap: 8px;
        margin-top: 10px;
    }

    .metric-card {
        background: #21252D;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 8px;
        padding: 10px 12px;
        flex: 1;
        text-align: center;
    }

    .metric-label {
        font-size: 10px;
        color: #A0A8B8;
        display: block;
        margin-bottom: 4px;
    }

    .metric-value {
        font-size: 24px;
        font-weight: 500;
        color: #FAFAFA;
        display: block;
    }

    .metric-value.amber {
        color: #BA7517;
    }

    /* Clear button */
    .clear-section {
        margin-top: auto;
        padding: 14px 16px;
        border-top: 1px solid rgba(255,255,255,0.08);
        background: #161920;
    }

    .clear-section .stButton > button,
    section[data-testid="stSidebar"] .clear-section .stButton > button {
        width: 100% !important;
        height: 34px !important;
        background: transparent !important;
        color: #A0A8B8 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 6px !important;
        font-size: 12px !important;
        font-weight: 400 !important;
    }

    .clear-section .stButton > button:hover,
    section[data-testid="stSidebar"] .clear-section .stButton > button:hover {
        background: rgba(255,255,255,0.05) !important;
    }

    /* MAIN AREA */
    /* Zone 9 - Top header */
    .main-header {
        background: #161920;
        height: 56px;
        padding: 0 24px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .main-title {
        font-size: 16px;
        font-weight: 500;
        color: #FAFAFA;
        line-height: 1.2;
        margin: 0;
    }

    .main-caption {
        font-size: 12px;
        font-weight: 400;
        color: #A0A8B8;
        margin: 3px 0 0 0;
    }

    /* Zone 10 - Chat messages */
    .chat-container {
        flex: 1;
        background: #0E1117;
        padding: 24px 24px 16px 24px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 24px;
    }

    .stChatMessage {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* User messages */
    .stChatMessage:has([alt="👤"]) {
        display: flex !important;
        justify-content: flex-end !important;
        align-items: flex-end !important;
        gap: 8px !important;
        flex-direction: row-reverse !important;
    }

    .stChatMessage:has([alt="👤"]) .stChatMessage-content {
        max-width: 65% !important;
        background: #1E3A5F !important;
        color: #FFFFFF !important;
        border-radius: 12px 12px 2px 12px !important;
        padding: 10px 14px !important;
        font-size: 13px !important;
        line-height: 1.5 !important;
    }

    .stChatMessage:has([alt="👤"]) img {
        width: 28px !important;
        height: 28px !important;
        border-radius: 50% !important;
        background: #1E3A5F !important;
        flex-shrink: 0 !important;
    }

    /* AI messages */
    .stChatMessage:has([alt="🤖"]) {
        display: flex !important;
        justify-content: flex-start !important;
        align-items: flex-start !important;
        gap: 8px !important;
    }

    .stChatMessage:has([alt="🤖"]) img {
        width: 28px !important;
        height: 28px !important;
        border-radius: 50% !important;
        background: rgba(83,74,183,0.2) !important;
        flex-shrink: 0 !important;
    }

    .ai-content-column {
        display: flex;
        flex-direction: column;
        gap: 6px;
        max-width: 82%;
    }

    .ai-bubble {
        background: #21252D;
        color: #FAFAFA;
        border-radius: 2px 12px 12px 12px;
        padding: 10px 14px;
        font-size: 13px;
        line-height: 1.5;
        width: 100%;
    }

    /* SQL Expander */
    .stExpander {
        background: #21252D !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 8px !important;
        margin: 0 !important;
    }

    .stExpander summary {
        height: 36px !important;
        padding: 0 14px !important;
        color: #A0A8B8 !important;
        font-size: 11px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        background: #21252D !important;
    }

    .stExpander .stCodeBlock {
        background: #161920 !important;
        border-radius: 0 0 8px 8px !important;
        padding: 12px 14px !important;
    }

    .stExpander .stCodeBlock code {
        font-family: monospace !important;
        font-size: 12px !important;
        color: #5DCAA5 !important;
        line-height: 1.6 !important;
    }

    /* Self-heal badge */
    .selfheal-badge {
        background: rgba(186,117,23,0.12);
        border: 1px solid rgba(239,159,39,0.4);
        border-radius: 8px;
        padding: 6px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 11px;
        font-weight: 500;
        color: #BA7517;
    }

    /* Zone 11 - Example chips */
    .chips-row {
        background: #161920;
        height: 48px;
        padding: 0 24px;
        border-top: 1px solid rgba(255,255,255,0.08);
        border-bottom: 1px solid rgba(255,255,255,0.08);
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .try-label {
        font-size: 11px;
        color: #606880;
        margin-right: 4px;
        flex-shrink: 0;
    }

    .chips-row .stButton > button {
        padding: 5px 14px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 20px !important;
        background: transparent !important;
        font-size: 12px !important;
        color: #A0A8B8 !important;
        height: auto !important;
        min-height: auto !important;
        cursor: pointer !important;
    }

    .chips-row .stButton > button:hover {
        background: rgba(255,255,255,0.05) !important;
        border-color: rgba(255,255,255,0.2) !important;
    }

    /* Zone 12 - Chat input */
    .stChatInput {
        flex: 1 !important;
    }

    .stChatInput > div {
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 21px !important;
        background: #21252D !important;
    }

    .stChatInput input {
        height: 42px !important;
        border: none !important;
        border-radius: 21px !important;
        padding: 0 18px !important;
        font-size: 13px !important;
        background: #21252D !important;
        color: #FAFAFA !important;
    }

    .stChatInput input::placeholder {
        color: #4A5060 !important;
    }

    .stChatInput input:focus {
        border: 1px solid #378ADD !important;
        outline: none !important;
        box-shadow: none !important;
    }

    .stChatInput input:disabled {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
    }

    /* File uploader override */
    .stFileUploader,
    section[data-testid="stSidebar"] .stFileUploader {
        margin: 0 !important;
    }

    .stFileUploader > div,
    section[data-testid="stSidebar"] .stFileUploader > div {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    /* Welcome area */
    .welcome-area {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 40px;
    }

    .welcome-title {
        font-size: 20px;
        font-weight: 500;
        color: #FAFAFA;
        margin-bottom: 12px;
    }

    .welcome-subtitle {
        font-size: 14px;
        color: #A0A8B8;
        margin-bottom: 24px;
    }

    .welcome-steps {
        display: flex;
        flex-direction: column;
        gap: 8px;
        font-size: 13px;
        color: #606880;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state based on JSON specification
if "messages" not in st.session_state:
    st.session_state.messages = []
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "selfheal_count" not in st.session_state:
    st.session_state.selfheal_count = 0
if "last_source" not in st.session_state:
    st.session_state.last_source = None
if "prefill" not in st.session_state:
    st.session_state.prefill = None
if "db_uri" not in st.session_state:
    st.session_state.db_uri = None

# Sidebar Implementation
with st.sidebar:
    # Zone 1 - Sidebar Header
    st.markdown("""
    <div class="sidebar-header">
        <div class="logo-row">
            <div class="icon-box"></div>
            <h4 class="app-title">SQL Chat Agent</h4>
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
        st.markdown('<span class="section-label">Database URL</span>', unsafe_allow_html=True)

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
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")
                table_names = []

        st.markdown('</div>', unsafe_allow_html=True)

    # Demo database setup
    elif source == "demo":
        db_uri = "sqlite:///shop.db"
        table_names = ["customers", "products", "orders"]

    # Update session state
    st.session_state.db_uri = db_uri

    # Zone 5 - Connection status
    if db_uri:
        if source == "demo":
            filename = "shop.db"
        elif source == "upload" and uploaded_file:
            filename = uploaded_file.name
        elif source == "url" and url_input:
            filename = url_input.split("/")[-1] if "/" in url_input else url_input
        else:
            filename = "database.db"

        st.markdown(f"""
        <div class="connection-status">
            <div class="status-row">
                <div class="status-dot"></div>
                <span class="status-text">Connected</span>
            </div>
            <div class="status-filename">{filename}</div>
        </div>
        """, unsafe_allow_html=True)

    # Zone 6 - Tables found
    if table_names:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<span class="section-label">Tables found</span>', unsafe_allow_html=True)

        pills_html = ''.join([f'<span class="table-pill">{table}</span>' for table in table_names])
        st.markdown(f'<div class="tables-pills">{pills_html}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Zone 7 - Session stats
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<span class="section-label">Session</span>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stats-row">
        <div class="metric-card">
            <span class="metric-label">Questions asked</span>
            <span class="metric-value">{st.session_state.question_count}</span>
        </div>
        <div class="metric-card">
            <span class="metric-label">Self-heals</span>
            <span class="metric-value amber">{st.session_state.selfheal_count}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Zone 8 - Clear chat button
    st.markdown('<div class="clear-section">', unsafe_allow_html=True)
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.question_count = 0
        st.session_state.selfheal_count = 0
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Clear chat when switching sources
if source != st.session_state.last_source:
    st.session_state.messages = []
    st.session_state.question_count = 0
    st.session_state.selfheal_count = 0
    st.session_state.last_source = source

# Main Area Implementation

# Zone 9 - Top header
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
                # AI message with structured layout
                st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

                # SQL expander
                if msg.get("sql"):
                    with st.expander("View SQL query"):
                        st.code(msg["sql"], language="sql")

                # Self-heal badge
                if msg.get("attempts", 1) > 1:
                    st.markdown(f"""
                    <div class="selfheal-badge">
                        self-healed · {msg["attempts"]} attempts
                    </div>
                    """, unsafe_allow_html=True)
else:
    # Welcome message when no chat
    if not db_uri:
        st.markdown("""
        <div class="welcome-area">
            <h2 class="welcome-title">Welcome to SQL Chat Agent</h2>
            <p class="welcome-subtitle">Connect to a database to start asking questions in natural language</p>
            <div class="welcome-steps">
                <div>📦 Use the sample shop database for instant access</div>
                <div>📤 Upload your own CSV or SQLite files</div>
                <div>🔗 Connect to remote databases via URL</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Zone 11 - Example chips (only when connected and no messages)
if db_uri and len(st.session_state.messages) == 0:
    example_chips = [
        {"label": "How many customers?", "prefill": "How many customers do we have?"},
        {"label": "Top 5 products?", "prefill": "What are the top 5 most expensive products?"},
        {"label": "Total revenue?", "prefill": "What is the total revenue from all orders?"}
    ]

    cols = [0.5] + [1] * len(example_chips) + [0.5]  # Add padding columns
    columns = st.columns(cols)

    with columns[0]:
        st.markdown('<span class="try-label">Try:</span>', unsafe_allow_html=True)

    for i, chip in enumerate(example_chips):
        with columns[i + 1]:
            if st.button(chip["label"], key=f"chip_{i}", use_container_width=True):
                st.session_state.prefill = chip["prefill"]
                st.rerun()

# Handle prefilled questions
if st.session_state.prefill and db_uri:
    prompt = st.session_state.prefill
    st.session_state.prefill = None

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI response
    with st.spinner("🔮 Analyzing and generating SQL..."):
        result = ask(prompt, db_uri)

    # Update counters
    st.session_state.question_count += 1
    if result.get("attempts", 1) > 1:
        st.session_state.selfheal_count += 1

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
            st.markdown(f"""
            <div class="selfheal-badge">
                self-healed · {result["attempts"]} attempts
            </div>
            """, unsafe_allow_html=True)

    # Update counters
    st.session_state.question_count += 1
    if result.get("attempts", 1) > 1:
        st.session_state.selfheal_count += 1

    # Save to session
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sql": result.get("sql", ""),
        "attempts": result.get("attempts", 1)
    })
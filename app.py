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

# CSS Variables and Complete Layout Styling
st.markdown("""
<style>
    :root {
        --color-background-primary: #ffffff;
        --color-background-secondary: #f8f9fa;
        --color-text-primary: #1f2937;
        --color-text-secondary: #6b7280;
        --color-text-tertiary: #9ca3af;
        --color-border-primary: #378ADD;
        --color-border-secondary: #d1d5db;
        --color-border-tertiary: #e5e7eb;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Reset and base styles */
    .stApp {
        background-color: var(--color-background-primary);
    }

    .main {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* SIDEBAR STYLING - 260px wide */
    .css-1d391kg {
        width: 260px !important;
        min-width: 260px !important;
        max-width: 260px !important;
        padding: 0 !important;
        background-color: var(--color-background-primary) !important;
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

    .sidebar-header-left {
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
        background: #2a4a6f;
        color: #AACCEE;
        border-radius: 10px;
        padding: 2px 8px;
    }

    /* Zone 2-8 - Sidebar sections */
    .sidebar-section {
        background: var(--color-background-primary);
        padding: 14px 16px;
        border-bottom: 1px solid var(--color-border-tertiary);
    }

    .sidebar-section-label {
        font-size: 11px;
        font-weight: 500;
        color: var(--color-text-secondary);
        margin-bottom: 10px;
        display: block;
    }

    /* Radio button styling */
    .stRadio > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        gap: 8px !important;
    }

    .stRadio label {
        font-size: 13px !important;
        color: var(--color-text-primary) !important;
        font-weight: 400 !important;
    }

    .stRadio label:has(input:checked) {
        font-weight: 500 !important;
    }

    /* File uploader styling */
    .upload-box {
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
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23534AB7' viewBox='0 0 24 24'%3E%3Cpath d='M12 4l-8 8h5v8h6v-8h5z'/%3E%3C/svg%3E") center/contain no-repeat;
        margin: 0 auto 8px;
    }

    .upload-text {
        font-size: 12px;
        color: #534AB7;
        margin-bottom: 4px;
    }

    .upload-subtext {
        font-size: 11px;
        color: #7F77DD;
    }

    /* Connection status */
    .connection-status {
        background: #E1F5EE;
        padding: 12px 16px;
        border-bottom: 1px solid var(--color-border-tertiary);
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
        color: #0F6E56;
        font-family: monospace;
    }

    /* Tables found pills */
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

    /* Session stats */
    .stats-container {
        display: flex;
        gap: 8px;
        margin-top: 10px;
    }

    .stat-card {
        background: var(--color-background-primary);
        border: 1px solid var(--color-border-tertiary);
        border-radius: 8px;
        padding: 8px 10px;
        flex: 1;
        text-align: center;
    }

    .stat-label {
        font-size: 10px;
        color: var(--color-text-secondary);
        display: block;
    }

    .stat-number {
        font-size: 22px;
        font-weight: 500;
        color: var(--color-text-primary);
        display: block;
        margin-top: 2px;
    }

    .stat-number.amber {
        color: #854F0B;
    }

    /* Sidebar buttons */
    .css-1d391kg .stButton > button {
        width: 100% !important;
        height: 34px !important;
        background: transparent !important;
        border: 1px solid var(--color-border-secondary) !important;
        border-radius: 6px !important;
        font-size: 12px !important;
        color: var(--color-text-secondary) !important;
        margin-top: 8px !important;
    }

    .css-1d391kg .stButton > button:hover {
        background: var(--color-background-secondary) !important;
    }

    .css-1d391kg .stButton > button.connect-button {
        background: #D85A30 !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    /* Clear button at bottom */
    .clear-section {
        margin-top: auto;
        padding: 14px 16px;
        border-top: 1px solid var(--color-border-tertiary);
    }

    /* MAIN AREA STYLING */
    .main-content {
        display: flex;
        flex-direction: column;
        height: 100vh;
    }

    /* Zone 9 - Top header */
    .main-header {
        background: var(--color-background-primary);
        height: 52px;
        padding: 0 24px;
        border-bottom: 1px solid var(--color-border-tertiary);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .main-title {
        font-size: 16px;
        font-weight: 500;
        color: var(--color-text-primary);
        margin: 0;
    }

    .main-caption {
        font-size: 12px;
        color: var(--color-text-secondary);
        margin: 2px 0 0 0;
    }

    /* Zone 10 - Chat area */
    .chat-container {
        flex: 1;
        background: var(--color-background-primary);
        padding: 20px 24px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    /* Chat messages */
    .stChatMessage {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* User messages - right aligned */
    .stChatMessage:has([alt="👤"]) {
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
        gap: 6px;
    }

    .stChatMessage:has([alt="👤"]) .stChatMessage-content {
        background: #1E3A5F;
        color: #FFFFFF;
        border-radius: 10px 10px 2px 10px;
        padding: 9px 13px;
        max-width: 65%;
        font-size: 13px;
        line-height: 1.5;
    }

    /* AI messages - left aligned */
    .stChatMessage:has([alt="🤖"]) {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        gap: 6px;
    }

    .stChatMessage:has([alt="🤖"]) .stChatMessage-content {
        display: flex;
        flex-direction: column;
        gap: 6px;
        max-width: 82%;
    }

    .ai-bubble {
        background: var(--color-background-secondary);
        color: var(--color-text-primary);
        border-radius: 10px 10px 10px 2px;
        padding: 9px 13px;
        font-size: 13px;
        line-height: 1.5;
    }

    /* SQL Expander */
    .sql-expander {
        border: 1px solid var(--color-border-secondary);
        border-radius: 6px;
        height: 32px;
        padding: 0 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        cursor: pointer;
        background: var(--color-background-primary);
    }

    .sql-expander-text {
        font-size: 11px;
        color: var(--color-text-secondary);
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
    .example-chips {
        background: var(--color-background-secondary);
        height: 44px;
        padding: 0 24px;
        border-top: 1px solid var(--color-border-tertiary);
        border-bottom: 1px solid var(--color-border-tertiary);
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .chips-label {
        font-size: 11px;
        color: var(--color-text-tertiary);
        margin-right: 4px;
    }

    .chip-button {
        padding: 5px 12px;
        border: 1px solid var(--color-border-secondary);
        border-radius: 20px;
        background: var(--color-background-primary);
        font-size: 12px;
        color: var(--color-text-secondary);
        cursor: pointer;
        transition: all 0.2s;
    }

    .chip-button:hover {
        background: var(--color-background-secondary);
        border-color: var(--color-border-primary);
    }

    /* Zone 12 - Chat input */
    .chat-input-container {
        background: var(--color-background-primary);
        height: 60px;
        padding: 0 24px;
        border-top: 1px solid var(--color-border-tertiary);
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .stChatInput {
        flex: 1 !important;
    }

    .stChatInput > div {
        border-radius: 20px !important;
        border: 1px solid var(--color-border-secondary) !important;
    }

    .stChatInput input {
        height: 40px !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0 16px !important;
        font-size: 13px !important;
    }

    .stChatInput input:focus {
        border-color: #378ADD !important;
        box-shadow: 0 0 0 1px #378ADD !important;
    }

    .stChatInput input:disabled {
        background: #f3f4f6 !important;
        color: var(--color-text-tertiary) !important;
    }

    /* Text input styling */
    .stTextInput > div > div > input {
        height: 34px !important;
        border: 1px solid var(--color-border-secondary) !important;
        border-radius: 6px !important;
        padding: 0 10px !important;
        font-size: 12px !important;
    }

    /* File uploader override */
    .stFileUploader {
        margin: 8px 0 0 0 !important;
    }

    .stFileUploader > div {
        border: none !important;
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_source" not in st.session_state:
    st.session_state.last_source = None
if "prefill" not in st.session_state:
    st.session_state.prefill = ""

# Sidebar Layout
with st.sidebar:
    # Zone 1 - Header
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-header-left">
            <div class="sidebar-icon"></div>
            <h4 class="sidebar-title">SQL Chat Agent</h4>
        </div>
        <div class="version-badge">v1.0</div>
    </div>
    """, unsafe_allow_html=True)

    # Zone 2 - Data source selector
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-section-label">Data source</span>', unsafe_allow_html=True)

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
        st.markdown('<span class="sidebar-section-label">Upload file</span>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload file",
            type=["db", "csv"],
            label_visibility="collapsed"
        )

        if uploaded_file:
            db_uri = get_db_uri("upload", uploaded_file)
            file_name = uploaded_file.name
            table_names = [file_name.split('.')[0].replace(" ", "_").lower()]

        st.markdown('</div>', unsafe_allow_html=True)

    # Zone 4 - URL input (conditional)
    elif source == "url":
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<span class="sidebar-section-label">Database URL</span>', unsafe_allow_html=True)

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
        connection_class = "connection-status"
        if source == "demo":
            filename = "shop.db"
        elif source == "upload" and uploaded_file:
            filename = uploaded_file.name
        elif source == "url":
            filename = url_input.split("/")[-1] if url_input else ""
        else:
            filename = ""

        st.markdown(f"""
        <div class="{connection_class}">
            <div class="connection-row">
                <div class="connection-dot"></div>
                <span class="connection-text">Connected</span>
            </div>
            <div class="connection-filename">{filename}</div>
        </div>
        """, unsafe_allow_html=True)

    # Zone 6 - Tables found
    if table_names:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<span class="sidebar-section-label">Tables found</span>', unsafe_allow_html=True)

        pills_html = ''.join([f'<span class="table-pill">{table}</span>' for table in table_names])
        st.markdown(f'<div class="tables-pills">{pills_html}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Zone 7 - Session stats
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-section-label">Session</span>', unsafe_allow_html=True)

    questions_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    heals_count = len([m for m in st.session_state.messages if m["role"] == "assistant" and m.get("attempts", 1) > 1])

    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-card">
            <span class="stat-label">Questions asked</span>
            <span class="stat-number">{questions_count}</span>
        </div>
        <div class="stat-card">
            <span class="stat-label">Self-heals</span>
            <span class="stat-number amber">{heals_count}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Zone 8 - Clear chat button (at bottom)
    st.markdown('<div style="flex: 1;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="clear-section">', unsafe_allow_html=True)
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Clear chat when switching sources
if source != st.session_state.last_source:
    st.session_state.messages = []
    st.session_state.last_source = source

# Main Content Layout
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Zone 9 - Main header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">Ask your database anything</h1>
    <p class="main-caption">Self-healing SQL agent · LangChain + Groq</p>
</div>
""", unsafe_allow_html=True)

# Zone 10 - Chat messages area
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
        if msg["role"] == "user":
            st.markdown(f'<div class="stChatMessage-content">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

            # SQL expander
            if msg.get("sql"):
                with st.expander("🔍 View SQL query"):
                    st.code(msg["sql"], language="sql")

            # Self-heal badge
            if msg.get("attempts", 1) > 1:
                st.markdown(f'<div class="heal-badge">⚡ self-healed · {msg["attempts"]} attempts</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Zone 11 - Example question chips
if db_uri and len(st.session_state.messages) == 0:
    example_questions = ["How many customers?", "Top 5 products?", "Total revenue?"]

    cols = st.columns([1] + [2] * len(example_questions) + [1])
    with cols[0]:
        st.markdown('<span class="chips-label">Try:</span>', unsafe_allow_html=True)

    for i, question in enumerate(example_questions):
        with cols[i + 1]:
            if st.button(question, key=f"chip_{i}", use_container_width=True):
                st.session_state.prefill = question
                st.rerun()

# Handle prefilled questions
if st.session_state.prefill and db_uri:
    prompt = st.session_state.prefill
    st.session_state.prefill = ""

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

# Zone 12 - Chat input
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

            st.markdown(f'<div class="ai-bubble">{result["answer"]}</div>', unsafe_allow_html=True)

            if result.get("sql"):
                with st.expander("🔍 View SQL query"):
                    st.code(result["sql"], language="sql")

            if result.get("attempts", 1) > 1:
                st.markdown(f'<div class="heal-badge">⚡ self-healed · {result["attempts"]} attempts</div>', unsafe_allow_html=True)

        # Save to session
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sql": result.get("sql", ""),
            "attempts": result.get("attempts", 1)
        })
else:
    st.chat_input("Set up a data source on the left first...", disabled=True)

st.markdown('</div>', unsafe_allow_html=True)
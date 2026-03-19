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

# Professional Responsive CSS with meaningful colors
st.markdown("""
<style>
    /* Base styles */
    .main {
        background-color: #0F1419;
    }
    .stApp {
        background-color: #0F1419;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 600;
        color: #1E3A5F;
        margin: 1rem 0;
        text-align: center;
    }
    h4 {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 500;
    }

    /* Brand color buttons - Dark Navy */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 42px;
        background-color: #1E3A5F;
        color: white;
        border: none;
        font-weight: 500;
        transition: all 0.2s ease;
        min-height: 44px; /* Touch-friendly */
    }
    .stButton>button:hover {
        background-color: #2A4A70;
        transform: translateY(-1px);
    }

    /* Success/Connected states - Teal */
    .success-badge {
        background-color: #E1F5EE;
        color: #0F6E56;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: 500;
        display: block;
        text-align: center;
    }

    /* AI/LLM related - Purple */
    .ai-badge {
        background-color: #EEEDFE;
        color: #534AB7;
        padding: 0.3rem 0.8rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
        display: block;
        text-align: center;
    }

    /* Self-heal warning - Amber */
    .heal-badge {
        background-color: #FAEEDA;
        color: #BA7517;
        padding: 0.3rem 0.8rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-block;
        margin: 0.5rem 0;
    }

    /* URL connection - Coral */
    .url-badge {
        background-color: #FAECE7;
        color: #D85A30;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: 500;
        display: block;
        text-align: center;
    }

    /* Chat messages */
    .stChatMessage:has([alt="👤"]) {
        background-color: #1E3A5F !important;
        border-left: 3px solid #2A4A70;
    }
    .stChatMessage:has([alt="🤖"]) {
        background-color: #534AB7 !important;
        border-left: 3px solid #6B5EC7;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background-color: #1E3A5F;
        padding: 0.8rem;
        border-radius: 6px;
        color: white;
    }
    div[data-testid="stMetric"] label {
        color: white !important;
        font-size: 0.8rem !important;
    }
    div[data-testid="stMetric"] div {
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }

    /* Radio buttons */
    .stRadio > div {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 1rem;
    }

    /* Connected indicator */
    .connected-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #0F6E56;
        border-radius: 50%;
        margin-right: 8px;
    }

    /* Example chips */
    .example-chip {
        background-color: rgba(30, 58, 95, 0.3);
        color: #ffffff;
        padding: 0.4rem 0.8rem;
        border-radius: 16px;
        border: 1px solid #1E3A5F;
        font-size: 0.9rem;
        margin: 0.2rem;
        cursor: pointer;
        transition: all 0.2s ease;
        min-height: 40px; /* Touch-friendly */
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .example-chip:hover {
        background-color: #1E3A5F;
    }

    /* Text styling */
    p, .stMarkdown {
        color: #e0e0e0;
    }

    /* Chat input styling */
    .stChatInput {
        margin-top: 1rem;
    }

    /* RESPONSIVE DESIGN */

    /* Desktop (default) - 260px sidebar */
    .css-1d391kg {
        width: 260px;
        min-width: 260px;
        max-width: 260px;
    }

    /* Tablet (768px - 1024px) */
    @media (max-width: 1024px) and (min-width: 768px) {
        .css-1d391kg {
            width: 220px;
            min-width: 220px;
            max-width: 220px;
        }
        .main-header {
            font-size: 1.8rem;
        }
        .stButton>button {
            font-size: 0.9rem;
        }
    }

    /* Mobile (up to 768px) */
    @media (max-width: 768px) {
        /* Sidebar becomes full-width overlay on mobile */
        .css-1d391kg {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
        }

        /* Header adjustments */
        .main-header {
            font-size: 1.5rem;
            margin: 0.5rem 0;
        }

        /* Button adjustments */
        .stButton>button {
            height: 48px; /* Larger touch targets */
            font-size: 0.95rem;
        }

        /* Badge adjustments */
        .success-badge, .url-badge, .ai-badge {
            font-size: 0.85rem;
            padding: 0.6rem 1rem;
        }

        /* Example buttons - stack vertically */
        .example-chip {
            width: 100%;
            margin: 0.3rem 0;
            min-height: 44px;
        }

        /* Chat messages - more padding */
        .stChatMessage {
            margin: 0.5rem 0;
        }

        /* Metrics - larger text */
        div[data-testid="stMetric"] {
            padding: 1rem;
        }
        div[data-testid="stMetric"] label {
            font-size: 0.9rem !important;
        }
        div[data-testid="stMetric"] div {
            font-size: 1.8rem !important;
        }

        /* Radio buttons - more padding */
        .stRadio > div {
            padding: 1.2rem;
        }

        /* File uploader adjustments */
        .stFileUploader {
            margin: 0.5rem 0;
        }

        /* Text input adjustments */
        .stTextInput input {
            height: 48px;
            font-size: 16px; /* Prevents zoom on iOS */
        }
    }

    /* Small mobile (up to 480px) */
    @media (max-width: 480px) {
        .main-header {
            font-size: 1.3rem;
        }

        .stButton>button {
            height: 50px;
            font-size: 1rem;
        }

        /* Stack example buttons vertically with spacing */
        .example-chip {
            min-height: 48px;
            margin: 0.4rem 0;
        }

        /* Larger metrics for readability */
        div[data-testid="stMetric"] div {
            font-size: 2rem !important;
        }

        /* More generous padding */
        .stRadio > div {
            padding: 1.5rem 1rem;
        }
    }

    /* Print styles */
    @media print {
        .css-1d391kg {
            display: none;
        }
        .main-header {
            color: #000;
        }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Data Source Management (260px fixed)
with st.sidebar:
    st.markdown('<h4>🗄️ SQL Chat Agent</h4>', unsafe_allow_html=True)
    st.markdown("---")

    # Source selector
    st.markdown("#### Data Source")
    source = st.radio(
        "Choose your database:",
        options=["demo", "upload", "url"],
        format_func=lambda x: {
            "demo": "📦 Demo Shop DB",
            "upload": "📤 Upload File",
            "url": "🔗 Remote URL"
        }[x],
        label_visibility="visible"
    )

    db_uri = None
    uploaded_file = None

    # Database connection status and info
    if source == "demo":
        st.markdown('<div class="success-badge"><span class="connected-dot"></span>Connected to Shop DB</div>', unsafe_allow_html=True)
        db_uri = "sqlite:///shop.db"
        st.markdown("**Tables:** customers, products, orders")
        st.markdown("**Records:** 50 customers, 20 products, 100 orders")

    elif source == "upload":
        uploaded_file = st.file_uploader(
            "Upload Database/CSV",
            type=["db", "csv"],
            help="SQLite .db files or CSV files"
        )
        if uploaded_file:
            db_uri = get_db_uri("upload", uploaded_file)
            st.markdown(f'<div class="success-badge"><span class="connected-dot"></span>Loaded: {uploaded_file.name}</div>', unsafe_allow_html=True)
        else:
            st.info("📁 Select file to upload")

    elif source == "url":
        url_input = st.text_input(
            "Connection String",
            placeholder="postgresql://user:pass@host/db"
        )
        if url_input:
            db_uri = url_input
            st.markdown('<div class="url-badge"><span class="connected-dot"></span>Remote DB Connected</div>', unsafe_allow_html=True)
        else:
            st.info("🔗 Enter database URL")

    st.markdown("---")

    # Session statistics
    st.markdown("#### Session Stats")
    if "messages" in st.session_state:
        questions = len([m for m in st.session_state.messages if m["role"] == "user"])
        healed = len([m for m in st.session_state.messages if m["role"] == "assistant" and m.get("attempts", 1) > 1])
    else:
        questions = healed = 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Questions", questions)
    with col2:
        st.metric("Self-Healed", healed)

    # Show self-healing status
    if healed > 0:
        st.markdown('<div class="heal-badge">⚡ Self-Healing Active</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ai-badge">🤖 Ready · 3 Retries</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Built with LangChain + Groq")

# Main Chat Area
st.markdown('<h1 class="main-header">Ask your database anything</h1>', unsafe_allow_html=True)
st.markdown("Natural language SQL queries with self-healing AI")

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
                with st.expander("📄 View SQL Query"):
                    st.code(msg["sql"], language="sql")

            # Self-heal badge (only if attempts > 1)
            if msg.get("attempts", 1) > 1:
                st.markdown(f'<div class="heal-badge">⚡ Self-healed · {msg["attempts"]} attempts</div>', unsafe_allow_html=True)

# Example question chips (only show if demo database and no chat history)
if source == "demo" and len(st.session_state.messages) == 0:
    st.markdown("#### 💡 Try These Examples")

    example_questions = [
        "How many customers do we have?",
        "Top 5 most expensive products",
        "Which city has most customers?",
        "Total revenue from orders"
    ]

    # Responsive layout: columns on desktop, stacked on mobile
    # Check if we should use mobile layout (this is a simple approach)
    # On mobile, we'll create single column layout
    use_mobile_layout = True  # We'll assume mobile-first approach

    if use_mobile_layout:
        # Mobile layout: stack vertically
        for i, question in enumerate(example_questions):
            if st.button(question, key=f"example_{i}", use_container_width=True):
                st.session_state.example_clicked = question
    else:
        # Desktop layout: use columns (fallback)
        cols = st.columns(len(example_questions))
        for i, question in enumerate(example_questions):
            with cols[i]:
                if st.button(question, key=f"example_{i}"):
                    st.session_state.example_clicked = question

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
                with st.expander("📄 View SQL Query"):
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
    st.info("👈 Connect to a database in the sidebar to start chatting")

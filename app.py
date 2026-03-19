import streamlit as st
from agent import ask, get_db_uri

st.set_page_config(
    page_title="SQL Chat Agent",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* ── Global ── */
html, body, [data-testid="stApp"] {
    background-color: #0E1117;
    font-family: Inter, sans-serif;
}

/* ── Sidebar background ── */
[data-testid="stSidebar"] {
    background-color: #161920;
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] > div:first-child {
    padding: 0;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; }

/* ── Radio buttons ── */
[data-testid="stRadio"] label {
    font-size: 13px !important;
    color: #FAFAFA !important;
}
[data-testid="stRadio"] > div { gap: 8px; }

/* ── All sidebar text ── */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #A0A8B8;
}

/* ── Inputs ── */
input, textarea {
    background-color: #21252D !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 6px !important;
    color: #FAFAFA !important;
    font-size: 13px !important;
}
input:focus, textarea:focus {
    border-color: #378ADD !important;
    box-shadow: none !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: #161920;
    border-top: 1px solid rgba(255,255,255,0.08);
    padding: 12px 24px;
}
[data-testid="stChatInput"] textarea {
    background: #21252D !important;
    border-radius: 21px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #FAFAFA !important;
    font-size: 13px !important;
    padding: 10px 18px !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 4px 24px !important;
}

/* ── User bubble ── */
[data-testid="stChatMessage"][data-testid*="user"] .stMarkdown p {
    background: #1E3A5F;
    color: #FFFFFF;
    border-radius: 12px 12px 2px 12px;
    padding: 10px 14px;
    display: inline-block;
    font-size: 13px;
    line-height: 1.5;
    max-width: 65%;
}

/* ── Buttons ── */
[data-testid="stButton"] button {
    background: transparent;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    color: #A0A8B8;
    font-size: 12px;
    padding: 5px 14px;
    transition: all 0.15s;
}
[data-testid="stButton"] button:hover {
    background: rgba(255,255,255,0.05);
    border-color: rgba(255,255,255,0.2);
    color: #FAFAFA;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #21252D !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary {
    color: #A0A8B8 !important;
    font-size: 11px !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #21252D;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 10px 12px;
}
[data-testid="stMetricLabel"] { font-size: 10px !important; color: #A0A8B8 !important; }
[data-testid="stMetricValue"] { font-size: 22px !important; color: #FAFAFA !important; }

/* ── Success/error boxes ── */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    font-size: 12px !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 1.5px dashed #7F77DD !important;
    border-radius: 8px !important;
    background: rgba(83,74,183,0.08) !important;
    padding: 12px !important;
}
[data-testid="stFileUploader"] label { color: #534AB7 !important; font-size: 12px !important; }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* ── Code blocks ── */
code { color: #5DCAA5 !important; background: #161920 !important; font-size: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
for key, val in {
    "messages": [],
    "question_count": 0,
    "selfheal_count": 0,
    "last_source": None,
    "prefill": None,
    "db_uri": None,
    "connected_tables": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:

    # Header
    st.markdown("""
    <div style="
        background:#1E3A5F;
        padding:14px 16px;
        margin:-1rem -1rem 0 -1rem;
        display:flex;
        align-items:center;
        justify-content:space-between;
        border-bottom:1px solid rgba(255,255,255,0.1);
    ">
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:28px;height:28px;background:#378ADD;border-radius:6px;"></div>
            <span style="font-size:15px;font-weight:500;color:#FFFFFF;">SQL Chat Agent</span>
        </div>
        <span style="font-size:10px;font-weight:500;color:#AACCEE;background:#2a4a6f;
                     border-radius:10px;padding:2px 8px;">v1.0</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Source selector
    st.markdown("<p style='font-size:11px;font-weight:500;color:#A0A8B8;margin-bottom:6px;'>Data source</p>", unsafe_allow_html=True)
    source = st.radio(
        "",
        options=["demo", "upload", "url"],
        format_func=lambda x: {
            "demo":   "Use sample shop database",
            "upload": "Upload my own file (.db or .csv)",
            "url":    "Connect via database URL"
        }[x],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='margin:12px 0'>", unsafe_allow_html=True)

    # Clear chat on source switch
    if source != st.session_state.last_source:
        st.session_state.messages = []
        st.session_state.last_source = source
        st.session_state.db_uri = None
        st.session_state.connected_tables = []

    uploaded_file = None

    # Demo
    if source == "demo":
        st.session_state.db_uri = "sqlite:///shop.db"
        try:
            from langchain_community.utilities import SQLDatabase
            db = SQLDatabase.from_uri("sqlite:///shop.db")
            st.session_state.connected_tables = db.get_usable_table_names()
        except:
            st.session_state.connected_tables = ["customers", "orders", "products"]

    # Upload
    elif source == "upload":
        st.markdown("<p style='font-size:11px;font-weight:500;color:#A0A8B8;margin-bottom:6px;'>Upload file</p>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["db", "csv"], label_visibility="collapsed")
        if uploaded_file:
            uri = get_db_uri("upload", uploaded_file)
            st.session_state.db_uri = uri
            try:
                from langchain_community.utilities import SQLDatabase
                db = SQLDatabase.from_uri(uri)
                st.session_state.connected_tables = db.get_usable_table_names()
            except:
                st.session_state.connected_tables = []

    # URL
    elif source == "url":
        st.markdown("<p style='font-size:11px;font-weight:500;color:#A0A8B8;margin-bottom:6px;'>Database URL</p>", unsafe_allow_html=True)
        url_input = st.text_input("", placeholder="sqlite:///mydb.db", label_visibility="collapsed")
        if st.button("Connect", use_container_width=True):
            if url_input:
                st.session_state.db_uri = url_input
                try:
                    from langchain_community.utilities import SQLDatabase
                    db = SQLDatabase.from_uri(url_input)
                    st.session_state.connected_tables = db.get_usable_table_names()
                except Exception as e:
                    st.error(f"Could not connect: {e}")
                    st.session_state.db_uri = None

    st.markdown("<hr style='margin:12px 0'>", unsafe_allow_html=True)

    # Connection status
    if st.session_state.db_uri:
        db_name = st.session_state.db_uri.split("///")[-1] if "///" in st.session_state.db_uri else st.session_state.db_uri
        st.markdown(f"""
        <div style="background:rgba(15,110,86,0.15);border-radius:8px;padding:10px 12px;margin-bottom:12px;">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
                <div style="width:8px;height:8px;border-radius:50%;background:#0F6E56;flex-shrink:0;"></div>
                <span style="font-size:12px;font-weight:500;color:#5DCAA5;">Connected</span>
            </div>
            <span style="font-size:11px;font-family:monospace;color:#0F6E56;">{db_name}</span>
        </div>
        """, unsafe_allow_html=True)

        # Table pills
        if st.session_state.connected_tables:
            st.markdown("<p style='font-size:11px;font-weight:500;color:#A0A8B8;margin-bottom:6px;'>Tables found</p>", unsafe_allow_html=True)
            pills_html = "<div style='display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px;'>"
            for t in st.session_state.connected_tables:
                pills_html += f"""<span style="font-size:11px;padding:3px 10px;border-radius:10px;
                    background:rgba(15,110,86,0.15);color:#5DCAA5;
                    border:1px solid rgba(93,202,165,0.3);">{t}</span>"""
            pills_html += "</div>"
            st.markdown(pills_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:10px 12px;margin-bottom:12px;">
            <div style="display:flex;align-items:center;gap:6px;">
                <div style="width:8px;height:8px;border-radius:50%;background:#606880;flex-shrink:0;"></div>
                <span style="font-size:12px;color:#606880;">Not connected</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:12px 0'>", unsafe_allow_html=True)

    # Session stats
    st.markdown("<p style='font-size:11px;font-weight:500;color:#A0A8B8;margin-bottom:8px;'>Session</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Questions asked", st.session_state.question_count)
    with c2:
        st.metric("Self-heals", st.session_state.selfheal_count)

    # Push clear button to bottom
    st.markdown("<div style='flex:1;min-height:40px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin:12px 0'>", unsafe_allow_html=True)
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.question_count = 0
        st.session_state.selfheal_count = 0
        st.rerun()

# ── MAIN AREA ─────────────────────────────────────────────────────────────────

# Header bar
st.markdown("""
<div style="
    background:#161920;
    border-bottom:1px solid rgba(255,255,255,0.08);
    padding:14px 24px;
">
    <div style="font-size:16px;font-weight:500;color:#FAFAFA;line-height:1.2;">
        Ask your database anything
    </div>
    <div style="font-size:12px;color:#A0A8B8;margin-top:3px;">
        Self-healing SQL agent &nbsp;·&nbsp; LangChain + Groq
    </div>
</div>
""", unsafe_allow_html=True)

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-end;">
                <div style="background:#1E3A5F;color:#FFFFFF;border-radius:12px 12px 2px 12px;
                            padding:10px 14px;max-width:65%;font-size:13px;line-height:1.5;">
                    {msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Answer bubble
            st.markdown(f"""
            <div style="background:#21252D;color:#FAFAFA;border-radius:2px 12px 12px 12px;
                        padding:10px 14px;font-size:13px;line-height:1.5;
                        display:inline-block;max-width:82%;">
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)

            # SQL expander
            if msg.get("sql"):
                with st.expander("View SQL query"):
                    st.code(msg["sql"], language="sql")

            # Self-heal badge
            if msg.get("attempts", 1) > 1:
                st.markdown(f"""
                <div style="background:rgba(186,117,23,0.12);border:1px solid rgba(239,159,39,0.4);
                            border-radius:8px;padding:6px 14px;margin-top:4px;display:inline-block;">
                    <span style="font-size:11px;font-weight:500;color:#BA7517;">
                        self-healed &nbsp;·&nbsp; {msg['attempts']} attempts
                    </span>
                </div>
                """, unsafe_allow_html=True)

# Example chips row
st.markdown("<hr style='margin:8px 0;border-color:rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
st.markdown("""
<div style="padding:0 0 6px 0;">
    <span style="font-size:11px;color:#606880;">Try asking:</span>
</div>
""", unsafe_allow_html=True)

chip_col1, chip_col2, chip_col3 = st.columns(3)
chips = [
    ("How many customers?",  "How many customers do we have?"),
    ("Top 5 products?",      "What are the top 5 most expensive products?"),
    ("Total revenue?",       "What is the total revenue from all orders?"),
]
for col, (label, prefill) in zip([chip_col1, chip_col2, chip_col3], chips):
    with col:
        if st.button(label, use_container_width=False):
            st.session_state.prefill = prefill
            st.rerun()

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# Chat input
db_uri = st.session_state.db_uri
placeholder = "Ask a question about your data..." if db_uri else "Set up a data source on the left first..."
prompt = st.chat_input(placeholder, disabled=not db_uri)

# Handle prefill from chips
if st.session_state.prefill and db_uri:
    prompt = st.session_state.prefill
    st.session_state.prefill = None

# Handle new message
if prompt and db_uri:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.question_count += 1

    with st.chat_message("user"):
        st.markdown(f"""
        <div style="display:flex;justify-content:flex-end;">
            <div style="background:#1E3A5F;color:#FFFFFF;border-radius:12px 12px 2px 12px;
                        padding:10px 14px;max-width:65%;font-size:13px;line-height:1.5;">
                {prompt}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = ask(prompt, db_uri)

        # Answer bubble
        st.markdown(f"""
        <div style="background:#21252D;color:#FAFAFA;border-radius:2px 12px 12px 12px;
                    padding:10px 14px;font-size:13px;line-height:1.5;
                    display:inline-block;max-width:82%;">
            {result['answer']}
        </div>
        """, unsafe_allow_html=True)

        # SQL expander
        if result.get("sql"):
            with st.expander("View SQL query"):
                st.code(result["sql"], language="sql")

        # Self-heal badge
        if result.get("attempts", 1) > 1:
            st.session_state.selfheal_count += 1
            st.markdown(f"""
            <div style="background:rgba(186,117,23,0.12);border:1px solid rgba(239,159,39,0.4);
                        border-radius:8px;padding:6px 14px;margin-top:4px;display:inline-block;">
                <span style="font-size:11px;font-weight:500;color:#BA7517;">
                    self-healed &nbsp;·&nbsp; {result['attempts']} attempts
                </span>
            </div>
            """, unsafe_allow_html=True)

    # Save to history
    st.session_state.messages.append({
        "role":     "assistant",
        "content":  result["answer"],
        "sql":      result.get("sql", ""),
        "attempts": result.get("attempts", 1)
    })
    st.rerun()
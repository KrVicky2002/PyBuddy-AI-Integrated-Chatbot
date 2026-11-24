
import streamlit as st

from database.db import initialize_database

from database.models import (
    create_conversation,
    get_all_conversations,
    save_message,
    get_messages,
    update_conversation_title
)

from utils.helpers import generate_title
from core.chatbot import get_response


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="PyBuddy - Python AI Tutor",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)



# ==========================================
# 2. CUSTOM CSS - LIGHT THEME
# ==========================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #fff !important;
    min-height: 100vh;}

/* Main content */
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
}

/* Sidebar branding */
.sidebar-logo {
    font-size: 27px;
    font-weight: 750;
    color: #172554;
    letter-spacing: -1px;
    margin-bottom: 3px;
}

.sidebar-subtitle {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 25px;
}

/* Main heading */
.main-heading {
    font-size: 34px;
    font-weight: 750;
    color: #172554;
    letter-spacing: -1px;
    margin-bottom: 5px;
}

.main-subheading {
    color: #64748b;
    font-size: 15px;
    margin-bottom: 30px;
}

/* Welcome section */
.welcome-container {
    text-align: center;
    padding: 65px 15px 35px 15px;
}

.welcome-icon {
    font-size: 55px;
    margin-bottom: 15px;
}

.welcome-title {
    font-size: 29px;
    font-weight: 700;
    color: #172554;
    margin-bottom: 10px;
}

.welcome-description {
    color: #64748b;
    font-size: 15px;
    line-height: 1.7;
}

/* Suggestion cards */
.suggestion-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 17px;
    min-height: 100px;
    margin-bottom: 10px;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
}

.suggestion-title {
    color: #1e293b;
    font-weight: 600;
    font-size: 14px;
    margin-bottom: 7px;
}

.suggestion-description {
    color: #64748b;
    font-size: 12px;
    line-height: 1.6;
}

/* Buttons */
.stButton > button {
    border-radius: 9px;
    font-weight: 550;
    transition: 0.2s ease;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
    padding: 17px;
    margin-bottom: 16px;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
}


/* ==========================================
   CHAT INPUT COMPOSER
========================================== */

/* Main input container */
[data-testid="stChatInput"] {
    background-color: #ffffff !important;
    border: 1px solid #dbe3ef !important;
    border-radius: 16px !important;
    padding: 5px !important;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.06);
    transition: all 0.2s ease;
}

/* Input focus effect */
[data-testid="stChatInput"]:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12);
}

/* Text input */
[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    color: #1e293b !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    padding: 12px !important;
}

/* Placeholder */
[data-testid="stChatInput"] textarea::placeholder {
    color: #94a3b8 !important;
    opacity: 1;
}

/* Send button */
[data-testid="stChatInput"] button {
    background-color: #4f46e5 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    border: none !important;
    transition: background-color 0.2s ease;
}

/* Send button hover */
[data-testid="stChatInput"] button:hover {
    background-color: #4338ca !important;
}

/* Bottom composer area */
[data-testid="stBottom"] {
    background-color: #f1f5f9 !important;
}

/* Composer spacing */
[data-testid="stBottom"] [data-testid="stChatInput"] {
    margin-bottom: 8px;
}

/* Code blocks */
[data-testid="stCode"] {
    border-radius: 10px;
}


/* Sidebar history buttons 
section[data-testid="stSidebar"] .stButton > button {
    text-align: left;
    justify-content: flex-start;
}
*/

/* ==========================================
   SIDEBAR POLISH
========================================== */

/* Sidebar spacing */
section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h3 {
    color: #334155;
    font-size: 15px;
    font-weight: 700;
    margin-top: 15px;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton > button {
    border-radius: 9px;
    padding: 9px 12px;
    font-size: 13px;
    transition: all 0.2s ease;
}

/* Sidebar button hover */
section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #eef2ff;
    border-color: #c7d2fe;
    color: #3730a3;
}

/* Sidebar divider */
section[data-testid="stSidebar"] hr {
    border-color: #e2e8f0;
}


/* Footer */
.app-footer {
    color: #94a3b8;
    text-align: center;
    font-size: 12px;
    padding: 15px;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ==========================================
   RESPONSIVE DESIGN
========================================== */

/* Tablets and smaller screens */
@media screen and (max-width: 768px) {

    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 6rem;
    }

    .main-heading {
        font-size: 27px;
    }

    .main-subheading {
        font-size: 13px;
    }

    .welcome-container {
        padding: 40px 8px 25px 8px;
    }

    .welcome-title {
        font-size: 23px;
    }

    .welcome-description {
        font-size: 13px;
    }

    .welcome-icon {
        font-size: 45px;
    }

    .suggestion-card {
        padding: 12px;
        min-height: 110px;
    }

    [data-testid="stChatMessage"] {
        padding: 12px;
    }
}

/* Small mobile screens */
@media screen and (max-width: 480px) {

    .main-heading {
        font-size: 24px;
    }

    .welcome-title {
        font-size: 21px;
    }

    .suggestion-title {
        font-size: 12px;
    }

    .suggestion-description {
        font-size: 11px;
    }
}


</style>
""", unsafe_allow_html=True)



# ==========================================
# 3. DATABASE INITIALIZATION
# ==========================================

initialize_database()


# ==========================================
# 4. SIDEBAR BRANDING
# ==========================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-logo">🐍 PyBuddy</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">Your Personal Python AI Tutor</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # New Chat button
    if st.button(
        "＋  New Chat",
        use_container_width=True,
        type="primary"
    ):

        new_chat_id = create_conversation()

        st.session_state.active_conversation_id = new_chat_id

        st.rerun()

    st.markdown("### Your Conversations")


# ==========================================
# 5. INITIALIZE ACTIVE CONVERSATION
# ==========================================

conversations = get_all_conversations()

if not conversations:

    create_conversation()

    conversations = get_all_conversations()


conversation_ids = [
    chat["id"] for chat in conversations
]


if (
    "active_conversation_id" not in st.session_state
    or st.session_state.active_conversation_id not in conversation_ids
):

    st.session_state.active_conversation_id = conversations[0]["id"]


# ==========================================
# 6. DISPLAY CHAT HISTORY
# ==========================================

with st.sidebar:

    if not conversations:

        st.caption("No conversations yet.")

    for chat in conversations:

        chat_id = chat["id"]
        chat_title = chat["title"]

        is_active = (
            chat_id == st.session_state.active_conversation_id
        )

        button_label = (
            f"●  {chat_title}"
            if is_active
            else f"   {chat_title}"
        )

        if st.button(
            button_label,
            key=f"chat_{chat_id}",
            use_container_width=True,
            type="secondary" if is_active else "tertiary"
        ):

            st.session_state.active_conversation_id = chat_id

            st.rerun()

    st.divider()

    st.caption("🐍 Built for Python learners")


# ==========================================
# 7. LOAD ACTIVE CONVERSATION
# ==========================================

messages = get_messages(
    st.session_state.active_conversation_id
)


# ==========================================
# 8. MAIN APPLICATION HEADER
# ==========================================

st.markdown(
    '<div class="main-heading">PyBuddy 🐍</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subheading">'
    'Your AI-powered companion for learning Python programming.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 9. WELCOME SCREEN
# ==========================================

if not messages:

    st.markdown("""
    <div class="welcome-container">

        <div class="welcome-icon">🐍</div>

        <div class="welcome-title">
            Hey there, Python Learner!
        </div>

        <div class="welcome-description">
            I'm PyBuddy. Let's learn Python together.
            <br>
            Ask me anything about Python programming.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("### What would you like to learn today?")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="suggestion-card">
            <div class="suggestion-title">
                🧱 Python Fundamentals
            </div>
            <div class="suggestion-description">
                Learn variables, data types and operators.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="suggestion-card">
            <div class="suggestion-title">
                🔁 Loops and Conditions
            </div>
            <div class="suggestion-description">
                Understand if statements, for loops and while loops.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="suggestion-card">
            <div class="suggestion-title">
                📦 Python Data Structures
            </div>
            <div class="suggestion-description">
                Explore lists, tuples, sets and dictionaries.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="suggestion-card">
            <div class="suggestion-title">
                🛠️ Debug Python Code
            </div>
            <div class="suggestion-description">
                Understand errors and improve your code.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# 10. DISPLAY CHAT MESSAGES
# ==========================================

for message in messages:

    if message["role"] == "user":

        avatar = "🧑‍💻"

    else:

        avatar = "🐍"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):

        st.markdown(message["content"])


# ==========================================
# 11. ACCEPT USER INPUT
# ==========================================

user_input = st.chat_input(
    "Ask To PyBuddy anything about Python...",
    max_chars=5000
)

if user_input:

    conversation_id = st.session_state.active_conversation_id

    # Check first message
    existing_messages = get_messages(conversation_id)

    is_first_message = len(existing_messages) == 0


    # Save user message
    save_message(
        conversation_id,
        "user",
        user_input
    )


    # Generate conversation title
    if is_first_message:

        title = generate_title(user_input)

        update_conversation_title(
            conversation_id,
            title
        )


    # Load conversation history
    stored_messages = get_messages(conversation_id)

    conversation_history = [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in stored_messages
    ]


    # Generate AI response
    try:

        with st.spinner("🐍 PyBuddy is preparing your answer..."):

            response = get_response(conversation_history)


        # Save assistant response
        save_message(
            conversation_id,
            "assistant",
            response
        )

        st.rerun()


    except Exception as e:

        st.error(
            "Unable to generate a response. "
            "Please try again in a moment."
        )

        st.caption(f"Technical details: {type(e).__name__}: {e}")


# ==========================================
# 12. FOOTER
# ==========================================

st.markdown("""
<div class="app-footer">
    <strong>🐍 PyBuddy</strong>
    <br>
    Your Personal Python AI Tutor
    <br>
    Built with Python • Streamlit • OpenRouter
</div>
""", unsafe_allow_html=True)
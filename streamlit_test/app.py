import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import pyrebase
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Firebase Configuration
firebase_config = {
    "apiKey": "AIzaSyC5-7v26XWgI3r18Tj5zvhJlpuM4AyF_xI",
    "authDomain": "baby-parent1.firebaseapp.com",
    "databaseURL": "https://baby-parent1-default-rtdb.firebaseio.com/",
    "projectId": "baby-parent1",
    "storageBucket": "baby-parent1.firebasestorage.app",
    "messagingSenderId": "373278045842",
    "appId": "1:373278045842:web:84ef5cb7d1532e24cc984b",
    "measurementId": "G-VY9G9TRJMR"
}

# ==================================================
# SSL CERTIFICATE FIX (For Corporate/Proxy Networks)
# ==================================================
# Suppress SSL warnings and disable verification to fix "self-signed certificate" errors
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
original_session_request = requests.Session.request
def patched_request(self, method, url, *args, **kwargs):
    kwargs['verify'] = False
    return original_session_request(self, method, url, *args, **kwargs)
requests.Session.request = patched_request

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def find_best_match(df, text):
    if df is not None and not df.empty:
        return 100, df.iloc[0]
    return 0, None

def validate_email(email):
    """Validate email format using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# ==================================================
# PROFESSIONAL THEME & CONFIG
# ==================================================
st.set_page_config(page_title="Quest of Growth | Professional Edition", layout="wide")

# ==================================================
# LOGIC & SESSION STATE (Initialize before use)
# ==================================================
if "total_xp" not in st.session_state: st.session_state.total_xp = 0
if "task_status" not in st.session_state: st.session_state.task_status = {}
if "user_name" not in st.session_state: st.session_state.user_name = "Voyager"
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = ""

# Place this exactly after st.set_page_config
# Place this exactly after st.set_page_config
st.markdown("""
<style>
    /* Hide the default Streamlit sidebar toggle (<<) always */
    [data-testid="collapsedControl"], 
    button[kind="headerNoPadding"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Sidebar Navigation Styling */
    section[data-testid="stSidebar"] .stRadio label {
        background: white;
        padding: 12px 15px;
        border-radius: 10px;
        border: 1px solid #f0f0f0;
        margin-bottom: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: transform 0.2s, border-color 0.2s;
        cursor: pointer;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        transform: translateX(4px);
        border-color: #d4af37;
        color: #d4af37;
    }
    /* Hide the radio circle to make it look like a button list */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child {
        display: none;
    }
</style>
""", unsafe_allow_html=True)


if st.session_state.logged_in:
    components.html("""
    <script>
        const parentDoc = window.parent.document;
        
        if (!parentDoc.getElementById('gemini-hamburger')) {
            const btn = parentDoc.createElement('button');
            btn.id = 'gemini-hamburger';
            btn.innerHTML = '☰';
            
            Object.assign(btn.style, {
                position: 'fixed',
                top: '12px',
                left: '16px',
                zIndex: '1000001',
                cursor: 'pointer',
                fontSize: '24px',
                background: 'none',
                border: 'none',
                color: '#d4af37',
                padding: '4px 8px',
                outline: 'none'
            });

            btn.onclick = function() {
                const sidebarBtn = parentDoc.querySelector('button[kind="headerNoPadding"]');
                if (sidebarBtn) sidebarBtn.click();
            };

            parentDoc.body.appendChild(btn);
        } else {
            // Ensure it is visible if it already exists
            parentDoc.getElementById('gemini-hamburger').style.display = 'block';
        }
    </script>
    """, height=0)


# ==================================================
# LANDING PAGE & AUTHENTICATION
# ==================================================
if not st.session_state.logged_in:
    # Initialize auth page state
    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "landing"  # landing, login, register

    # Landing Page
    if st.session_state.auth_page == "landing":
        st.markdown("""
        <style>
        .landing-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 80vh;
            flex-direction: column;
            text-align: center;
        }
        .landing-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 50px;
            border-radius: 15px;
            border: 2px solid #000000;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            width: 100%;
        }
        .landing-title {
            color: #000000 !important;
            font-size: 2.5rem;
            margin-bottom: 20px;
        }
        .landing-subtitle {
            color: #333333;
            font-size: 1.2rem;
            margin-bottom: 40px;
            line-height: 1.6;
        }
        .feature-list {
            text-align: left;
            margin: 30px 0;
            color: #555555;
        }
        .feature-list li {
            margin: 10px 0;
            padding-left: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<h1 class="landing-title">🌱 Quest of Growth</h1>', unsafe_allow_html=True)
        st.markdown('<p class="landing-subtitle">Your comprehensive guide to child development and parenting milestones</p>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.write("")  # Spacer
        with col2:
            if st.button("🔐 Login", key="go_to_login", use_container_width=True):
                st.session_state.auth_page = "login"
                st.rerun()
            if st.button("📝 Register", key="go_to_register", use_container_width=True):
                st.session_state.auth_page = "register"
                st.rerun()
        with col3:
            st.write("")  # Spacer

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Login Page
    elif st.session_state.auth_page == "login":
        st.markdown("""
        <style>
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }
        .login-form {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 10px;
            border: 2px solid #000000;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 450px;
            width: 100%;
            text-align: center;
        }
        .login-title {
            color: #000000 !important;
            margin-bottom: 10px;
            font-size: 1.8rem;
        }
        .login-subtitle {
            color: #333333;
            margin-bottom: 20px;
            font-size: 0.9rem;
        }
        .auth-methods {
            text-align: left;
            margin: 20px 0;
            font-size: 0.85rem;
            color: #555555;
        }
        .auth-methods h4 {
            margin-bottom: 10px;
            color: #000000;
        }
        .auth-methods ul {
            margin: 0;
            padding-left: 20px;
        }
        .auth-methods li {
            margin: 5px 0;
        }
        </style>
        """, unsafe_allow_html=True)

      

        st.markdown('<h1 class="login-title">🔐 Login to Quest of Growth</h1>', unsafe_allow_html=True)

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", key="login_btn", use_container_width=True):
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                try:
                    user = auth.sign_in_with_email_and_password(email.strip(), password)
                    st.session_state.logged_in = True
                    st.session_state.user_email = email.strip()
                    st.success("Login successful!")
                    st.rerun()
                except Exception as e:
                    error_msg = str(e)
                    if "INVALID_EMAIL" in error_msg:
                        st.error("Invalid email format. Please check your email address.")
                    elif "INVALID_LOGIN_CREDENTIALS" in error_msg:
                        st.error("Incorrect email or password.")
                    elif "EMAIL_NOT_FOUND" in error_msg:
                        st.error("No account found with this email.")
                    elif "INVALID_PASSWORD" in error_msg:
                        st.error("Incorrect password.")
                    else:
                        st.error(f"Login failed: {error_msg}")

        st.markdown('<p style="text-align: center; margin: 20px 0; color: #555555;">Don\'t have an account?</p>', unsafe_allow_html=True)
        if st.button("📝 Register", key="go_to_register_from_login", use_container_width=True):
            st.session_state.auth_page = "register"
            st.rerun()

        if st.button("← Back to Home", key="back_to_landing_from_login"):
            st.session_state.auth_page = "landing"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Register Page
    elif st.session_state.auth_page == "register":
        st.markdown("""
        <style>
        .register-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }
        .register-form {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 10px;
            border: 2px solid #000000;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 450px;
            width: 100%;
            text-align: center;
        }
        .register-title {
            color: #000000 !important;
            margin-bottom: 10px;
            font-size: 1.8rem;
        }
        .register-subtitle {
            color: #333333;
            margin-bottom: 20px;
            font-size: 0.9rem;
        }
        .auth-methods {
            text-align: left;
            margin: 20px 0;
            font-size: 0.85rem;
            color: #555555;
        }
        .auth-methods h4 {
            margin-bottom: 10px;
            color: #000000;
        }
        .auth-methods ul {
            margin: 0;
            padding-left: 20px;
        }
        .auth-methods li {
            margin: 5px 0;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<h1 class="register-title">📝 Register for Quest of Growth</h1>', unsafe_allow_html=True)

        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password (min 6 characters)", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

        if st.button("Create Account", key="register_btn", use_container_width=True):
            if not email or not password:
                st.error("Please enter both email and password.")
            elif not validate_email(email):
                st.error("Please enter a valid email address.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    st.success("Account created successfully! Please log in.")
                    st.session_state.auth_page = "login"
                    st.rerun()
                except Exception as e:
                    error_message = str(e)
                    if "EMAIL_EXISTS" in error_message:
                        st.error("This email is already registered. Please use the Login button instead.")
                    else:
                        st.error(f"Registration failed: {error_message}")

        st.markdown('<p style="text-align: center; margin: 20px 0; color: #555555;">Already have an account?</p>', unsafe_allow_html=True)
        if st.button("🔐 Login", key="go_to_login_from_register", use_container_width=True):
            st.session_state.auth_page = "login"
            st.rerun()

        if st.button("← Back to Home", key="back_to_landing_from_register"):
            st.session_state.auth_page = "landing"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()  # Stop execution if not logged in

# ==================================================
# DATASETS: DETAILED DEVELOPMENTAL DESCRIPTIONS
# ==================================================
PARENT_DESCRIPTIONS = {
    # 0-2Y
    "Monitor sleep cycles": "Scientific sleep monitoring involves tracking REM and Non-REM cycles. During deep sleep, the pituitary gland releases growth hormones essential for physical development, while REM sleep supports cognitive processing and memory consolidation.",
    "Introduction to solids": "This transition marks the development of jaw muscles and introduce critical micronutrients like Iron and Zinc, which support neurological growth during the first 1000 days of life.",
    "Sensory play": "Stimulating the five senses helps build nerve connections in the brain's pathways, which lead to the child's ability to complete more complex learning tasks later in life.",
    "Language mirroring": "By reflecting sounds, you are reinforcing the 'Serve and Return' interaction style, which is foundational for social-emotional development and future communication skills.",
    
    # 3-5Y
    "Social coaching": "Guiding children through peer interactions helps them understand social cues and cooperative play, which are essential for developing empathy and conflict-resolution skills.",
    "Emotional labels": "Teaching children to name their emotions helps build the prefrontal cortex's ability to regulate the amygdala, reducing tantrums and increasing emotional intelligence.",
    "Creative art": "Artistic expression at this stage develops fine motor skills and symbolic thinking, allowing children to represent their internal world through external media.",
    "Hygiene": "Establishing consistent hygiene routines builds autonomy and physiological awareness, helping children transition from dependent care to self-regulation.",
    
    # 6-12Y
    "Study habits": "Establishing structured learning environments encourages the development of executive functions like planning, focus, and task initiation.",
    "Digital safety": "Introducing digital literacy ensures children understand the boundaries of the internet, focusing on privacy, cyber-ethics, and healthy screen usage.",
    "Friendships": "Supporting deeper peer bonds helps children navigate complex social hierarchies and loyalty, which are vital for long-term psychological well-being.",
    "Financial basics": "Introducing the concepts of saving and delayed gratification builds the foundational cognitive frameworks for economic responsibility and mathematical logic.",
    
    # 13-25Y
    "Career paths": "Facilitating exploration of vocational interests helps the adolescent brain narrow its focus and develop a sense of identity and future-oriented purpose.",
    "Mental health": "Prioritizing open dialogue about emotional well-being is critical during the final stages of brain maturation (pruning), specifically for the prefrontal cortex.",
    "Financial autonomy": "Transitioning to independent budget management reinforces adult decision-making patterns and personal accountability.",
    "Life skills": "Mastering household management and critical thinking fosters the self-efficacy required for a successful transition into independent adulthood.",
    
    "General": "This observation task is designed to target specific developmental windows. Recording these milestones ensures a balanced growth trajectory and early identification of care needs."
}

CHILD_DESCRIPTIONS = {
    # 0-2Y
    "Tummy time practice": "Critical for core strength, tummy time develops the neck, shoulder, and back muscles required for later motor milestones like sitting up, crawling, and eventually walking.",
    "Object tracking": "Focusing on moving objects strengthens the ocular muscles and neural pathways responsible for visual attention and depth perception.",
    "Babbling back": "Vocal experimentation is the precursor to speech; it exercises the vocal cords and teaches the rhythmic structure of conversation.",
    "Grasping soft toys": "Developing the palmar grasp is a key fine motor milestone that prepares the hand for complex tasks like holding a pencil or using tools.",
    
    # 3-5Y
    "Learning ABCs": "Phonemic awareness through alphabet recognition is the foundation of literacy, linking visual symbols to specific auditory sounds.",
    "Counting 1-20": "Learning numerical sequence introduces the concept of quantity and stable order, which are the building blocks of early mathematical reasoning.",
    "Identifying basic shapes": "Visual-spatial processing of geometric shapes helps the brain organize the physical environment and prepare for complex spatial logic.",
    "Sharing toys": "Practice in sharing develops the 'Theory of Mind,' the ability to understand that others have different thoughts and desires than oneself.",
    
    # 6-12Y
    "Daily reading goals": "Consistent reading increases vocabulary density and strengthens the brain's white matter, which is responsible for high-speed information processing.",
    "Mathematics practice": "Engagement with numerical patterns moves the brain from concrete counting to abstract operational thinking, building neural pathways for logical deduction.",
    "Science experiments": "The scientific method encourages critical inquiry and helps children understand cause-and-effect relationships through empirical observation.",
    "Logical puzzles": "Puzzles stimulate the prefrontal cortex, encouraging trial-and-error learning and enhancing spatial reasoning—both core components of mathematical success.",
    
    # 13-25Y
    "Advanced Algebra": "Algebraic training transitions the brain to handle variables and symbols. This develops the high-level analytical reasoning required for scientific and engineering disciplines.",
    "Analytical essays": "Complex writing tasks require the integration of multiple brain regions to synthesize information, argue a position, and structure logic.",
    "Public speaking": "Practicing rhetoric and presentation builds confidence and the neural efficiency required to process social feedback in real-time.",
    "Technical certification": "Mastering specific technical domains prepares the individual for the specialized cognitive demands of the modern professional workforce.",
    
    "General": "This activity focuses on achieving a specific learning objective. By mastering this task, you are reinforcing neural connections responsible for age-specific cognitive and physical skills."
}

ROADMAP_DATA = [
    {"age": "0-5Y", "title": "Early Development", "icon": "🍼", "color": "#FF6B6B", "pos": (200, 50)},
    {"age": "5-6Y", "title": "Social Integration", "icon": "🪁", "color": "#4ECDC4", "pos": (270, 155)},
    {"age": "6-12Y", "title": "Academic Roots", "icon": "📚", "color": "#45B7D1", "pos": (120, 280)},
    {"age": "12-15Y", "title": "Adolescent Growth", "icon": "🚀", "color": "#96CEB4", "pos": (250, 420)},
    {"age": "18-22Y", "title": "Higher Education", "icon": "🏛️", "color": "#FFEEAD", "pos": (100, 580)},
    {"age": "23-25Y", "title": "Career Launch", "icon": "💼", "color": "#D4A5A5", "pos": (280, 720)},
    {"age": "25Y+", "title": "Life Mastery", "icon": "👑", "color": "#9B59B6", "pos": (200, 880)},
]

PARENT_LEARNING = {
    "0-2Y": ["Monitor sleep cycles", "Introduction to solids", "Sensory play", "Language mirroring"],
    "3-5Y": ["Social coaching", "Emotional labels", "Creative art", "Hygiene"],
    "6-12Y": ["Study habits", "Digital safety", "Friendships", "Financial basics"],
    "13-25Y": ["Career paths", "Mental health", "Financial autonomy", "Life skills"]
}

CHILD_LEARNING = {
    "0-2Y": ["Tummy time practice", "Object tracking", "Babbling back", "Grasping soft toys"],
    "3-5Y": ["Learning ABCs", "Counting 1-20", "Identifying basic shapes", "Sharing toys"],
    "6-12Y": ["Daily reading goals", "Mathematics practice", "Science experiments", "Logical puzzles"],
    "13-25Y": ["Advanced Algebra", "Analytical essays", "Public speaking", "Technical certification"]
}

# ==================================================
# LOGIC & SESSION STATE
# ==================================================
if "total_xp" not in st.session_state: st.session_state.total_xp = 0
if "task_status" not in st.session_state: st.session_state.task_status = {}
if "user_name" not in st.session_state: st.session_state.user_name = "Voyager"
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = ""

def update_status(task_key, status):
    prev = st.session_state.task_status.get(task_key, "Not Done")
    if prev == "Not Done" and status == "Done":
        st.session_state.total_xp += 30
    elif prev == "Done" and status == "Not Done":
        st.session_state.total_xp = max(0, st.session_state.total_xp - 30)
    st.session_state.task_status[task_key] = status

# ==================================================
# SIDEBAR CONTENT
# ==================================================
with st.sidebar:
    # Sidebar Header with Avatar
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <img src="https://api.dicebear.com/9.x/adventurer/svg?seed={st.session_state.user_name}&backgroundColor=transparent" width="100" style="border-radius: 50%; border: 3px solid #d4af37; padding: 3px; margin-bottom: 10px;">
        <h2 style='color:#333; font-size:1.2rem; margin:0;'>{st.session_state.user_name}</h2>
        <p style='color:gray; font-size:0.8rem;'>Level {st.session_state.total_xp // 300} Explorer</p>
    </div>
    """, unsafe_allow_html=True)
    
    # label_visibility="collapsed" keeps the list looking like a professional menu
    page = st.radio(
        "Menu", 
        ["📊 Dashboard", "🗺️ Quest Roadmap", "🧠 Parent Hub", "🎯 Child Zone", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.metric("Total Progress XP", st.session_state.total_xp)

    st.write("")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.auth_page = "landing"
        st.rerun()

# ==================================================
# PAGE 1: DASHBOARD
# ==================================================
if page == "📊 Dashboard":
    # 1. Determine Time of Day for Greeting
    hour = datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    # 2. Find Next Recommended Task
    next_task_name = "All Tasks Completed! 🎉"
    next_task_loc = "Relax"
    
    # Search Parent Hub
    found = False
    for age_grp, tasks in PARENT_LEARNING.items():
        for t in tasks:
            if st.session_state.task_status.get(f"p_{age_grp}_{t}") != "Done":
                next_task_name = t
                next_task_loc = "🧠 Parent Hub"
                found = True
                break
        if found: break
    
    # Search Child Zone if not found
    if not found:
        for age_grp, tasks in CHILD_LEARNING.items():
            for t in tasks:
                if st.session_state.task_status.get(f"c_{age_grp}_{t}") != "Done":
                    next_task_name = t
                    next_task_loc = "🎯 Child Zone"
                    found = True
                    break
            if found: break

    # 3. Custom CSS
    st.markdown("""
    <style>
        .dash-card {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #e5e7eb;
            height: 100%;
            transition: transform 0.2s;
        }
        .dash-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        }
        .stat-value {
            font-size: 28px;
            font-weight: 700;
            color: #1f2937;
        }
        .stat-label {
            font-size: 13px;
            color: #6b7280;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .section-header {
            font-size: 20px;
            font-weight: 700;
            color: #111827;
            margin: 25px 0 15px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .mission-card {
            background: linear-gradient(135deg, #d4af37 0%, #f3e5ab 100%);
            color: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)

    # 4. Header Section
    st.markdown(f"### 🌤️ {greeting}, {st.session_state.user_name}")
    st.markdown("_\"The way we talk to our children becomes their inner voice.\" — Peggy O'Mara_")
    st.write("")

    # 5. KPI Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    current_xp = st.session_state.total_xp
    level = current_xp // 300
    completed_tasks = list(st.session_state.task_status.values()).count("Done")
    next_milestone = (level + 1) * 300
    
    with c1:
        st.markdown(f"""
        <div class="dash-card">
            <div class="stat-label">✨ Total XP</div>
            <div class="stat-value">{current_xp}</div>
            <div style="color: #10b981; font-size: 12px;">Lifetime Earned</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="dash-card">
            <div class="stat-label">🏆 Current Level</div>
            <div class="stat-value">Lvl {level}</div>
            <div style="color: #6b7280; font-size: 12px;">Next: {next_milestone} XP</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="dash-card">
            <div class="stat-label">✅ Completed</div>
            <div class="stat-value">{completed_tasks}</div>
            <div style="color: #3b82f6; font-size: 12px;">Missions Done</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        status_tier = "Elite" if current_xp > 900 else "Pro" if current_xp > 500 else "Member"
        st.markdown(f"""
        <div class="dash-card">
            <div class="stat-label">🌟 Status</div>
            <div class="stat-value">{status_tier}</div>
            <div style="color: #8b5cf6; font-size: 12px;">Top 5% Parent</div>
        </div>
        """, unsafe_allow_html=True)

    # 6. Main Content Split
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="section-header">📊 Growth Analytics</div>', unsafe_allow_html=True)
        
        # Simulated Trend Data (since we don't have history DB)
        # We create a curve that ends at current XP
        trend_data = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "XP Growth": [
                max(0, current_xp - 150), 
                max(0, current_xp - 120), 
                max(0, current_xp - 100), 
                max(0, current_xp - 60), 
                max(0, current_xp - 30), 
                max(0, current_xp - 10), 
                current_xp
            ]
        })
        st.area_chart(trend_data.set_index("Day"), color="#d4af37", height=250)

        st.markdown('<div class="section-header">🧠 Skill Distribution</div>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({
            "Category": ["Cognitive", "Social", "Physical", "Emotional", "Language", "Creativity"],
            "Score": [
                current_xp * 0.3 + 20, 
                current_xp * 0.25 + 30, 
                current_xp * 0.4 + 10, 
                current_xp * 0.2 + 40,
                current_xp * 0.35 + 15,
                current_xp * 0.15 + 25
            ]
        })
        st.bar_chart(chart_data.set_index("Category"), color="#8b5cf6", height=200)
    
    with col_right:
        st.markdown('<div class="section-header">🚀 Next Mission</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="mission-card">
            <div style="font-size: 14px; opacity: 0.9; margin-bottom: 5px;">RECOMMENDED FOR YOU</div>
            <div style="font-size: 22px; font-weight: bold; margin-bottom: 10px; color: #1f2937;">{next_task_name}</div>
            <div style="font-size: 14px; margin-bottom: 20px; color: #374151;">Found in: <b>{next_task_loc}</b></div>
            <div style="background: rgba(255,255,255,0.3); padding: 8px; border-radius: 8px; font-size: 12px; color: #1f2937;">
                💡 Completing this unlocks +30 XP
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown('<div class="section-header">🏅 Recent Activity</div>', unsafe_allow_html=True)
        
        if not st.session_state.task_status:
            st.info("Start your journey to see updates here!")
        else:
            recent = list(st.session_state.task_status.items())[-4:]
            for k, v in reversed(recent):
                task_name = k.split('_')[-1]
                st.markdown(f"""
                <div style="padding: 12px; background: white; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #10b981; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="font-size: 13px; font-weight: 600; color: #374151;">{task_name}</div>
                    <div style="font-size: 11px; color: #9ca3af;">Completed just now</div>
                </div>
                """, unsafe_allow_html=True)

# ==================================================
# PAGE 2: QUEST ROADMAP
# ==================================================
elif page == "🗺️ Quest Roadmap":
    st.markdown("## 🗺️ Your Life Journey Map")
    st.markdown("<div style='color:gray; margin-bottom:20px;'>Follow the golden path of development milestones.</div>", unsafe_allow_html=True)
    
    markers = ""
    for i, s in enumerate(ROADMAP_DATA):
        x, y = s["pos"]
        # Determine label position (left or right of the node)
        is_right = x > 200
        label_x = 50 if is_right else -170
        
        markers += f"""
        <g class="milestone-group" transform="translate({x}, {y})" style="cursor: pointer;">
            <!-- Connecting Line to Label -->
            <line x1="0" y1="0" x2="{label_x + (0 if is_right else 120)}" y2="0" stroke="{s['color']}" stroke-width="2" stroke-dasharray="4" opacity="0.8" />
            
            <!-- Main Circle Marker -->
            <circle r="30" fill="#111" stroke="{s['color']}" stroke-width="3" filter="url(#glow)">
                <animate attributeName="r" values="30;32;30" dur="4s" repeatCount="indefinite" begin="{i*0.5}s"/>
            </circle>
            <text x="0" y="10" text-anchor="middle" font-size="24">{s['icon']}</text>
            
            <!-- Label Box (Dark Theme) -->
            <g transform="translate({label_x}, -22)">
                <rect width="130" height="45" rx="8" fill="#1a1a1a" stroke="{s['color']}" stroke-width="1" stroke-opacity="0.5" />
                <rect width="4" height="45" rx="2" fill="{s['color']}" x="{0 if is_right else 126}" />
                <text x="{15 if is_right else 10}" y="18" font-family="Segoe UI, sans-serif" font-size="13" font-weight="bold" fill="#eee">{s['title']}</text>
                <text x="{15 if is_right else 10}" y="35" font-family="Segoe UI, sans-serif" font-size="11" fill="#aaa">{s['age']}</text>
            </g>
        </g>
        """
    
    roadmap_html = f"""
    <div style="background: #000000; padding: 40px; border-radius: 20px; border: 1px solid #333; box-shadow: 0 0 30px rgba(0,0,0,0.8);">
        <svg width="100%" height="950" viewBox="-50 0 500 950" style="overflow: visible;">
            <defs>
                <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <!-- Winding Path Background -->
            <path d="M 200 50 C 350 150, 50 250, 200 350 C 350 450, 50 550, 200 650 C 350 750, 50 850, 200 900" 
                  fill="none" stroke="#222" stroke-width="10" stroke-linecap="round" />
            
            <!-- Animated Golden Path -->
            <path d="M 200 50 C 350 150, 50 250, 200 350 C 350 450, 50 550, 200 650 C 350 750, 50 850, 200 900" 
                  fill="none" stroke="#d4af37" stroke-width="3" stroke-dasharray="10, 10" stroke-linecap="round" filter="url(#glow)">
                  <animate attributeName="stroke-dashoffset" from="100" to="0" dur="20s" repeatCount="indefinite" />
            </path>

            {markers}
        </svg>
    </div>
    """
    components.html(roadmap_html, height=1000)

# ==================================================
# PAGE 3 & 4: HUBS (Clean Interactive Descriptions)
# ==================================================
elif page in ["🧠 Parent Hub", "🎯 Child Zone"]:
    is_parent = page == "🧠 Parent Hub"
    hub_title = "Parent Growth Portal" if is_parent else "Child Training Zone"
    hub_icon = "🧠" if is_parent else "🎯"
    theme_color = "#d4af37" if is_parent else "#4ECDC4"
    
    data = PARENT_LEARNING if is_parent else CHILD_LEARNING
    desc_lookup = PARENT_DESCRIPTIONS if is_parent else CHILD_DESCRIPTIONS
    
    st.markdown(f"## {hub_icon} {hub_title}")
    st.markdown(f"<div style='color:gray; margin-bottom:20px;'>Select a developmental phase to view specific growth tasks and milestones.</div>", unsafe_allow_html=True)
    
    # Phase Selection
    selected_age = st.selectbox("Select Developmental Phase", list(data.keys()), index=0)
    
    # Calculate Progress
    tasks = data[selected_age]
    total_tasks = len(tasks)
    completed_tasks = 0
    for t in tasks:
        key = f"{'p' if is_parent else 'c'}_{selected_age}_{t}"
        if st.session_state.task_status.get(key) == "Done":
            completed_tasks += 1
            
    progress = completed_tasks / total_tasks if total_tasks > 0 else 0
    
    # Delightful Progress Card
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #ffffff 0%, #f8f9fa 100%); padding: 20px; border-radius: 15px; border: 1px solid #eee; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 10px;">
            <div>
                <span style="font-size: 16px; font-weight:bold; color:#333;">Phase Progress</span>
                <div style="font-size: 12px; color:gray;">{selected_age} Milestones</div>
            </div>
            <span style="font-size: 24px; font-weight:bold; color:{theme_color};">{int(progress*100)}%</span>
        </div>
        <div style="width:100%; background-color:#e9ecef; height:12px; border-radius:6px; overflow:hidden;">
            <div style="width:{progress*100}%; background-color:{theme_color}; height:100%; border-radius:6px; transition: width 1s ease-in-out;"></div>
        </div>
        <div style="margin-top:12px; display:flex; justify-content:space-between; font-size:12px; color:#666;">
            <span>🚀 {completed_tasks} completed</span>
            <span>🏁 {total_tasks} total</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Task List
    st.markdown("### 📋 Active Missions")
    
    for t in tasks:
        key = f"{'p' if is_parent else 'c'}_{selected_age}_{t}"
        status = st.session_state.task_status.get(key, "Not Done")
        is_done = status == "Done"
        
        # Dynamic Icon
        icon = "✅" if is_done else "⭕"
        
        # Expander for Task
        with st.expander(f"{icon} {t}", expanded=not is_done):
            c1, c2 = st.columns([3, 1])
            
            with c1:
                st.markdown(f"**Why this matters:**")
                description = desc_lookup.get(t, desc_lookup.get("General"))
                st.info(description)
                
            with c2:
                st.write("")
                st.write("")
                if not is_done:
                    if st.button("Complete Mission", key=f"btn_{key}", type="primary", use_container_width=True):
                        update_status(key, "Done")
                        st.balloons()
                        st.rerun()
                else:
                    st.success("Completed!")
                    if st.button("Undo", key=f"btn_{key}", use_container_width=True):
                        update_status(key, "Not Done")
                        st.rerun()

# ==================================================
# PAGE 5: SETTINGS (Updated with more features)
# ==================================================
elif page == "⚙️ Settings":
    st.markdown("## ⚙️ Settings & Preferences")
    st.markdown("<div style='color:gray; margin-bottom:30px;'>Manage your profile, app preferences, and data privacy.</div>", unsafe_allow_html=True)

    # Custom CSS for Settings
    st.markdown("""
    <style>
        .settings-card {
            background-color: white;
            border-radius: 12px;
            padding: 25px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .settings-header {
            font-size: 18px;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 15px;
            border-bottom: 1px solid #f0f0f0;
            padding-bottom: 10px;
        }
        .danger-zone {
            border: 1px solid #fecaca;
            background-color: #fff5f5;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 1. Profile Section
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown('<div class="settings-header">👤 User Profile</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 3])
    with c1:
        # Generate a consistent avatar based on username
        st.markdown(f"""<img src="https://api.dicebear.com/9.x/adventurer/svg?seed={st.session_state.user_name}&flip=true" width="120" style="border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">""", unsafe_allow_html=True)
    with c2:
        new_name = st.text_input("Display Name", value=st.session_state.user_name)
        st.text_input("Email Address", value=st.session_state.user_email, disabled=True, help="Managed via Firebase Auth")
        
        if st.button("Save Profile Changes", type="primary"):
            st.session_state.user_name = new_name
            st.success("Profile updated successfully!")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. App Preferences
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown('<div class="settings-header">🔔 Notifications & Appearance</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.toggle("Enable Email Notifications", value=True)
        st.toggle("Weekly Progress Report", value=True)
    with col_b:
        st.toggle("Sound Effects", value=False)
        st.toggle("High Contrast Mode", value=False)
    
    st.caption("Note: These preferences are saved locally for this session.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Data Management
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown('<div class="settings-header">💾 Data Management</div>', unsafe_allow_html=True)
    
    d1, d2 = st.columns([3, 1])
    with d1:
        st.markdown("**Export Your Journey**")
        st.markdown("Download a CSV file containing all your completed milestones and XP history.")
    with d2:
        progress_data = pd.DataFrame(list(st.session_state.task_status.items()), columns=['Task_ID', 'Status'])
        csv = progress_data.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv, file_name="evolution_progress.csv", mime="text/csv", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. Danger Zone
    st.markdown('<div class="settings-card danger-zone">', unsafe_allow_html=True)
    st.markdown('<div class="settings-header" style="color: #dc2626;">🚨 Danger Zone</div>', unsafe_allow_html=True)
    
    dz1, dz2 = st.columns([3, 1])
    with dz1:
        st.markdown("**Factory Reset**")
        st.markdown("This will permanently delete all your progress, XP, and unlocked achievements. This action cannot be undone.")
    with dz2:
        if st.button("Reset All Data", type="primary"):
            st.session_state.total_xp = 0
            st.session_state.task_status = {}
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
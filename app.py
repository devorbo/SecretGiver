import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# הגדרות דף
st.set_page_config(page_title="משחק הגמד והענק", page_icon="🎁", layout="centered")

# עיצוב מותאם אישית בסגנון הוורוד/יוקרתי הקודם
st.markdown("""
    <style>
    @import url('                                                       ;400;600&display=swap');
    
    /* הגדרות כלליות ורקע */
    .stApp {
        background-color: #fdf2f8 !important;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #fdf2f8 !important;
        direction: rtl;
        text-align: right;
    }

    /* עיצוב הכותרות */
    h1 {
        color: #831843 !important;
        font-weight: 300 !important;
        letter-spacing: -1px !important;
        text-align: center !important;
        padding-top: 2rem;
    }
    
    .subtitle {
        color: #be185d;
        text-align: center;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 3rem;
        opacity: 0.7;
        font-weight: 600;
    }

    /* עיצוב כרטיסי המשתתפים */
    [data-testid="stHorizontalBlock"] {
        background-color: rgba(255, 255, 255, 0.7) !important;
        padding: 1.5rem !important;
        border-radius: 20px !important;
        border: 1px solid rgba(251, 207, 232, 0.5) !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 1rem !important;
    }

    /* עיצוב שדות הקלט */
    .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid #fbcfe8 !important;
        padding: 12px !important;
        background-color: white !important;
        text-align: right !important;
    }
    
    .stTextInput label {
        color: #9d174d !important;
        font-weight: 600 !important;
        margin-bottom: 5px !important;
    }

    /* עיצוב כפתורים */
    .stButton button {
        background-color: #ec4899 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        height: 3rem !important;
    }
    
    .stButton button:hover {
        background-color: #db2777 !important;
        box-shadow: 0 10px 15px -3px rgba(244, 114, 182, 0.3) !important;
        transform: translateY(-2px) !important;
    }

    /* כפתור הוספת משתתף - עיצוב שונה */
    div[data-testid="stColumn"]:first-child .stButton button {
        background-color: transparent !important;
        color: #ec4899 !important;
        border: 2px dashed #fbcfe8 !important;
    }
    
    div[data-testid="stColumn"]:first-child .stButton button:hover {
        background-color: #fff1f2 !important;
        border-color: #ec4899 !important;
    }

    /* התאמות לנייד */
    @media (max-width: 640px) {
        [data-testid="stHorizontalBlock"] {
            padding: 1rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# פונקציה לשליחת מייל
def send_email(giver_name, giver_email, receiver_name):
    try:
        smtp_config = st.secrets["smtp"]
        msg = MIMEMultipart()
        msg['From'] = smtp_config["from_email"]
        msg['To'] = giver_email
        msg['Subject'] = "הגרלת הגמד והענק - מי הענק שלך?"
        
        html = f"""
        <div dir="rtl" style="font-family: sans-serif; line-height: 1.6; text-align: right;">
            <p>היי <strong>{giver_name}</strong>!</p>
            <p>הגרלת הגמד והענק הסתיימה ונקבע כי:</p>
            <p style="font-size: 1.2em; color: #831843; background-color: #fdf2f8; padding: 15px; border-radius: 10px; display: inline-block; border: 1px solid #fbcfe8;">
                אתה הגמד של: <strong>{receiver_name}</strong>
            </p>
            <p>זה הזמן להתחיל לחשוב על מתנה מפנקת...</p>
            <p>בהצלחה!</p>
        </div>
        """
        msg.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(smtp_config["host"], smtp_config["port"]) as server:
            server.starttls()
            server.login(smtp_config["user"], smtp_config["password"])
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"שגיאה בשליחת מייל ל-{giver_email}: {e}")
        return False

st.markdown('<h1>משחק הגמד והענק</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">ארגנו את החלפת המתנות שלכם בקלות ובנעימות</p>', unsafe_allow_html=True)

if 'participants' not in st.session_state:
    st.session_state.participants = [{"name": "", "email": ""}, {"name": "", "email": ""}, {"name": "", "email": ""}]

def add_participant():
    st.session_state.participants.append({"name": "", "email": ""})

# הצגת המשתתפים
for i, p in enumerate(st.session_state.participants):
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.participants[i]["name"] = st.text_input(f"שם {i+1}", value=p["name"], key=f"name_{i}")
    with col2:
        st.session_state.participants[i]["email"] = st.text_input(f"אימייל {i+1}", value=p["email"], key=f"email_{i}")

col_add, col_draw = st.columns(2)
with col_add:
    st.button("➕ הוספת משתתף", on_click=add_participant)
with col_draw:
    if st.button("🚀 בצע הגרלה ושלח מיילים"):
        active = [p for p in st.session_state.participants if p["name"].strip() and p["email"].strip()]
        if len(active) < 2:
            st.error("נא להזין לפחות 2 משתתפים.")
        else:
            receivers = active[:]
            random.shuffle(receivers)
            if any(active[i]["email"] == receivers[i]["email"] for i in range(len(active))):
                receivers = receivers[1:] + [receivers[0]]
                
            with st.spinner("שולח מיילים..."):
                success = 0
                for i in range(len(active)):
                    if send_email(active[i]["name"], active[i]["email"], receivers[i]["name"]):
                        success += 1
                if success == len(active):
                    st.success("ההגרלה הסתיימה! המיילים נשלחו בהצלחה.")
                    st.balloons()

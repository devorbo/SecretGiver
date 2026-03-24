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
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #fdf2f8;
        font-family: 'Inter', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .stButton button {
        background-color: #ec4899;
        color: white;
        border-radius: 15px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        background-color: #db2777;
        box-shadow: 0 10px 15px -3px rgba(244, 114, 182, 0.4);
        transform: translateY(-2px);
    }
    
    .stTextInput input {
        border-radius: 12px;
        border: 1px solid #fbcfe8;
        padding: 10px;
        background-color: rgba(255, 255, 255, 0.8);
    }
    
    .stTextInput label {
        color: #9d174d;
        font-weight: 500;
    }
    
    h1 {
        color: #831843;
        font-weight: 300;
        letter-spacing: -1px;
        text-align: center;
    }
    
    .subtitle {
        color: #be185d;
        text-align: center;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 2rem;
        opacity: 0.7;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        background-color: rgba(255, 255, 255, 0.6);
        padding: 1.5rem;
        border-radius: 24px;
        border: 1px solid rgba(251, 207, 232, 0.5);
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
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

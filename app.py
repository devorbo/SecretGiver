import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# הגדרות דף
st.set_page_config(page_title="משחק הגמד והענק", page_icon="🎁", layout="centered")

# הזרקת עיצוב מותאם אישית (CSS) למראה וורוד, נקי ומעוגל
st.markdown("""
    <style>
    /* רקע כללי בהיר מאוד */
    .stApp {
        background-color: #fffafd;
    }
    
    /* עיצוב כותרת עליונה */
    .main-title {
        color: #702a4d;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0px;
    }
    
    .sub-title {
        color: #d84d8d;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.2rem;
        margin-top: 0px;
        margin-bottom: 30px;
    }
    
    /* עיצוב כפתור השליחה הוורוד */
    div.stButton > button:first-child {
        background-color: #f43f8e;
        color: white;
        border-radius: 15px;
        border: none;
        padding: 15px 30px;
        font-size: 1.1rem;
        width: 100%;
        transition: 0.3s;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #d6337a;
    }
    
    /* עיצוב כפתור הוספת משתתף */
    button[kind="secondary"] {
        border-radius: 15px;
        border: 1px dashed #f43f8e;
        color: #f43f8e;
        background-color: transparent;
        width: 100%;
    }

    /* עיצוב תיבות הקלט */
    .stTextInput input {
        border-radius: 10px;
        border: 1px solid #fce4ec;
        background-color: white;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# פונקציה לשליחת מייל
def send_email(giver_name, giver_email, receiver_name):
    try:
        # משיכת הגדרות מתוך st.secrets [cite: 1, 2]
        smtp_config = st.secrets["smtp"]
        
        msg = MIMEMultipart()
        msg['From'] = smtp_config["from_email"]
        msg['To'] = giver_email
        msg['Subject'] = "הגרלת הגמד והענק - מי הענק שלך?"
        
        html = f"""
        <div dir="rtl" style="font-family: sans-serif; line-height: 1.6; text-align: right;">
            <p>היי <strong>{giver_name}</strong>!</p>
            <p>הגרלת הגמד והענק הסתיימה ונקבע כי:</p>
            <p style="font-size: 1.5em; color: #f43f8e;">אתה הגמד של: <strong>{receiver_name}</strong></p>
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

# ממשק המשתמש עם הטקסטים המקוריים
st.markdown('<h1 class="main-title">משחק הגמד והענק</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ארגנו את החלפת המתנות שלכם בקלות ובנעימות</p>', unsafe_allow_html=True)

# ניהול רשימת המשתתפים
if 'participants' not in st.session_state:
    st.session_state.participants = [{"name": "", "email": ""}, {"name": "", "email": ""}, {"name": [{"name": "", "email": ""}]}]

def add_participant():
    st.session_state.participants.append({"name": "", "email": ""})

# טופס הזנת נתונים
for i, p in enumerate(st.session_state.participants):
    col1, col2 = st.columns([1, 1])
    with col1:
        st.session_state.participants[i]["name"] = st.text_input("שם", value=p["name"], key=f"name_{i}", placeholder="שם")
    with col2:
        st.session_state.participants[i]["email"] = st.text_input("אימייל", value=p["email"], key=f"email_{i}", placeholder="אימייל")

st.button("הוספת משתתף +", on_click=add_participant)

if st.button("בצע הגרלה ושלח מיילים ✈️"):
    participants = [p for p in st.session_state.participants if p["name"] and p["email"]]
    
    if len(participants) < 2:
        st.warning("יש להזין לפחות 2 משתתפים.")
    else:
        givers = participants[:]
        receivers = participants[:]
        random.shuffle(receivers)
        
        # מניעת מצב שאדם מגריל את עצמו
        valid = True
        for i in range(len(givers)):
            if givers[i]["email"] == receivers[i]["email"]:
                valid = False
                break
        
        if not valid:
            receivers = receivers[1:] + [receivers[0]]
            
        with st.spinner("שולח הודעות סודיות..."):
            success_count = 0
            for i in range(len(givers)):
                if send_email(givers[i]["name"], givers[i]["email"], receivers[i]["name"]):
                    success_count += 1
            
            if success_count == len(givers):
                st.success(f"ההגרלה בוצעה! {success_count} מיילים נשלחו בהצלחה.")

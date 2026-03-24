import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# הגדרות דף
st.set_page_config(page_title="משחק הגמד והענק", page_icon="🎁", layout="centered")

# הזרקת עיצוב CSS למראה וורוד ומעוגל (כמו ב-AI Studio)
st.markdown("""
    <style>
    .stApp { background-color: #fffafd; }
    .main-title { color: #702a4d; text-align: center; font-family: 'Segoe UI', sans-serif; font-size: 3rem; font-weight: bold; margin-bottom: 0px; }
    .sub-title { color: #d84d8d; text-align: center; font-family: 'Segoe UI', sans-serif; font-size: 1.2rem; margin-top: 0px; margin-bottom: 30px; }
    
    /* עיצוב כפתור ביצוע הגרלה */
    div.stButton > button:first-child { 
        background-color: #f43f8e; color: white; border-radius: 20px; border: none; 
        padding: 15px 30px; font-size: 1.1rem; width: 100%; font-weight: bold;
    }
    
    /* עיצוב כפתור הוספת משתתף */
    button[kind="secondary"] { 
        border-radius: 20px; border: 1px dashed #f43f8e; color: #f43f8e; 
        background-color: white; width: 100%; 
    }

    /* עיצוב תיבות הקלט */
    .stTextInput input { border-radius: 15px !important; border: 1px solid #fce4ec !important; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# פונקציה לשליחת מייל דרך המפתחות שב-Secrets 
def send_email(giver_name, giver_email, receiver_name):
    try:
        smtp_config = st.secrets["smtp"] # שימוש בהגדרות המאובטחות 
        msg = MIMEMultipart()
        msg['From'] = smtp_config["from_email"]
        msg['To'] = giver_email
        msg['Subject'] = "הגרלת הגמד והענק - מי הענק שלך?"
        
        html = f"""
        <div dir="rtl" style="font-family: sans-serif; text-align: right; padding: 20px; border: 1px solid #fce4ec; border-radius: 15px;">
            <h2 style="color: #d84d8d;">היי {giver_name}!</h2>
            <p>ההגרלה בוצעה בהצלחה.</p>
            <p style="font-size: 1.3em;">האדם שאתה הגמד שלו הוא: <strong style="color: #f43f8e;">{receiver_name}</strong></p>
            <p>שיהיה בהצלחה ובהנאה!</p>
        </div>
        """
        msg.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(smtp_config["host"], smtp_config["port"]) as server:
            server.starttls()
            server.login(smtp_config["user"], smtp_config["password"])
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"שגיאה בשליחה ל-{giver_email}: {e}")
        return False

# כותרות האתר 
st.markdown('<h1 class="main-title">משחק הגמד והענק</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ארגנו את החלפת המתנות שלכם בקלות ובנעימות</p>', unsafe_allow_html=True)

# אתחול רשימת המשתתפים (תיקון ה-KeyError)
if 'participants' not in st.session_state:
    st.session_state.participants = [{"name": "", "email": ""}, {"name": "", "email": ""}, {"name": "", "email": ""}]

def add_participant():
    st.session_state.participants.append({"name": "", "email": ""})

# תצוגת הזנת נתונים
for i in range(len(st.session_state.participants)):
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.participants[i]["name"] = st.text_input("שם", value=st.session_state.participants[i]["name"], key=f"name_{i}", placeholder="הכנס שם...")
    with col2:
        st.session_state.participants[i]["email"] = st.text_input("אימייל", value=st.session_state.participants[i]["email"], key=f"email_{i}", placeholder="הכנס אימייל...")

st.button("הוספת משתתף +", on_click=add_participant)

if st.button("בצע הגרלה ושלח מיילים ✈️"):
    # סינון רק משתתפים עם נתונים מלאים
    valid_p = [p for p in st.session_state.participants if p["name"].strip() and p["email"].strip()]
    
    if len(valid_p) < 2:
        st.warning("יש להזין לפחות שני משתתפים כדי להתחיל.")
    else:
        givers = valid_p[:]
        receivers = valid_p[:]
        
        # הגרלה שמוודאת שאף אחד לא מקבל את עצמו
        max_attempts = 100
        for _ in range(max_attempts):
            random.shuffle(receivers)
            if all(givers[i]["email"] != receivers[i]["email"] for i in range(len(givers))):
                break
        
        with st.spinner("שולח הודעות סודיות..."):
            count = 0
            for i in range(len(givers)):
                if send_email(givers[i]["name"], givers[i]["email"], receivers[i]["name"]):
                    count += 1
            
            if count == len(givers):
                st.success(f"הסתיים בהצלחה! {count} מיילים נשלחו.")

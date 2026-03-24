import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# הגדרות דף
st.set_page_config(page_title="משחק הגמד והענק", page_icon="🎁", layout="centered")

# פונקציה לשליחת מייל
def send_email(giver_name, giver_email, receiver_name):
    try:
        # משיכת הגדרות מתוך st.secrets
        smtp_config = st.secrets["smtp"]
        
        msg = MIMEMultipart()
        msg['From'] = smtp_config["from_email"]
        msg['To'] = giver_email
        msg['Subject'] = "הגרלת הגמד והענק - מי הענק שלך?"
        
        html = f"""
        <div dir="rtl" style="font-family: sans-serif; line-height: 1.6;">
            <p>היי <strong>{giver_name}</strong>!</p>
            <p>הגרלת הגמד והענק הסתיימה ונקבע כי:</p>
            <p style="font-size: 1.2em; color: #2c3e50;">אתה הגמד של: <strong>{receiver_name}</strong></p>
            <p>זה הזמן להתחיל לחשוב על מתנה מפנקת...</p>
            <p>בהצלחה!</p>
        </div>
        """
        msg.attach(MIMEText(html, 'html'))
        
        # התחברות לשרת ושליחה
        with smtplib.SMTP(smtp_config["host"], smtp_config["port"]) as server:
            server.starttls()
            server.login(smtp_config["user"], smtp_config["password"])
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"שגיאה בשליחת מייל ל-{giver_email}: {e}")
        return False

# ממשק המשתמש
st.title("🎁 משחק הגמד והענק")
st.write("הזינו את שמות המשתתפים והמיילים שלהם, ואנחנו נבצע את ההגרלה ונשלח לכולם מייל סודי!")

# ניהול רשימת המשתתפים ב-Session State
if 'participants' not in st.session_state:
    st.session_state.participants = [{"name": "", "email": ""}, {"name": "", "email": ""}, {"name": "", "email": ""}]

def add_participant():
    st.session_state.participants.append({"name": "", "email": ""})

# טופס הזנת נתונים
for i, p in enumerate(st.session_state.participants):
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.participants[i]["name"] = st.text_input(f"שם משתתף {i+1}", value=p["name"], key=f"name_{i}")
    with col2:
        st.session_state.participants[i]["email"] = st.text_input(f"אימייל משתתף {i+1}", value=p["email"], key=f"email_{i}")

st.button("➕ הוסף משתתף", on_click=add_participant)

if st.button("🚀 בצע הגרלה ושלח מיילים"):
    participants = [p for p in st.session_state.participants if p["name"] and p["email"]]
    
    if len(participants) < 2:
        st.warning("יש להזין לפחות 2 משתתפים עם שם ואימייל.")
    else:
        # לוגיקת ההגרלה
        givers = participants[:]
        receivers = participants[:]
        random.shuffle(receivers)
        
        # וידוא שאף אחד לא קיבל את עצמו (הזזה ב-1 אם יש התאמה)
        valid = True
        for i in range(len(givers)):
            if givers[i]["email"] == receivers[i]["email"]:
                valid = False
                break
        
        if not valid:
            receivers = receivers[1:] + [receivers[0]]
            
        # שליחת המיילים
        with st.spinner("שולח מיילים..."):
            success_count = 0
            for i in range(len(givers)):
                if send_email(givers[i]["name"], givers[i]["email"], receivers[i]["name"]):
                    success_count += 1
            
            if success_count == len(givers):
                st.success(f"ההגרלה הסתיימה! {success_count} מיילים נשלחו בהצלחה.")
            else:
                st.warning(f"נשלחו {success_count} מתוך {len(givers)} מיילים. בדקו את השגיאות למעלה.")

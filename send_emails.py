import smtplib
from email.mime.text import MIMEText
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. Firebase Setup ---
if not firebase_admin._apps:  # _apps is a dict of initialized apps
    cred = credentials.Certificate("path/to/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# --- 2. Email Setup ---
SENDER = "anvit.aggarwal@gmail.com"
PASSWORD = "tuaj dmyu ewhw ozxb"  # create an App Password in Google account settings

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = to

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, to, msg.as_string())

# --- 3. Process Pending Emails ---
def process_emails():
    emails_ref = db.collection("emails").where("status", "==", "pending")
    docs = emails_ref.stream()

    for doc in docs:
        data = doc.to_dict()
        try:
            send_email(data["to"], data["subject"], data["body"])
            doc.reference.update({"status": "sent"})
            print(f"✅ Sent email to {data['to']}")
        except Exception as e:
            doc.reference.update({"status": "failed"})
            print(f"❌ Failed to send {data['to']}: {e}")

if __name__ == "__main__":
    process_emails()

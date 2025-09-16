import shutil
import smtplib
from email.message import EmailMessage
import os
 
# === CONFIGURATION ===
MEDIA_ROOT = "/opt/fetchmatica/media"
ALERT_THRESHOLD_PERCENT = 95  # ✅ TESTING: trigger alert if usage >= 95%
 
# === EMAIL CONFIGURATION (Amazon SES) ===
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'AKIAZWYU4SSW225W72IS'
EMAIL_HOST_PASSWORD = 'BD/ClYXfkWYs+B+CsaTtI8Vsbmu4ykbCD66AWLzE1C30'
EMAIL_FROM = 'info@fetchmatica.facileserv.com'
EMAIL_TO= 'huzefa.poonawala@facileserv.com,jyothish.kumar@facileserv.com,devops.support@facileserv.com,irfan.shaikh@facileserv.com,rohit.kadam@facileserv.com,parmeshwar.karbhari@facileserv.com,sourav.banerjee@facileserv.com,ashwini.wakhare@facileserv.com,akash.nerkar@facileserv.com,omkar.kure@facileserv.com'
 
def get_disk_usage_percent(path):
    total, used, free = shutil.disk_usage(path)
    return (used / total) * 100
 
def send_email_alert(usage_percent):
    msg = EmailMessage()
    msg["Subject"] = "🚨 Alert: Fetchmatica Storage Below 10GB Immediate Attention Required"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content(
        f"The disk usage on {MEDIA_ROOT} is {usage_percent:.2f}%.\n"
        f"Please take action before the server runs out of space."
    )
 
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
            if EMAIL_USE_TLS:
                smtp.starttls()
            smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            smtp.send_message(msg)
            print("✅ alert email sent.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
 
# === MAIN LOGIC ===
if __name__ == "__main__":
    usage_percent = get_disk_usage_percent(MEDIA_ROOT)
    print(f"Current disk usage on {MEDIA_ROOT}: {usage_percent:.2f}%")
 
    if usage_percent >= ALERT_THRESHOLD_PERCENT:
        send_email_alert(usage_percent)
    else:
        print("✅ Disk usage is below the 95% test threshold. No email sent.")
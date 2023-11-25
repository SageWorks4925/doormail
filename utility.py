import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(recipient_email, subject, body):
    sender_email = "worksofsage@gmail.com"
    sender_password = "jpvj qlan kxov rvzn" #"Worksofsage@123"

    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your SMTP server
    server.starttls()
    server.login(sender_email, sender_password)

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    server.send_message(msg)
    server.quit()

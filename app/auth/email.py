import smtplib
from email.message import EmailMessage
from flask import current_app, url_for

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    msg = EmailMessage()
    msg['Subject'] = 'Pen12 - Şifre Sıfırlama Talebi'
    msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
    msg['To'] = user.email
    
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    body = f'''Şifrenizi sıfırlamak için aşağıdaki bağlantıya tıklayın:

{reset_url}

Eğer bu talebi siz yapmadıysanız, bu e-postayı görmezden gelebilirsiniz.
'''
    msg.set_content(body)
    
    try:
        server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
        if current_app.config['MAIL_USE_TLS']:
            server.starttls()
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"E-posta gönderme hatası: {e}")

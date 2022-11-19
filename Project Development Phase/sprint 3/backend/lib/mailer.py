from flask import current_app, url_for
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_mail(subject, to_emails, plain_text_content=None, html_content=None, from_email=current_app.config['EMAIL_CONFIRMATION_SENDER_EMAIL']):
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        plain_text_content=plain_text_content,
        html_content=html_content)
    SendGridAPIClient(current_app.config['SENDGRID_API_KEY']).send(message)


def send_confirmation_email(user):
    try:
        to_emails = [user.email]
        confirmation_token = user.get_confirmation_token()
        confirmation_link = url_for(
            'auth.confirm_email', token=confirmation_token, _external=True)
        subject = 'Inventory: Confirm Your Mail Now!'
        plain_text_content = 'Please confirm your account by clicking the confirmation link below.'
        html_content = f'''
                        <a href='{confirmation_link}' target='_blank'>Click Here to Confirm Your Account!</a>
                    '''
        send_mail(subject=subject, to_emails=to_emails,
                  plain_text_content=plain_text_content, html_content=html_content)
    except Exception as e:
        current_app.log_exception(e)

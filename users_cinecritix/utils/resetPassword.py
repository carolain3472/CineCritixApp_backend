from sendgrid.helpers.mail import Mail
from decouple import config
from sendgrid import SendGridAPIClient
import os
from datetime import datetime

def sendResetPasswordEmail(reset_password_token):
    # Obtén el token como cadena
    forgot_password_token = str(reset_password_token.key)

    # Obtén el usuario desde el token
    user = reset_password_token.user

    # Define el saludo
    greetings = f"Hola {user.nombre} {user.apellido}," if user.nombre and user.apellido else "Hola"

    # Construye el contenido del correo electrónico
    email_html_content = f"<html><body><p>{greetings}</p>Por favor, usa este token para CineCritix App:<b> {forgot_password_token}</b></body></html>"

    message = Mail(
        from_email='pruebadesarrollo335@gmail.com',
        to_emails=[user.email],
        subject=f"Recuperar contraseña de CineCritix App. {str(datetime.now())}",
        html_content=email_html_content
    )

    sendgrid_client = SendGridAPIClient(api_key='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')

    response = sendgrid_client.send(message)

    if response.status_code== 202:
        print('Contraseña de recuperación enviada exitosamente a' +
              str(reset_password_token.user.email))
    else:
        print("Error al enviar el email")

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    msg = MIMEMultipart()
    message = f"""
    
    Hola {reset_password_token.user.username},
    
    Hemos recibido una solicitud para resetear su contraseña. Por favor haz click en el link de abajo para resetear tu contraseña:
    http://www.jvarasm.com/reset_password/?token={reset_password_token.key}
    
    Si no has solicitado reseto de contraseña, puedes ignorar de manera segura este email.
    
    Atentamente,
    Jonathan Varas
    
    """
    # setup the parameters of the message 
    password = "True1234trust1234!"
    msg['From'] = "jvarasdev@jvarasm.com"
    msg['To'] = reset_password_token.user.email
    msg['Subject'] = "Reseteo de contraseña"
    # add in the message body 
    msg.attach(MIMEText(message, 'plain'))
    #create server 
    #server = smtplib.SMTP('smtp.gmail.com' , port=465) #hotmail: "smtp-mail.outlook.com", 
    server = smtplib.SMTP_SSL('mail.jvarasm.com', port=465)
    #server.starttls()
    # Login Credentials for sending the mail 
    server.login(msg['From'], password)
    # send the message via the server. 
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()
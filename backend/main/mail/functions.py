from .. import mailsender
from flask import current_app, render_template
from flask_mail import Message
from smtplib import SMTPException

#Enviar mail.
def sendMail(to, subject, template, **kwargs):
    '''Envio de mails.
            
            -args:
                -to: Hacia donde se envia el mail.
                -subject: Titulo del mensaje.
                -template: Contenido a enviar en el mail.
                -**kwargs: Acepta mas argumentos
    '''
    #Configuracion del mail
    msg = Message( subject, sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=to)
    try:
        #Creación del cuerpo del mensaje
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        #Envío de mail
        result = mailsender.send(msg)
    except SMTPException as e:
        print(str(e))
        return "Mail deliver failed"
    return True

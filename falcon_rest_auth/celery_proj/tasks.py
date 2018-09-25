from __future__ import absolute_import, unicode_literals

from .celery import app

import requests
import json

@app.task
def send_gmail(provider,template, recipient, body_replace_params = None):
    import smtplib
    credentials = json.loads( provider.get("credentials") )
    
    BODY = template.get("body")
    if body_replace_params:
      new_body = BODY.format(**body_replace_params)
      BODY = new_body




    FROM = provider.get("default_from_address")
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = template.get("subject")
    TEXT = BODY

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    print (message,FROM,TO,SUBJECT,BODY)

    try:
        server = smtplib.SMTP(credentials.get("host"), credentials.get("port"))
        server.ehlo()
        server.starttls()
        server.login(credentials.get("user"), credentials.get("password"))
        server.sendmail(FROM, TO, message)
        server.close()
        print ('successfully sent the mail')
    except Exception as ex:
      print ("failed to send mail")
      print (str(ex))
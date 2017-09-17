

def send_email(user, pwd, recipient, subject, body, attachment):
   
    # based on :
    # https://www.linkedin.com/pulse/python-script-send-email-attachment-using-your-gmail-account-singh

    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from smtplib import SMTP
    import smtplib
    import sys


    try:

        recipients = [recipient]
        emaillist = [elem.strip().split(',') for elem in recipients]
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = user
        msg['Reply-to'] = user
 
        msg.preamble = 'Multipart massage.\n'
 
        part = MIMEText( body )
        msg.attach(part)
 
        part = MIMEApplication( open( excel_file_path  ,"rb").read() )
        part.add_header('Content-Disposition', 'attachment', filename= excel_file_path   )
        msg.attach(part)
 

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login( user , pwd)

        server.sendmail(msg['From'], emaillist , msg.as_string())

    except Exception as e:
        print "Cannot send email and attachment. Error is: "
        print e 

if __name__ == '__main__':

    import os
    user = "johnsteedman360dev@gmail.com"
    recipient = "johnsteedman360@gmail.com"
    pwd   = 'DEVED!23'
    subject = 'an email'
    body    = 'hello...'
    excel_file_path =os.path.join (os.getcwd(),'EONET_Events.xlsx' )
    send_email(user, pwd, recipient, subject, body, excel_file_path)




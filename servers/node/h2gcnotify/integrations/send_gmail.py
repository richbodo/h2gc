#!/usr/bin/python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

def mail_pwd(pwd_file):
   try: 
      pf_handle = open(pwd_file,'r')
   except:
      print "can't open send_gmail config file"
   try:
      pstring=readline(pf_handle)
   except:
      print "can't read from send_gmail config file"
   close(pf_handle)
   return pstring


def mail(to, subject, text, attach):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()


gmail_user = "ahewes@kungfuvrobots.com"
home_dir = os.path.expanduser("~") + "/.h2gc/"
pwd_file = home_dir + "integrations/sendgmail"
gmail_pwd = mail_pwd()
if (gmail_pwd == ""):
   print "You have to initialize the send_gmail integration by dropping a password in: " + pwd_file 
   exit(1)
mail("support@kungfuvrobots.com",
   "One more test",
   "Only used for this demo",
   "/home/richbodo/.h2gc/support_summary")

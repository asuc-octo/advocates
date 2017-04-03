import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
PASSWORD = "saorocks!"
ADDRESS = "noreplysaoberkeley@gmail.com"
#change to 'no-reply@sao' or something
def send_mail(toaddr, subject, body): 
	fromaddr = ADDRESS
	msg = MIMEMultipart()
	msg['From'] = ADDRESS
	msg['To'] = toaddr
	msg['Subject'] = subject
	 
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, PASSWORD)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

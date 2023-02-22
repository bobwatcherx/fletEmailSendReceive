from flet import *
import imaplib
import email
import smtplib

from email.header import Header,decode_header,make_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders


# SET CONNECTION
HOST = "imap.gmail.com"
USERNAME = "bobwatcherx@gmail.com"
PASSWORD = "bvegeyruhcgzmyqe"


def main(page:Page):
	page.scroll = "auto"
	listemail = Column(scroll="auto")
	datemail = TextField(label="filter date",
		hint_text="Example 22-Feb-2023",
		value="22-Feb-2023"
		)

	# NOW CREATE FILTER FOR DATE 
	# YOU CAN FILTER INBOX MESSAGE BY DATE 

	def filternow(e):
		# CLEAR DATA LAST AND PUSH DATA NEW
		listemail.controls.clear()
		page.update()
		# AND CALL FUNCTION AGAIN FOR PUSH DATA TO WIDGET AGAIN
		checkemail()

	filteremail = Row([
		datemail,
		IconButton(icon="search",
			on_click=filternow
			)

		],alignment="end")



	# CHECK YOU INBOX EMAIL THEN GET ALL DATA AND PUSH TO WIDGET
	def checkemail():
		m = imaplib.IMAP4_SSL(HOST,993)
		m.login(USERNAME,PASSWORD)
		m.select("INBOX")
		result,data  = m.uid("search",None,'SINCE',datemail.value)
		if result == "OK":
			for num in data[0].split():
				result,data = m.uid("fetch",num,'(RFC822)')
				if result == "OK":
					email_message_raw = email.message_from_bytes(data[0][1])
					email_from = str(make_header(decode_header(email_message_raw['From'])))
					email_subject = str(make_header(decode_header(email_message_raw['Subject'])))
					email_date = str(make_header(decode_header(email_message_raw['Date'])))

					# AND SHOW PRINT YOU CAN SEE FROM TERMINAL
					print("from :",email_from)
					print("subject :",email_subject)
					print("date :",email_date)

					# AND PRINT MESSAGE BODY 
					email_message = email.message_from_bytes(data[0][1])
					for part in email_message.walk():
						if part.get_content_type() == "text/plain":
							body = part.get_payload(decode=True)
							print("YOu message body : ",body.decode("utf-8"))

					print("")

					# AND PUSH DATA LIKE SUBJECT FROM MAIL ,TO LISTEMAIL
					listemail.controls.append(
						ListTile(
							leading=Icon(name="mail"),
							title=Text(f"sub : {email_from}"),
							subtitle=Row([
								Text(email_from),
								Text(email_date)

								],alignment="spaceBetween")

							)

						)
					page.update()


		# CLOSE CONNECTION
		m.close()
		m.logout()
	checkemail()



	# NOW CREATE SEND EMAIL TO CLIENT
	mysubject = TextField(label="subject")
	myfromemail = TextField(label="from email")
	mytoemail = TextField(label="to email")
	mybodyemail = TextField(label="you message here")


	def sendingemail(e):
		smtp_server = "smtp.gmail.com"
		smtp_port = 587

		server = smtplib.SMTP(smtp_server,smtp_port)
		server.ehlo()
		server.starttls()
		server.login(USERNAME,PASSWORD)


		# AND CREATE EMAIL
		msg = MIMEMultipart()
		msg['Subject'] = "{}".format(mysubject.value)
		msg['From'] = myfromemail.value
		msg['To'] = mytoemail.value

		# YOU CAN SEND FILE ATTACHMENT TO CLIENT
		# EXAMPLE I WILL SEND FILE TXT 
		# I CREATE FILE 

		filename = "example.txt"
		attachment = open(filename,"rb")
		part = MIMEBase("application","octet-stream")
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header("Content-Disposition","attachment;filename=%s" % filename)
		msg.attach(part)

		# AND SET YOU VALUE BODY MESSAGE HERE
		body = mybodyemail.value
		msg.attach(MIMEText(body,"plain"))

		# AND LAST SEND MAIL TO CLIENT
		server.sendmail(myfromemail.value,mytoemail.value,msg.as_string())
		server.quit()



	containermessage =  Container(
		bgcolor="blue200",
		padding=10,
		margin=margin.only(left=30,right=30),
		content=Column([
			Text("Send email ",size=20),
			mysubject,
			myfromemail,
			mytoemail,
			mybodyemail,
			Row([
				FloatingActionButton(
				icon="add",
				shape=CircleBorder(),
				bgcolor="blue",
				on_click=sendingemail

					)

				],alignment="end")

			])
		)



	page.add(
		AppBar(
		title=Text("GMAIL Remake",size=25,weight="bold",
			color="white"
			),
		bgcolor="blue"
			),
		containermessage,
		Column([
			Text("Inbox You email",size=25,weight="bold"),
			filteremail,
			listemail

		])


		)

flet.app(target=main)



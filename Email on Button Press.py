import smtplib
import RPi.GPIO as GPIO
import time
  
#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'youremail@email.com' #change this to match your gmail account
GMAIL_PASSWORD = 'yourPassword'  #change this to match your gmail password
 
#Set GPIO pins to use BCM pin numbers
GPIO.setmode(GPIO.BCM)
 
#Set digital pin 17(BCM) to an input
GPIO.setup(17, GPIO.IN)
 
#Set digital pin 17(BCM) to an input and enable the pullup 
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
#Event to detect button press
GPIO.add_event_detect(17, GPIO.FALLING)
 
  
class Emailer:
    def sendmail(self, recipient, subject, content):
          
        #Create Headers
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                   "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)
  
        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
  
        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
  
        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.quit
  
sender = Emailer()
 
while True:
    if GPIO.event_detected(17):
        sendTo = 'anotheremail@email.com'
        emailSubject = "Button Press Detected!"
        emailContent = "The button has been pressed at: " + time.ctime()
        sender.sendmail(sendTo, emailSubject, emailContent)
        print("Email Sent")
 
    time.sleep(0.1)
    
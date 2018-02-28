#-*- coding: utf-8 -*-
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import Separator
from tkinter.scrolledtext import *
import smtplib
import tkinter as tk
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ftplib import FTP_TLS, FTP
import sys

sys.tracebacklimit = 0

def clear_search(event):
  if(input_smtp_username.get() == "Only if authentication enabled"):
    input_smtp_username.delete(0, tk.END)
    input_smtp_password.delete(0, tk.END)
  input_smtp_username.config(fg='black')
  input_smtp_password.config(fg='black', show='*')

def displayOptionsFTP(server, port, user, password):
  textPad.configure(state='normal')
  textPad.insert('end', "---Parameters-----------------\nServer: " + server + "\n" +
    "port: " + port + "\n" +
    "user: " + user + "\n" +
    "password: " + password + "\n")
  textPad.see("end")
  textPad.insert('end',"\n---Starting FTP checking------------\n")
  textPad.see("end")
  
  
def displayOptionsSMTP(server, port, user, password, from_email, to_email, subject, body):
  textPad.configure(state='normal')
  textPad.insert('end', "---Parameters-----------------\nServer: " + server + "\n" +
    "port: " + port + "\n" +
    "user: " + user + "\n" +
    "password: " + password + "\n" +
    "from: " + from_email + "\n" + 
    "to: " + to_email + "\n" + 
    "subject: " + subject + "\n" + 
    "body: " + body + "\n")
  textPad.see("end")
  textPad.insert('end',"\n---Starting SMTP checking------------\n")
  textPad.see("end")
  
def sendMail(server, port, user, password, from_email, to_email, subject, body):
  displayOptionsSMTP(server, port, user, password, from_email, to_email, subject, body)
  msg = MIMEMultipart()
  msg['From'] = from_email
  msg['To'] = to_email
  msg['Subject'] = subject
  message = body
  msg.attach(MIMEText(message))
  try:
        
        textPad.insert('end',"An SMTP instance encapsulates an SMTP connection to " + server + ":" + port + "\n")
        mailserver = smtplib.SMTP(server, port,None, 8)
        textPad.insert('end', "\t -> success\n")
        if (mailserver):
          textPad.insert('end',"Initiating the SMTP conversation using EHLO" + "\n")
          mailserver.ehlo()
          textPad.insert('end', "\t -> success\n")
          textPad.see("end")
          
          if (is_tls_checked.get() == 1):
            textPad.insert('end',"Initializing TLS!" + "\n")
            mailserver.starttls()
            textPad.insert('end', "\t -> success\n")
            textPad.see("end")
          textPad.insert('end',"Initiating the SMTP conversation using EHLO" + "\n")
          mailserver.ehlo()
          textPad.insert('end', "\t -> success\n")
          textPad.see("end")
          
          if (is_auth_checked.get() == 1):
            textPad.insert('end', "Logging in with " + user + ":" + password + "\n")
            mailserver.login(user, password)
            textPad.insert('end',"\tSuccessfully logged in using " + user + ":" + password + "\n")
            textPad.see("end")
          textPad.insert('end', "Trying to send referenced email\n")
          mailserver.sendmail(msg['From'], msg['To'], msg.as_string())
          textPad.insert('end',"\tMessage sent successfully!" + "\n" + "\n")
          textPad.see("end")
          mailserver.quit()
  except Exception as e:
    textPad.insert('end',"Exception raised: {}".format(e))
    textPad.see("end")
  textPad.config(state=DISABLED)
  textPad.see("end")

def sendFtp(server, port, user, password):
  displayOptionsFTP(server, port, user, password)
  textPad.configure(state='normal')
  if (is_tls_ftp_checked.get() == 1):
    try:
          textPad.insert('end', "Initializing FTP_TLS\n")
          ftps = FTP_TLS()
          textPad.insert('end', "\t -> success\n")
          textPad.insert('end', "Connecting to " + server + ":"+ port + "\n")
          ftps.connect(server, int(port))
          textPad.insert('end', "\t -> success\n")
          if (is_auth_ftp_checked.get() == 1):
            textPad.insert('end', "Trying to connect with anonymous login\n")
            ftps.login()
            textPad.insert('end', "\t -> success\n")
            textPad.see("end")
          else:
            textPad.insert('end', "Logging in with " + user + ":" + password + "\n")
            textPad.see("end")
            ftps.login(user=user, passwd=password)
            textPad.insert('end', "\t -> success\n")
            textPad.see("end")
          ftps.prot_p()
          textPad.see("end")
          listing = []
          textPad.insert('end', "--Listing directories:\n")
          ftps.retrlines("LIST",listing.append)
          textPad.insert('end', "\n".join(listing))
          textPad.insert('end', "\n\t -> success\n")
          textPad.see("end")
          ftps.close()
    except Exception as e:
          textPad.configure(state='normal')
          textPad.insert('end', "Exception raised: {}\n".format(e))
    textPad.config(state=DISABLED)
  else:
    try:
          textPad.insert('end',"---Starting FTP checking------------\n")
          textPad.insert('end', "Initializing FTP\n")
          ftp = FTP()
          textPad.insert('end', "\t -> success\n")
          textPad.insert('end', "Connecting to " + server + ":"+ port + "\n")
          ftp.connect(server, int(port))
          textPad.insert('end', "\t -> success\n")
          if (is_auth_ftp_checked.get() == 1):
            textPad.insert('end', "Trying to connect with anonymous login\n")
            ftp.login()
            textPad.insert('end', "\t -> success\n")
            textPad.see("end")
          else:
            textPad.insert('end', "Logging in with " + user + ":" + password + "\n")
            textPad.see("end")
            ftp.login(user=user, passwd=password)
            textPad.insert('end', "\t -> success\n")
            textPad.see("end")
          ftp.prot_p()
          textPad.see("end")
          listing = []
          textPad.insert('end', "--Listing directories:\n")
          ftp.retrlines("LIST",listing.append)
          textPad.insert('end', "\n".join(listing))
          textPad.insert('end', "\n\t -> success\n")
          textPad.see("end")
          ftp.close()
    except Exception as e:
          textPad.configure(state='normal')
          textPad.insert('end', "Exception raised: {}\n".format(e))
    textPad.config(state=DISABLED)

def about():
  messagebox.showinfo("About","A little program to check whether an SMTP or FTP server works or does not work!\nContact: contact@husonny.fr")

def exitProg():
  mainWin.destroy()
  sys.exit(0)
  

#Main Win
mainWin = Tk()
mainWin.title('Smtp -/- Ftp Checker')
mainWin.resizable(False, False)

menubar = Menu(mainWin)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=about)
helpmenu.add_command(label="Exit", command=exitProg)
menubar.add_cascade(label="Help", menu=helpmenu)

mainWin.config(menu=menubar)
#Frame
mainFrame = Frame(mainWin, borderwidth=2, relief=GROOVE)
mainFrame.grid(row=0, column=0,padx=20, pady=5)

#Smtp section
##section
label_frame_smtp = LabelFrame(mainFrame, text="Check smtp", padx=20, pady=15)
label_frame_smtp.grid(row=0, column=0, sticky=N)

#server
Label(label_frame_smtp, text="Server:").grid(row=0, sticky=W)
smtp_server= StringVar()
input_smtp_server = Entry(label_frame_smtp, textvariable= smtp_server, show='', bg ='white', fg='black', width=30)
input_smtp_server.grid(row=0, column=1)

#port
Label(label_frame_smtp, text="Port:").grid(row=1, sticky=W)
smtp_port= StringVar()
input_smtp_port = Entry(label_frame_smtp, textvariable= smtp_port, show='', bg ='white', fg='black', width=30)
input_smtp_port.insert(0,'25')
input_smtp_port.grid(row=1, column=1)

#Username
Label(label_frame_smtp, text="Username:").grid(row=2, sticky=W)
smtp_username= StringVar()
input_smtp_username = Entry(label_frame_smtp, textvariable= smtp_username, show='', bg ='white', fg='grey', width=30)
input_smtp_username.insert(0, 'Only if authentication enabled')
input_smtp_username.bind("<FocusIn>", clear_search)
input_smtp_username.grid(row=2, column=1)


#Password
Label(label_frame_smtp, text="Password:").grid(row=3, sticky=W)
smtp_password= StringVar()
input_smtp_password = Entry(label_frame_smtp, textvariable= smtp_password, show='', bg ='white', fg='grey', width=30)
input_smtp_password.insert(0, 'Only if authentication enabled')
input_smtp_username.bind("<FocusIn>", clear_search)
input_smtp_password.grid(row=3, column=1)

is_auth_checked = IntVar()
enable_auth = Checkbutton(label_frame_smtp, text="Authentication Enabled", variable=is_auth_checked)
enable_auth.select()
enable_auth.grid(row=4, column=0)

is_tls_checked = IntVar()
enable_tls = Checkbutton(label_frame_smtp, text="Use TLS", variable=is_tls_checked)
enable_tls.select()
enable_tls.grid(row=4,column=1)

#Label(label_frame_smtp, text="").grid(row=4, sticky=W)
Separator(label_frame_smtp, orient='horizontal').grid(column=0, row=5, columnspan=2, sticky='ew')
Label(label_frame_smtp, text="").grid(row=6, sticky=W)
#From:
Label(label_frame_smtp, text="From:").grid(row=7, sticky=W)
smtp_from= StringVar()
input_smtp_from = Entry(label_frame_smtp, textvariable= smtp_from, show='', bg ='white', fg='black', width=30)
input_smtp_from.grid(row=7, column=1)

#To:
Label(label_frame_smtp, text="To:").grid(row=8, sticky=W)
smtp_to= StringVar()
input_smtp_to = Entry(label_frame_smtp, textvariable= smtp_to, show='', bg ='white', fg='black', width=30)
input_smtp_to.grid(row=8, column=1)

#Subject:
Label(label_frame_smtp, text="Subject:").grid(row=9, sticky=W)
smtp_subject= StringVar()
input_smtp_subject = Entry(label_frame_smtp, textvariable= smtp_subject, show='', bg ='white', fg='black', width=30)
input_smtp_subject.grid(row=9, column=1)

#Body:
Label(label_frame_smtp, text="Body:").grid(row=10, sticky=W)
smtp_body= StringVar()
input_smtp_body = Entry(label_frame_smtp, textvariable= smtp_body, show='', bg ='white', fg='black', width=30)
input_smtp_body.grid(row=10, column=1)

Button(label_frame_smtp, text="Send", command= lambda:sendMail(smtp_server.get(), smtp_port.get(), smtp_username.get(), smtp_password.get(), smtp_from.get(), smtp_to.get(), smtp_subject.get(), smtp_body.get())).grid(row=11, column=1, sticky='e')


###ftp section
##section
label_frame_ftp = LabelFrame(mainFrame, text="Check ftp", padx=20, pady=5)
label_frame_ftp.grid(row=0, column=1, sticky=N)

#server
Label(label_frame_ftp, text="Server:").grid(row=0, sticky=W)
ftp_server= StringVar()
input_ftp_server = Entry(label_frame_ftp, textvariable= ftp_server, show='', bg ='white', fg='black', width=30)
input_ftp_server.grid(row=0, column=1)

#port
Label(label_frame_ftp, text="Port:").grid(row=1, sticky=W)
ftp_port= StringVar()
input_ftp_port = Entry(label_frame_ftp, textvariable= ftp_port, text='', bg ='white', fg='black', width=30)
input_ftp_port.insert(0,'21')
input_ftp_port.grid(row=1, column=1)

#user
Label(label_frame_ftp, text="User:").grid(row=2, sticky=W)
ftp_user= StringVar()
input_ftp_user = Entry(label_frame_ftp, textvariable= ftp_user, text='', bg ='white', fg='black', width=30)
input_ftp_user.grid(row=2, column=1)

#password
Label(label_frame_ftp, text="Password:").grid(row=3, sticky=W)
ftp_password= StringVar()
input_ftp_password = Entry(label_frame_ftp, textvariable= ftp_password, show='*', bg ='white', fg='black', width=30)
input_ftp_password.grid(row=3, column=1)

is_auth_ftp_checked = IntVar()
enable_auth_ftp = Checkbutton(label_frame_ftp, text="Anonymous login", variable=is_auth_ftp_checked)
enable_auth_ftp.grid(row=4, column=0)

is_tls_ftp_checked = IntVar()
enable_tls_ftp = Checkbutton(label_frame_ftp, text="Use TLS", variable=is_tls_ftp_checked)
enable_tls_ftp.select()
enable_tls_ftp.grid(row=4,column=1)

Button(label_frame_ftp, text="Send", command= lambda:sendFtp(input_ftp_server.get(), input_ftp_port.get(), input_ftp_user.get(), input_ftp_password.get())).grid(row=5, column=1,sticky=E)

###Log section
##section
label_frame_log = LabelFrame(mainWin, text="Log", padx=10, pady=1)
label_frame_log.grid(row=1, column=0)

textPad = ScrolledText(label_frame_log, width=80, height=10)
textPad.config(state=DISABLED)
textPad.grid(row=0)


mainWin.mainloop()

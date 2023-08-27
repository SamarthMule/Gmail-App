from tkinter import *
from email.message import EmailMessage
from tkinter import messagebox, filedialog
import smtplib
import os
import imghdr

check = False

def attachment():
    global filename, filetype, filepath, check
    check = True
    filepath = filedialog.askopenfilename(initialdir='Python Projects\Gmail app', title='Select File')
    filetype = filepath.split('.')
    filetype = filetype[1]
    filename = os.path.basename(filepath)
    text_area.insert(END, f'\n{filename}\n')


def sendingEmail(toAddress, subject, body):
    f = open('settings.txt', 'r')
    for i in f: credentials = i.split(',')
    message = EmailMessage()
    message['subject'] = subject
    message['to'] = toAddress
    message['from'] = credentials[0]
    message.set_content(body)
    if check:
        if filetype == 'png' or filetype == 'jpg' or filetype == 'jpeg':
            f = open(filepath, 'rb')
            file_data = f.read()
            subtype = imghdr.what(filepath)

            message.add_attachment(
                file_data, maintype='image', subtype=subtype, filename=filename)

        else:
            f = open(filepath, 'rb')
            file_data = f.read()
            message.add_attachment(
                file_data, maintype='application', subtype='octet-stream', filename=filename)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(credentials[0], credentials[1])
    s.send_message(message)
    x = s.ehlo()
    if x[0] == 250: return 'sent'
    else: return 'failed'

def send_email():
    if toEntryField.get() == '' or subjectEntry.get() == '' or text_area.get(1.0, END) == '\n':
        messagebox.showerror('Error', 'All Fields Are Required', parent=root)

    else:
        result = sendingEmail(
            toEntryField.get(), subjectEntry.get(), text_area.get(1.0, END))
        if result == 'sent':
            messagebox.showinfo('Success', 'Email is sent successfulyy')
        if result == 'failed':
            messagebox.showerror('Error', 'Email is not sent.')

        messagebox.showinfo('Success', 'Emails are sent successfully')


def settings():
    def clear1():
        fromEntryField.delete(0, END)
        passwordEntryField.delete(0, END)

    def save():
        if fromEntryField.get() == '' or passwordEntryField.get() == '':
            messagebox.showerror('Error', 'All Fields Are Required', parent=rootN)

        else:
            f = open('settings.txt', 'w')
            f.write(fromEntryField.get()+','+passwordEntryField.get())
            f.close()
            messagebox.showinfo('Information', 'CREDENTIALS SAVED SUCCESSFULLY', parent=rootN)

    rootN = Toplevel()
    rootN.title('Setting')
    rootN.geometry('650x340+350+90')
    icon = PhotoImage(file="setting.png")
    root.iconphoto(True,icon)
    rootN.resizable(False, False)

    rootN.config(bg='lightgreen')

    Label(rootN, text='Your Information', image=logo, compound=LEFT,
          font=('goudy old style', 40, 'bold'),fg='green', bg='lightgreen').grid(padx=60)

    fromLabelFrame = LabelFrame(rootN, text=' From (Email Address) ',
                                font=('times new roman', 19, 'bold'), bd=5, fg='gold',bg='green')
    fromLabelFrame.grid(row=1, column=0, pady=20)

    fromEntryField = Entry(fromLabelFrame, font=(
        'times new roman', 18, 'bold'), width=30)
    fromEntryField.grid(row=0, column=0)

    passwordLabelFrame = LabelFrame(rootN, text=' Password ',
                                    font=('times new roman', 19, 'bold'), bd=5,fg='gold',bg='green')
    passwordLabelFrame.grid(row=2, column=0, pady=20)

    passwordEntryField = Entry(passwordLabelFrame, font=(
        'times new roman', 18, 'bold'), width=30, show='*')
    passwordEntryField.grid(row=0, column=0)

    Button(rootN, text='SAVE', font=('times new roman', 18, 'bold'),cursor='hand2', bg='green',
           fg='lightgreen', command=save,activebackground="lightgreen",activeforeground="green"
           ).place(x=210, y=280)
    Button(rootN, text='CLEAR', font=('times new roman', 18, 'bold'),cursor='hand2', bg='green',
           fg='lightgreen', command=clear1,activebackground="lightgreen",activeforeground="green"
           ).place(x=340, y=280)

    f = open('setting.txt', 'r')
    for i in f: credentials = i.split(',')

    fromEntryField.insert(0, credentials[0])
    passwordEntryField.insert(0, credentials[1])

    rootN.mainloop()

def exit():
    result = messagebox.askyesno('Exit', 'Do you want to exit?')
    if result: root.destroy()
    else: pass

def clear():
    toEntryField.delete(0, END)
    subjectEntry.delete(0, END)
    text_area.delete(1.0, END)

root = Tk()
root.title('EMAIL APPLICATION GUI')
root.geometry('830x650')
root.config(bg='lightgreen')
icon = PhotoImage(file="logo.png")
root.iconphoto(False,icon)
root.resizable(False, False)

Frame_Title = Frame(root, bg='lightgreen')
Frame_Title.grid(row=0, column=0,pady=10)
logo = PhotoImage(file='email.png')
Label_Title = Label(Frame_Title, text=" SAMARTH'S EMAIL APPLICATION", image=logo, compound=LEFT,
                    font=('luicda', 30, 'bold'),bg='lightgreen')
Label_Title.grid(row=0, column=0)
settingIMG = PhotoImage(file='setting.png')

Button(Frame_Title, image=settingIMG, bd=0, bg='lightgreen', cursor='hand2',
       activebackground='lightgreen', command=settings).grid(row=0, column=1, padx=5,pady=5)

toLabelFrame = LabelFrame(root, text=' To ', font=(
    'times new roman', 19, 'bold'), fg='gold', bg='green')
toLabelFrame.grid(row=2, column=0,pady=10,padx=15)

toEntryField = Entry(toLabelFrame, font=(
    'times new roman', 18, 'bold'), width=62)
toEntryField.grid(row=0, column=0)

subjectLabelFrame = LabelFrame(root, text=' Subject ', font=('times new roman', 19, 'bold'),fg='orange', bg='green')
subjectLabelFrame.grid(row=3, column=0, pady=10,padx=15)

subjectEntry = Entry(subjectLabelFrame, font=('times new roman', 18, 'bold'), width=62)
subjectEntry.grid(row=0, column=0,pady=5,padx=15)

emailLabelFrame = LabelFrame(root, text=' Message ', font=(
    'times new roman', 19, 'bold'),fg='yellow', bg='green')
emailLabelFrame.grid(row=4, column=0, pady=10,padx=5)

attachImage = PhotoImage(file='attachments.png')

Button(emailLabelFrame, image=attachImage, compound=LEFT, font=('arial', 12, 'bold'),cursor='hand2', bd=0,
       bg='lightgreen', activebackground='lightgreen', command=attachment).grid(row=4, column=2)

text_area = Text(emailLabelFrame, font=('times new roman', 14,), height=8)
text_area.grid(row=1, column=0, columnspan=2)

ButtonFrame = LabelFrame(root, text=' Buttons ', font=(
    'times new roman', 19, 'bold'),fg='darkgreen', bg='lightgreen',bd=0)
ButtonFrame.grid(row=5, column=0, padx=20)

Button(ButtonFrame, text='Send', bd=0, bg='green', fg='lightgreen', font='lucida 17 bold',
       activebackground="lightgreen",activeforeground="green",
       cursor='hand2', command=send_email).grid(row=5,column=1,pady=10,padx=10)


Button(ButtonFrame, text='Clear', bd=0, bg='green', fg='lightgreen', font='lucida 17 bold',
       activebackground="lightgreen",activeforeground="green",
       cursor='hand2', command=clear).grid(row=5,column=2,pady=10,padx=10)


Button(ButtonFrame, text='Exit', bd=0, bg='green', fg='lightgreen', font='lucida 17 bold',
       activebackground="lightgreen",activeforeground="green",
       cursor='hand2', command=exit).grid(row=5,column=3,pady=10,padx=10)

root.mainloop()
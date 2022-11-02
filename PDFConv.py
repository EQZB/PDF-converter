#PDF Converter here we go!
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkPDFViewer import tkPDFViewer as pdf
from tkinterdnd2 import DND_FILES, TkinterDnD
import fitz
import os
import re

###--------------tkinter case--------------###
root = TkinterDnD.Tk()
root.geometry("600x400")
root.title("PDF Converter")
root.configure(bg="pink")

###-------------set frames-------------------###
mainframe = Frame(root, bg="pink")
mainframe.pack()

#####-----------------FUNCTIONS--------------------#####

###-----------clear listbox--------------------###
def clear_box():
    mainframe_LB.delete(1,END)

###------------search pdf files-----------------###
v2 = None
def check_file():
    global v2
    
    #get the entry from the view_entry textbox
    filename=mainframe_LB.get(1)
    if filename:
        if filename.endswith(".pdf") == False:
            clean_string=re.sub('[{}]','',filename)
        else:
            clean_string=filename
            
        #destroy old file if it exists
        if v2:
            v2.destroy()
        #create new pdf images  
        v1=pdf.ShowPdf()
        #clear stored images
        v1.img_object_li.clear()
        #set a new pop out window
        newWindow=tkinter.Toplevel(mainframe)
        #store new images
        v2=v1.pdf_view(newWindow, pdf_location=open(clean_string,"r"), height=50, width=80)
        v2.pack(pady=(0,0))

###----------------select destination folder------------###
dest_folder = None
def sel_dest_fold():
    folder=filedialog.askdirectory(initialdir=os.getcwd(), title="Select Destination Folder")
    global dest_folder
    dest_folder = folder
    dest_LB.delete(0)
    dest_LB.insert(1, folder)
   
    
###-------------converting pdf to txt files------------###
def convert_pdf():
    
    #get filename
    filename=mainframe_LB.get(1)
    if filename:
        if filename.endswith(".pdf") == False:
            clean_string=re.sub('[{}]','',filename)
        else:
            clean_string=filename
    
    #convert pdf to string
    pymupdf_text=""
    try:
        with fitz.open(clean_string) as doc:
            for page in doc:
                pymupdf_text += page.getText()
                txtfile = open(dest_folder + "/" +"PDF-to-text File.txt", "w", encoding="utf-8")   
        txtfile.write(pymupdf_text)
        newWindow = tkinter.Toplevel()
        newWindow.geometry("300x60+100+100")
        newWindow.title("Conversion Notification")
        Label(newWindow, text="Conversion Successful! See destination folder.").pack(side=TOP, ipadx=5,ipady=2, expand=True)
        Button(newWindow, text="OK", command=newWindow.destroy, bd=5).pack()
   
    except:
        newWindow = tkinter.Toplevel()
        newWindow.geometry("200x60")
        newWindow.title("Conversion Notification")
        Label(newWindow, text="Conversion Unsuccessful!").pack(fill="both")
        Button(newWindow, text="OK", command=newWindow.destroy, bd=5).pack()

    txtfile.close()

###-------------set buttons/boxes-----------------###
check_butt = Button(mainframe, text="CHECK PDF FILE", command=check_file, width=50, bd=5)
check_butt.pack()
mainframe_LB = Listbox(mainframe, width=50, height=2, bd=1)
mainframe_LB.insert(1,"Drag the PDF that you want to convert here:")
mainframe_LB.drop_target_register(DND_FILES)
mainframe_LB.dnd_bind('<<Drop>>', lambda e: mainframe_LB.insert(tkinter.END, e.data))
mainframe_LB.pack()
clear_butt = Button(mainframe, text="CLEAR", command=clear_box, width=50, bd=5)
clear_butt.pack()
convert_butt = Button(mainframe, text="CONVERT TO .TXT FILE", command=convert_pdf, width=50, bd=5)
convert_butt.pack()
dest_butt = Button(mainframe, text="Select Destination Folder", command=sel_dest_fold, width=50, bd=5)
dest_butt.pack()
dest_LB = Listbox(mainframe, width=50, height=1, bd=1)
Label(mainframe, text="Destination Folder", height=1).pack(side=BOTTOM)
dest_LB.pack()



root.mainloop()

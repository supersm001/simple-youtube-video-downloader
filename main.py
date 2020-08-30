from pytube import *
from tkinter.filedialog import *
import sys
from tkinter.messagebox import *
from threading import *


def getInfo():
    try:

        url = text.get()
        print(url)
        getInfoButton.config(text="Wait...")
        getInfoButton.config(state=DISABLED)
        ob = YouTube(url)

        st = ob.streams.first()
        st2 = ob.streams.filter(progressive=True)
        for items in st2:
            option = str(items.itag) + "    " + items.mime_type + "     " + str(items.resolution) + "       " + \
                     str(int(items.filesize/1000000)) + 'MB' + "\n"
            getList.insert(END, option)

        vTitle.config(text=st.title, fg="black")
        getInfoButton.config(text="Get Info")
        getInfoButton.config(state=NORMAL)

    except Exception as e:
        print(e)
        vTitle.config(text="ERROR!!! Invalid Link", fg="red")


def download():
    try:

        button.config(text="Please Wait...")
        button.config(state=DISABLED)
        path = askdirectory()
        print(path)
        if path is None:
            return

        select = getList.curselection()
        selected = getList.get(select)
        vid = selected.split("  ")[0]
        url = text.get()
        ob = YouTube(url)

        video = ob.streams.get_by_itag(vid)

        video.download(path)

        button.config(text="Start Download")
        button.config(state=NORMAL)
        showinfo("Download Finished", "Downloaded Successfully")
        text.delete(0, END)

    except Exception as e:
        print(e)
        vTitle.config(text="ERROR!!! Invalid Link", fg="red")
        button.config(text="Start Download")
        button.config(state=NORMAL)
        text.delete(0, END)


def downloadThread():
    thread = Thread(target=download)
    thread.start()


def infoThread():
    thread = Thread(target=getInfo)
    thread.start()


main = Tk()
main.iconbitmap(os.path.join(sys.path[0], "Download.ico"))
main.title("YouTube Video Downloader")
main.geometry("630x620")
main.resizable(False, False)

label = Label(main, font=('arial', 20, 'bold'), text="Paste Video Link Here")
label.place(x=160, y=10)
img = PhotoImage(file="hand.png")

label2 = Label(main, image=img)
label2.place(x=270, y=50)

text = Entry(main, font=('arial', 20, 'bold'), justify=CENTER, width=39, bd=4)
text.place(x=20, y=110)

getInfoButton = Button(main, font=('arial', 20, 'bold'), text="Get List", bd=6, fg='red', command=infoThread)
getInfoButton.place(x=230, y=160)

Title = Label(main, font=('arial', 8, 'bold'), justify=CENTER, text="Title of File :")
Title.place(x=20, y=220)

vTitle = Label(main, font=('arial', 8, 'bold'), justify=CENTER, text="", fg="black")
vTitle.place(x=20, y=240)

Title2 = Label(main, font=('arial', 10, 'bold'), justify=CENTER, text="Choose your resolution :")
Title2.place(x=20, y=270)

getList = Listbox(main,  font=('arial', 10, 'bold'), height=14, width=83, bd=4)
getList.place(x=20, y=290)


button = Button(main, font=('arial', 20, 'bold'), text="Start Download", bd=6, fg='red', command=downloadThread)
button.place(x=180, y=550)


main.mainloop()

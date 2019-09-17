from Tkinter import *
from os import listdir,remove
from os.path import isfile, join,dirname,realpath


class FileListViewer:

    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        scrollbar = Scrollbar(top)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.Lb1 = Listbox(top,selectmode=MULTIPLE,yscrollcommand=scrollbar.set)

        self.B = Button(top, text="Delete", command=self.deleteFiles)


        dir_path = dirname(realpath(__file__) )+ "/loops"
        print dir_path
        onlyfiles = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
        for i in onlyfiles:
            self.Lb1.insert(END,i)
        self.Lb1.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=self.Lb1.yview)
        self.B.pack()

    def ok(self):

        self.top.destroy()

    def showDlg(self):
        q = FileListViewer(root)

    def deleteFiles(self):
        reslist = list()
        stem = dirname(realpath(__file__) )+ "/loops"
        seleccion = self.Lb1.curselection()
        for i in seleccion:
            entrada = self.Lb1.get(i)
            reslist.append(entrada)
        for val in reslist:
            print(val)
            if isfile(stem + "/" + val):
                remove(stem + "/" + val)
                print "deleted"


def showFileList():
    d = FileListViewer(root)

root = Tk()

Button(root, text="Hello!", command=showFileList).pack()
root.update()



root.mainloop()
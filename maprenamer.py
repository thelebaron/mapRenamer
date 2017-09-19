
import subprocess, os, errno, shutil
import tkinter as tk
import os.path

from enum import Enum
from shutil import copyfile
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askopenfilenames
from tkinter.messagebox import showerror
import tkinter.messagebox
from _thread import start_new_thread

#pretty sure this can be refactored

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
    """
    def add():
        global x
        x += 1
        w.config(text=x)
        label.config(text=x)
    """
    def testInt(s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
    def create_widgets(self):
        global testOnly
        testOnly = False
        global verbose
        verbose = 0
        strvar = tk.StringVar()
        strvar.set('map renamer')
        self.w = tk.Label(self, textvariable=strvar,font=("Helvetica", 16))
        self.w.pack()

        self.checkboxTest = tk.BooleanVar()
        self.chkUDIM = tk.BooleanVar()
        self.chkZBR = tk.BooleanVar()
        self.chkMUD = tk.BooleanVar()

        self.fuzzyspellingvariable = tk.BooleanVar()
        global var
        var = tk.StringVar()
        var.set("default")

        self.butt1 = tk.Button(self, fg="green")
        self.butt1["text"] = "File Input\n(to rename)"
        self.butt1["command"] = self.load_files
        self.butt1.pack(side="top")

        self.butt2 = tk.Button(self, fg="orange")
        self.butt2["text"] = "verbosity"
        self.butt2["command"] = self.toggleVerbose
        self.butt2.pack(side="top")

        """
        self.butt3 = tk.Button(self, fg="blue")
        self.butt3["text"] = "showType"
        self.butt3["command"] = self.identifyUVConvention
        self.butt3.pack(side="top")
        """
        #debug text
        #debug text
        #debug text
        #debug text


        self.label = tk.Label(self, text="no file input")
        self.label.pack()

        self.label2 = tk.Label(self, text="0 files")
        self.label2.pack()

        # checkboxes
        self.chk = tk.Checkbutton(self, name="checkbox_Test",variable=self.checkboxTest)
        self.chk["command"] = self.checkbxTestDef
        self.chk["text"] = "test only(debug output without renaming)"
        self.chk.pack(side="top")


        """
        # checkboxes
        self.chk = tk.Checkbutton(self, name="chk_mar",variable=self.chkUDIM)
        self.chk["command"] = self.checkUdi
        self.chk["text"] = "mari(udim)"
        self.chk.pack(side="top")

        self.contents = tk.Checkbutton(self,name="chk_mud",variable=self.chkMUD)
        self.contents["command"] = self.checkMud
        self.contents["text"] = "mudbox"
        self.contents.pack(side="top")

        self.contents = tk.Checkbutton(self,name="chk_zb",variable=self.chkZBR)
        self.contents["command"] = self.checkZb
        self.contents["text"] = "zbrush"
        self.contents.pack(side="top")
        """


        #quitter
        self.quit = tk.Button(self, text="QUIT", fg="black", command=root.destroy)
        self.quit.pack(side="bottom")


        #textbox
        self.T = tk.Text(root, height=32, width=125)
        self.T.pack()
        self.T.insert('1.0', "Awaiting\na file\n")

    def logError(self):
        #showerror("debug:"% contents)
        if self.fuzzyspellingvariable.get():
            self.var.set("true")
            messageDetails = "true"
            self.T.delete("1.0", tkinter.END)
            self.T.insert('1.0', "yargh")
        else:
            self.var.set("false")
            messageDetails = "false"
            self.T.insert('1.0', "rargh")
            
        showerror(title="debug:",message=messageDetails)

    
    
    def checkUdi(self):
        if self.chkUDIM.get():
            self.T.delete("1.0", tkinter.END)
            self.T.insert('1.0', "UDIM")
            var = "UDIM"
    def checkbxTestDef(self):
        

        global testOnly

        if self.checkboxTest.get():
            testOnly = True
            self.T.delete("1.0", tkinter.END)
            self.T.insert('1.0', "dont rename, test only")
        else:
            testOnly = False
            self.T.delete("1.0", tkinter.END)
            self.T.insert('1.0', "rename on")
            
        
    def checkMud(self):
        if self.chkMUD.get():
            self.T.delete("1.0", tkinter.END)
            self.T.insert('1.0', "Mudbox")
            var = "Mudbox"
    def checkZb(self):
        if self.chkZBR.get():
            self.T.delete("1.0", tkinter.END) #delete textbox text
            self.T.insert('1.0', "Zbrush")
            var = "Zbrush"

    def identifyUVConvention(self):
        global uv_conv
        #1 = udim, 2 = mudbox style, 3 = zbrush style
        uv_conv = 0


        keyword_mud = "_v"
        if uvConvString.isdigit():
            uv_conv = 1
        if keyword_mud in originalFilename:
            uv_conv = 2
            

        """
        if keyword_mud in originalFilename:
            uv_conv = 2
            #showerror("Open Source File", "Mudbox/Uv1 format found in file\n'%s'" % uv_conv)

        keyword_udim = "10" #need to adjust this later
        
        if keyword_udim in originalFilename:
            uv_conv = 1
            #showerror("Open Source File", "UDIM format found in file\n'%s'" % uv_conv)

        keyword_udim = "1099" #special case
        
        if keyword_udim in originalFilename:
            uv_conv = 1
            #showerror("Open Source File", "UDIM format found in file\n'%s'" % uv_conv)

        """
        
        
        if uv_conv == 0:
            uv_conv = 0
            showerror("Error Source File", "No uv naming convention found? in\n'%s'" % originalFilename)


    #------------------------------------------------#
    def identifyCoordinates(self):
        global zz
        global x
        global y
        global outputConvention

        #process mudbox style input
        if uv_conv == 2:
            x,y = filenameWithoutExtension.split("_v")
            
            junk,x = x.split("_u")
            #showerror("Error Source File", "show\n'%s'" % y)

            
            zz = "_u"+ str(x)+"_v"+str(y)
            #as coords start at 0,0
            x = int(x)-1
            y = int(y)-1

            #showerror("Debug", "conv y is\n'%s'" % y)
            #self.T.delete("1.0", tkinter.END) #delete textbox text
            if verbose > 1:
                
                self.T.insert('1.0',  "\n" )
                self.T.insert('1.0', y)
                self.T.insert('1.0', " y coord is ")
                self.T.insert('1.0', x)
                self.T.insert('1.0', " x coord is ")
                self.T.insert('1.0', " uv(mudbox) processed: ")
                self.T.insert('1.0',  "\n" )
            
        
            desiredUdim = 1000 +(x+1)+(y*10)
            if verbose > 1:
                self.T.insert('1.0', desiredUdim)
                self.T.insert('1.0', " | Udim: ")
            #showerror("Debug", "Desired udim is\n'%s'" % desiredUdim)

            outputConvention = str(desiredUdim)
            #self.T.delete("1.0", tkinter.END) #delete textbox text
            if verbose > 1:
                #self.T.insert('1.0', outputConvention)
                self.T.insert('1.0',  "\n" )

        #process mari style
        if uv_conv == 1:
            #CONVERSION
            y1 = int(uvConvString[1])
            y2 = int(uvConvString[2])
            yy = str(y1)+str(y2)

            x = int(uvConvString[3])
            if x==0: #special case for say 10(1010 is x10), for this conversion process
                x = 10
                y = int(yy) - 1
            else:
                y = int(yy)

            #showerror("Debug", "conv y is\n'%s'" % y)
            
            if verbose > 1:
                self.T.insert('1.0',  "\n" )
                self.T.insert('1.0', y)
                self.T.insert('1.0', " y coord is ")

            #as coords start at 0,0 also y coord already does this
            x -= 1
            if verbose > 1:
                self.T.insert('1.0', x)
                self.T.insert('1.0', "x coord is ")
                self.T.insert('1.0', " udim(mari) processed: ")
                self.T.insert('1.0',  "\n" )
            #self.T.insert('1.0', convention)
            #xy = 0.0
            #showerror("UV coord debug", "Coords\n'%s'" % x)
            #maths: 1000+(u+1)+(v*10)

            y += 1#again because uv coords on this format start at 1 instead of 0
            if verbose > 1:
                self.T.insert('1.0', y)
                self.T.insert('1.0', "_v")
            x += 1#again because uv coords on this format start at 1 instead of 0
            if verbose > 1:
                self.T.insert('1.0', x)
                self.T.insert('1.0', "_u")
                self.T.insert('1.0', " | uv style: ")
                

            outputConvention = "_u" + str(x) + "_v" + str(y)
            #self.T.delete("1.0", tkinter.END) #delete textbox text
            if verbose > 1:
                #self.T.insert('1.0', outputConvention)
                self.T.insert('1.0',  "\n" )

            
    def load_files(self):
        global user_input
        user_input = askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("all files","*.*"),("all files","*.*")))
        if verbose == 0:
            self.T.delete("1.0", tkinter.END) #delete textbox text
            
        self.T.insert('1.0', " files loaded ")
        self.T.insert('1.0',  len(user_input) )
        self.T.insert('1.0',  "\n" )
        filesforlabel = str(len(user_input)) + " files renamed"
        self.label2.configure(text=filesforlabel)

        if user_input:
            global input_fileList
            input_fileList = root.tk.splitlist(user_input)

            for fName in input_fileList:
                self.T.insert('1.0',  "\n" )
                self.T.insert('1.0',  fName )
                self.T.insert('1.0', "input: ")

                #self.T.insert('1.0', "loop")
                global originalFilename
                global path
                path, originalFilename = os.path.split(fName)#[1]

                global extension
                extension = os.path.splitext(originalFilename)[1]
                global filenameWithoutExtension
                filenameWithoutExtension, junk = originalFilename.split(extension)
                self.label.configure(text=filenameWithoutExtension)









                #int filename length ie filename.1001.ext or filename_u1_v1.ext
                global len_filename_UV_Ext
                len_filename_UV_Ext = len(originalFilename)

                #int filename length without ext ie filename.1001 or filename_u1_v1
                extLength = len(extension)
                global len_filename_UV
                len_filename_UV = len_filename_UV_Ext - len(extension) #for the extension
                #get the uv name convention
                

                


                global uvConvString                
                uvConvString = str(originalFilename[len_filename_UV-4:len_filename_UV])

                self.identifyUVConvention()

                self.identifyCoordinates()

                #int filename without ext or uv scheme ie filename or filename
                global nameLen
                if uv_conv != 1: #if its not mari style...TODO WHAT IF ITS u100_v100??
                    nameLen = len_filename_UV - len(zz) #for the uv segment
                else:
                    nameLen = len_filename_UV - 4 #for the uv segment
                
                #chop it up
                filename = str(originalFilename[0:nameLen]) 
                global convention
                convention = originalFilename[nameLen:len_filename_UV]
                

                #self.T.delete("1.0", tkinter.END) #delete textbox text
                #filename
                
                #if verbose > 1:
                    #self.T.insert('1.0', convention)#"file read"
                
                #showerror("Open Source File", "out \n'%s'" % outputConvention)
    
                self.T.insert('1.0', filename)
                self.T.insert('1.0', "filename -")
                newFilename = filename + outputConvention
                newOutput = path + "/" + newFilename + extension
                
                global testOnly
                if not testOnly:
                    os.rename(fName,newOutput)

                self.T.insert('1.0',  "\n" )
                self.T.insert('1.0',  newOutput )
                self.T.insert('1.0', "output: ")

            #self.T.delete("1.0", tkinter.END) #delete textbox text
            #self.T.insert('1.0', user_input)#"file read"
            #shutil.copy2(user_input, 'C:\\delicious')
            #shutil.copy2('C:\\spam.txt', 'C:\\delicious')
            #try:
                #shutil.copy('C:\\spam.txt', 'C:\\delicious')
                #print("""here it comes: self.settings["template"].set(user_input)""")
            #except:                     # <- naked except is a bad idea
                #showerror("Open Source File", "Failed to read file\n'%s'" % user_input)
        else:
            #self.T.delete("1.0", tkinter.END) #delete textbox text
            self.T.insert('1.0', "operation cancelled")
    

    def toggleVerbose(self):
        global verbose
        
        if verbose < 3:
            verbose += 1
        else:
            verbose = 0

        #showerror("Verbosity", verbose)
        self.T.delete("1.0", tkinter.END)
        #global var
        #self.label.config(text="var", width=50)
        self.label.configure(text="verbose on")
        if verbose == 0:
            self.label.configure(text="verbose off")
        if verbose ==1 :
            self.label.configure(text="verbose 1")
        if verbose ==2 :
            self.label.configure(text="verbose 2")
        if verbose ==3 :
            self.label.configure(text="verbose 3")
            
        self.label.update_idletasks()
    






#-------------------------------------------------------------------------------
# GUI
#-------------------------------------------------------------------------------

# Create root window object

root = tk.Tk()
root.title("chris' awesome mapRenamer")
root.tk.call('wm', 'iconbitmap', root._w, '-default', 'icon.ico')
root.minsize(100,100)
root.maxsize(400, 400)

app = Application(master=root)
app.mainloop()
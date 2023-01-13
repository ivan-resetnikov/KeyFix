from tkinter import Tk, Frame, Button, Label, Entry, Scrollbar, TclError, PhotoImage
from tkinter import ttk
Notebook = ttk.Notebook

from os   import system, path, makedirs, environ
from json import load,   dump

from keyboard import add_hotkey, unhook_all_hotkeys, press_and_release
from time     import sleep



def loadFromFile (path) :
    with open(path, 'r', encoding='utf8') as file : return load(file)

def writeToFile (path, content) :
    with open(path, 'w', encoding='utf8') as file : return dump(content, file, ensure_ascii=True, indent=2)



# layout.json file is where your hotkeys for games saved.
# You can found it at C:\Users\<USERNAME>\AppData\Local\KeyFix\layout.json


class Application :
    def __init__ (self) :
        self.root = Tk()
        self.root.geometry('620x400')
        self.root.title('KeyFix | V 1.0')
        self.root.resizable(0, 1)
        self.root.iconphoto(False, PhotoImage(file='icon.png'))

        self.layout = {}


        appdataPath = environ['APPDATA']
        self.layoutPath = f'{appdataPath}\\KeyFix\\layout.json'

        # create "KeyFix" folder in "appdata\Local", if it not exist
        if not path.exists(f'{appdataPath}\\KeyFix') :
            makedirs(f'{appdataPath}\\KeyFix')

        # create "layout.json" file, if it not exist
        if not path.exists(self.layoutPath) :
            with open(self.layoutPath, 'w') as file : file.write('{}')


    def loadTabs (self) :
        self.layout = loadFromFile(self.layoutPath)
        gamesList = list(self.layout.keys())

        for tab in self.tabControl.tabs() :
            self.tabControl.forget(tab)

        for game in gamesList :
            frame = Frame(self.tabControl)
            self.tabControl.add(frame, text=game)

            for y, hotkey in enumerate(self.layout[game]) :
                Label(frame, text=hotkey[0]).grid(row=y, column=1)
                Label(frame, text=hotkey[1]).grid(row=y, column=3)
                Label(frame, text=f'{y}:').grid(row=y, column=0)
                Label(frame, text='->').grid(row=y, column=2)


    def addGame (self) :
        self.layout[self.addGameEntry.get()] = []
        writeToFile(self.layoutPath, self.layout)
        self.loadTabs()


    def addShortcut (self) :
        self.layout[self.tabControl.tab(self.tabControl.select(), 'text')].append([self.addShortcutEntry0.get(), self.addShortcutEntry1.get()])
        writeToFile(self.layoutPath, self.layout)
        self.loadTabs()


    def shortcut (self, key) :
        sleep(0.5)
        print(123132321132)
        press_and_release(key)


    def startShortcuts (self) :
        try : unhook_all_hotkeys()
        except AttributeError : pass

        for shortcut in self.layout[self.tabControl.tab(self.tabControl.select(), 'text')] :
            add_hotkey(shortcut[0], self.shortcut, args=(shortcut[1],))


    def run (self) :
        self.showKeys = Button(self.root, text='Show availible keys', command=lambda : system('start keys.txt')).pack(padx=15, pady=7, fill='both')
        self.startKeyFixer = Button(self.root, text='Start hotkeys',  command=self.startShortcuts)              .pack(padx=15, pady=7, fill='both')

        ##### add new game #####
        self.addPanel = Frame(self.root)
        self.addGamePanel     = Frame(self.addPanel, highlightbackground="gray", highlightthickness=1)
        self.addShortcutPanel = Frame(self.addPanel, highlightbackground="gray", highlightthickness=1)

        Button(self.addGamePanel,     text='Add game',     command=self.addGame    ).grid(row=0, column=0, padx=5, pady=15)
        Button(self.addShortcutPanel, text='Add shortcut', command=self.addShortcut).grid(row=0, column=2, padx=5, pady=15)

        self.addGameEntry = Entry(self.addGamePanel)
        self.addGameEntry.grid(row=0, column=1, padx=5, pady=15)

        self.addShortcutEntry0 = Entry(self.addShortcutPanel)
        self.addShortcutEntry1 = Entry(self.addShortcutPanel)

        self.addShortcutEntry0.grid(row=0, column=3, padx=5, pady=15)
        self.addShortcutEntry1.grid(row=0, column=4, padx=5, pady=15)

        ######### tabs #########
        self.tabControl = Notebook(self.root)

        self.loadTabs()

        self.addPanel.pack(padx=15, pady=15, fill='both')

        self.addGamePanel.grid(row=0, column=0, padx=5)
        self.addShortcutPanel.grid(row=0, column=1, padx=5)

        self.tabControl  .pack(padx=15, pady=15, expand=1, fill='both')

        self.root.mainloop()



if __name__ == '__main__' :
    Application().run()

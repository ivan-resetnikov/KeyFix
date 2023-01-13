from tkinter import Tk, PhotoImage, StringVar, HORIZONTAL
from tkinter import ttk

Notebook   = ttk.Notebook
Frame      = ttk.Frame
Button     = ttk.Button
Label      = ttk.Label
Entry      = ttk.Entry
OptionMenu = ttk.OptionMenu
Labelframe = ttk.Labelframe
Scale      = ttk.Scale

from theme.customTitleBar import CustomTitle

from os   import system, path, makedirs, environ
from json import load,   dump

from keyboard import add_hotkey, unhook_all_hotkeys, press_and_release
from time     import sleep

from ctypes import windll, c_int, byref, sizeof



def loadFromFile (path) :
    with open(path, 'r', encoding='utf8') as file : return load(file)

def writeToFile (path, content) :
    with open(path, 'w', encoding='utf8') as file : return dump(content, file, ensure_ascii=True, indent=2)




# layout.json file is where your hotkeys for games saved.
# You can found it at C:\Users\<USERNAME>\AppData\Roaming\KeyFix\layout.json

class Application :
    def __init__ (self) :
        self.root = Tk()
        self.root.geometry('775x700+100+100')
        self.root.title('KeyFix V 1.2 (c) 2023 - TheUnknownDev')
        self.root.resizable(0, 0)
        self.root.iconphoto(0, PhotoImage(file='icon.png'))

        self.root.tk.call('source', 'theme.tcl')

        self.layout = {}

        self.pressDuration = 0.5
        self.latency = self.pressDuration

        # path to "AppData\Roaming" folder
        appdataPath = environ['APPDATA']

        ################# Layout #################
        self.layoutPath = f'{appdataPath}\\LowRezCat\\KeyFix\\layout.json'

        # create "LowRezCat" folder in "appdata\Local", if it not exist
        if not path.exists(f'{appdataPath}\\LowRezCat') :
            makedirs(f'{appdataPath}\\LowRezCat')

        # create "KeyFix" folder in "appdata\Local", if it not exist
        if not path.exists(f'{appdataPath}\\LowRezCat\\KeyFix') :
            makedirs(f'{appdataPath}\\LowRezCat\\KeyFix')

        # create "layout.json" file, if it not exist
        if not path.exists(self.layoutPath) :
            with open(self.layoutPath, 'w') as file : file.write('{}')


        ################# Themes ################# 
        self.availibleThemes = ['Choose theme', 'dark', 'light']

        self.preferencesPath = f'{appdataPath}\\LowRezCat\\KeyFix\\preferences.json'

        # create "preferences.json" file, if it not exist
        if not path.exists(self.preferencesPath) :
            with open(self.preferencesPath, 'w') as file : file.write('{"theme": "light"}')
            self.root.tk.call('set_theme', 'light')
            self.theme = 'light'

        else :
            self.theme = loadFromFile(self.preferencesPath)['theme']
            self.root.tk.call('set_theme', self.theme)


    def quitter (self, e):
        root.quit()
        #root.destroy()


    def loadTabs (self) :
        self.layout = loadFromFile(self.layoutPath)
        gamesList = list(self.layout.keys())

        for tab in self.tabControl.tabs() :
            self.tabControl.forget(tab)

        for game in gamesList :
            frame = Frame(self.tabControl)
            self.tabControl.add(frame, text=game)

            Button(frame, text='Remove game', command=self.removeGame).grid(row=0, column=0, columnspan=4, padx=5, pady=5)
            Button(frame, text='Remove last hotkey', command=self.removeHotkey).grid(row=0, column=4, columnspan=4, padx=5, pady=5)

            for y, hotkey in enumerate(self.layout[game]) :
                Label(frame, text=hotkey[0].upper()).grid(row=y+1, column=0)
                Label(frame, text=hotkey[1].upper()).grid(row=y+1, column=2)
                Label(frame, text='>').grid(row=y+1, column=1)




    def addGame (self) :
        if self.addGameEntry.get() != '' :
            self.layout[self.addGameEntry.get()] = []
            writeToFile(self.layoutPath, self.layout)
            self.loadTabs()


    def addShortcut (self) :
        if self.addShortcutEntry0.get() != '' and self.addShortcutEntry1.get() != '' :
            self.layout[self.tabControl.tab(self.tabControl.select(), 'text')].append([self.addShortcutEntry0.get(), self.addShortcutEntry1.get()])
            writeToFile(self.layoutPath, self.layout)
            self.loadTabs()


    def shortcut (self, key, duration) :
        sleep(float(duration))
        press_and_release(key)


    def startHotkeys (self) :
        try : unhook_all_hotkeys()
        except AttributeError : pass

        for shortcut in self.layout[self.tabControl.tab(self.tabControl.select(), 'text')] :
            add_hotkey(shortcut[0], self.shortcut, args=(shortcut[1], self.latency))


    def changeTheme (self, option) :
        self.root.tk.call('set_theme', self.themeVar.get())
        writeToFile(self.preferencesPath, {'theme': self.themeVar.get()})
        self.theme = self.themeVar.get()


    def removeHotkey (self) :
        self.layout[self.tabControl.tab(self.tabControl.select(), 'text')].pop()
        writeToFile(self.layoutPath, self.layout)
        self.loadTabs()


    def removeGame (self) :
        self.layout.pop(self.tabControl.tab(self.tabControl.select(), 'text'))
        writeToFile(self.layoutPath, self.layout)
        self.loadTabs()


    def showDuration (self, val) :
        try : self.duraionDisplay['text'] = 'Latency: ' + str((float(val[:4:]))*1000) + ' ms'
        except AttributeError : pass

        self.latency = val


    def run (self) :
        #### custom title bar ####
        if self.theme == 'dark' :
            bg = '#333333'
            fg = '#ffffff'
        else :
            bg = '#ffffff'
            fg = '#000000'
        self.titleBar = CustomTitle(self.root, title_text='Hello,World!', bg=bg, fg=fg)
        self.titleBar.resizeable = 1
        self.titleBar.packBar()

        #### show all keys #####
        self.showKeys = Button(self.root, text='Show availible keys', command=lambda : system('start keys.txt')).pack(padx=15, pady=10, fill='both')
        self.startKeyFixer = Button(self.root, text='Start hotkeys',  command=self.startHotkeys)              .pack(padx=15, pady=10, fill='both')

        ##### add new game #####
        self.addPanel = Frame(self.root)
        self.addGamePanel     = Labelframe(self.addPanel, text='Add game')
        self.addShortcutPanel = Labelframe(self.addPanel, text='Add shortcut')

        Button(self.addGamePanel,     text='Add game',     command=self.addGame    ).grid(row=0, column=0, padx=5, pady=15)
        Button(self.addShortcutPanel, text='Add shortcut', command=self.addShortcut).grid(row=0, column=2, padx=5, pady=15)

        self.addGameEntry = Entry(self.addGamePanel)
        self.addGameEntry.grid(row=0, column=1, padx=5, pady=15)

        ##### add shortcut #####
        self.addShortcutEntry0 = Entry(self.addShortcutPanel)
        self.addShortcutEntry1 = Entry(self.addShortcutPanel)

        self.addShortcutEntry0.grid(row=0, column=3, padx=5, pady=15)
        self.addShortcutEntry1.grid(row=0, column=4, padx=5, pady=15)

        ######### tabs #########
        self.tabControl = Notebook(self.root)

        self.loadTabs()

        self.addPanel.pack(padx=15, pady=15, fill='both')

        self.addGamePanel    .grid(row=0, column=0, padx=5)
        self.addShortcutPanel.grid(row=0, column=1, padx=5)

        self.tabControl.pack(padx=15, pady=15, expand=1, fill='both')

        #### charnge theme ####
        self.themeVar = StringVar(self.root)
        self.themeVar.set('Choose theme')

        self.themeBox = OptionMenu(self.root, self.themeVar, *self.availibleThemes, command=self.changeTheme)

        self.themeBox.pack(padx=15, pady=15, fill='both')

        #### press latency ####
        self.durationFrame = Labelframe(self.root, text='Latency')

        self.slider = Scale(self.durationFrame, variable=self.pressDuration, from_=0.25, to=2, orient=HORIZONTAL, command=self.showDuration)
        self.slider.set(self.pressDuration)

        self.duraionDisplay = Label(self.durationFrame)

        self.duraionDisplay.grid(row=0, column=1, padx=10, pady=10)
        self.slider        .grid(row=0, column=0, padx=10, pady=10)

        self.durationFrame.pack(padx=10, pady=10, fill='both')

        self.showDuration(str(self.pressDuration))

        self.root.mainloop()



if __name__ == '__main__' :
    Application().run()
from pytube import YouTube
import json
import os
import PySimpleGUI as sg

format = {
    "video":[]
}

open('data.json', 'a').close()

with open('data.json', 'r+') as database:
    try:
        json.load(database)
    except:
        json.dump(format, database, indent=4)


# Get video information and show on GUI
class videoInfo:
    def __init__(self, url):
        self.url = url
        try:
            self.yt = YouTube(url)
        except:
            sg.popup_error("Error", "Invalide URL")

    def getTitle(self):
        try:
            return self.yt.title
        except:
            pass
    
    def getAuthor(self):
        try:
            return self.yt.author
        except:
            pass

    def getViews(self):
        try:
            return self.yt.views
        except:
            pass

    def getRating(self):
        try:
            return self.yt.rating
        except:
            pass

with open('data.json') as json_file: 
    data = json.load(json_file) 
info = data['video']


class app:
    def __init__(self):
        self.info = info
        self.layout()
        global title
        title = []
        for i in range(0, len(info)):
            title.append(info[i]['title'])
            i += 1

    def layout(self):
        self.menu = [['File', ['Exit']],
                    ['Theme', ['Light', 'Dark']],
                    ['Help', 'About'],]


        self.windowLayout = [[sg.Menu(self.menu)],
            [sg.Text('Welcome to PyKeep', size=(40, 1), justification='center', font=("Helvetica", 25))],
            [sg.Text('URL'), sg.Input(key='-URL-', do_not_clear=False, size=(80, 1))],
            [sg.Text('Note'), sg.Input(key='-Note-', do_not_clear=False, size=(80, 1)), sg.Submit('Keep')],
            [sg.Listbox(values=[], size=(100, 8), enable_events=True, key='-Title-', pad=(5,10))],
            [sg.Button('Delete')],
            [sg.Multiline("URL: ", size=(100, 1), key='Info-1', pad=(5,10), right_click_menu= ['&Right', ['Copy']])],
            [sg.Listbox(values=["Author: ", "View: ", "Rating: ", "Note: "], size=(100, 8), key='Info-2', pad=(5,0))]]


    # Add video information to data.json
    def addInformation(self):
        getVideoInfo = videoInfo(self.userInput)
        videoTitle = getVideoInfo.getTitle()
        videoAuthor = getVideoInfo.getAuthor()
        videoView = getVideoInfo.getViews()
        videoRating = getVideoInfo.getRating()  
        # python object to be appended 
        if videoTitle:
            y = {
                "url": self.userInput,
                "title": videoTitle,
                "author": videoAuthor,
                "view": videoView,
                "rating": videoRating,
                "note": self.note
            }

            self.info.append(y)
            with open('data.json','w') as f: 
                json.dump(data, f, indent=4)

            for i in range(1,500):
                    sg.one_line_progress_meter('Progress Bar', i+1, 500, 'Uploading Information')

            title.append(info[-1]['title'])

    # Delete video info from data.json
    def deleteInformation(self):
        x = 0
        for x in range(0,len(info)):
            if str(('["' + info[x]['title'] + '"]')) == str(values['-Title-']) or str(("['" + info[x]['title'] + "']")) == str(values['-Title-']):
                self.info.pop(x)
                title.pop(x)
                self.window.FindElement('-Title-').Update(values=title)
                break
            elif str(values['-Title-']) == '[]':
                sg.popup_error('Error', "No item is selected")
                break
            x +=1

        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)


    def recordInfo(self):
        self.userInput = values['-URL-']
        self.note = values['-Note-']
        self.addInformation()
        self.window.FindElement('-Title-').Update(values=title)

    def readWindow(self):
        self.window = sg.Window("PyKeep", self.windowLayout, size=(700, 480), finalize=True)
        self.window.FindElement('-Title-').Update(values=title)
        while True:
            global values
            global event
            event, values = self.window.Read()
            if event in (None, 'Exit'):
                break
            elif event == 'Keep':
                self.recordInfo()
            elif event == 'Delete':
                sg.popup_annoying("Delete", "You have successfully deleted this item")
                self.deleteInformation()
            elif event == 'Dark':
                sg.ChangeLookAndFeel('Dark')
            elif event == '-Title-':
                for x in range(0,len(info)):
                    if str(('["' + info[x]['title'] + '"]')) == str(values['-Title-']) or str(("['" + info[x]['title'] + "']")) == str(values['-Title-']):
                        self.window.FindElement('Info-1').Update('URL:     ' + info[x]["url"])
                        self.window.FindElement('Info-2').Update(values= [('Author:  ' + info[x]["author"]), ('View:     ' + str(info[x]["view"])), ('Rating:   ' + str(info[x]["rating"])), ('Note:     ' + info[x]["note"])])
            elif event == 'About':
                about= """
About

Welcome to PyKeep, an open source Python app that organize your Youtube Video Collection!

Simply input the video url and wait for a few seconds. The information will automatically be uploaded to data.json database, and you can access your record anytime you want!
"""
                sg.popup_scrolled(about, size=(50, 30), title='About')
                
# Excute window
pykeep = app()
pykeep.readWindow()











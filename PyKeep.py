'''
PyKeep, version 1.0

Keep your favourite Youtube videos in one app!

(C) MengZe 2020-present
'''

# Copyright information.
__author__ = 'MengZe'
__copyright__ = '(C) MengZe 2020-present'
__license__ = 'Public Domain'
__version__ = '1.0.0'
from pytube import YouTube
import json
import os
import webbrowser
import PySimpleGUI as sg

# Create data.json
json_format = {
    "video":[]
}

open('data.json', 'a').close()
open('data.txt', 'a').close()


with open('data.json', 'r+') as json_database:
    try:
        json.load(json_database)
    except:
        json.dump(json_format, json_database, indent=4)

# Get video information and show on GUI
class videoInfo:
    global yt
    def __init__(self, url):
        self.url = url
        try:
            self.yt = YouTube(url)
        except:
            sg.popup_annoying("Error", "Invalide URL")

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


with open('data.json') as json_database: 
    data = json.load(json_database) 
info = data['video']


# The actual app, designed with PySimpleGUI
class app:
    def __init__(self):
        self.info = info
        self.layout()
        global title

        # Display all exsiting data
        title = []
        for i in range(0, len(info)):
            title.append(info[i]['title'])
            i += 1

    def layout(self):
        self.menu = [['Search', ['YouTube', '---', 'Exit']],
                    ['Theme', ['Light', 'Dark']],
                    ['Help', 'About'],]


        self.windowLayout = [[sg.Menu(self.menu)],
            [sg.Text('Welcome to PyKeep', size=(40, 1), justification='center', font=("Helvetica", 25))],
            [sg.Text('URL'), sg.Input(key='-URL-', do_not_clear=False, size=(80, 1))],
            [sg.Text('Note'), sg.Input(key='-Note-', do_not_clear=False, size=(80, 1)), sg.Submit('Keep')],
            [sg.Listbox(values=[], size=(100, 8), enable_events=True, key='-Title-', pad=(5,10))],
            [sg.Button('Play Video', key='-Browser-'), sg.Button('Delete')],
            [sg.Multiline("URL: ", size=(100, 1), key='Info-1', pad=(5,10), right_click_menu= ['&Right', ['Copy']])],
            [sg.Listbox(values=["Author: ", "View: ", "Rating: ", "Note: "], size=(100, 8), key='Info-2', pad=(5,0))],
            [sg.Button('Download Video', key='-Video-'), sg.Button('Download Audio', key='-Audio-')]]


    # Add video information to data.json
    def addInformation(self):
        getVideoInfo = videoInfo(self.userInput)
        videoTitle = getVideoInfo.getTitle()
        videoAuthor = getVideoInfo.getAuthor()
        videoView = getVideoInfo.getViews()
        videoRating = getVideoInfo.getRating()  
        # python object to be appended 
        if videoTitle:
            json_info = {
                "url": self.userInput,
                "title": videoTitle,
                "author": videoAuthor,
                "view": videoView,
                "rating": videoRating,
                "note": self.note
            }
            
            with open('data.txt', 'a') as txt_database:
                txt_database.write(self.userInput + "\n")

            self.info.append(json_info)
            with open('data.json','w') as json_database: 
                json.dump(data, json_database, indent=4)

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

        with open('data.json', 'w') as json_database:
            json.dump(data, json_database, indent=4)

    # When the user click 'Keep', write the data to json and update the app with new data
    def recordInfo(self):
        self.userInput = values['-URL-']
        self.note = values['-Note-']
        self.addInformation()
        self.window.FindElement('-Title-').Update(values=title)
    
    # Run the window 
    def readWindow(self):
        self.window = sg.Window("PyKeep", self.windowLayout, size=(700, 500), finalize=True)
        self.window.FindElement('-Title-').Update(values=title)
        while True:
            global values
            global event
            event, values = self.window.Read()
            if event in (None, 'Exit'):
                break
            elif event == 'YouTube':
                webbrowser.open('https://www.youtube.com/')
            elif event == 'Keep':
                self.recordInfo()
            elif event == 'Delete':
                sg.popup_annoying("Delete", "You have successfully deleted this item")
                self.deleteInformation()
            elif event == '-Browser-':
                print('Open browser')
                try:
                    webbrowser.open(values['Info-1'])
                except:
                    sg.popup_annoying('Error', 'No video is selected')

            elif event == '-Title-':
                for x in range(0,len(info)):
                    if str(('["' + info[x]['title'] + '"]')) == str(values['-Title-']) or str(("['" + info[x]['title'] + "']")) == str(values['-Title-']):
                        url = info[x]["url"]
                        self.window.FindElement('Info-1').Update(url)
                        self.window.FindElement('Info-2').Update(values= [('Author:  ' + info[x]["author"]), ('View:     ' + str(info[x]["view"])), ('Rating:   ' + str(info[x]["rating"])), ('Note:     ' + info[x]["note"])])

            elif event == '-Video-':
                try:
                    sg.popup_scrolled('This feature is not officially done yet','For a better experience, check out: ','https://github.com/jkelol111/tkyoutubedl','Click OK to continue')
                    url = values['Info-1']
                    try:
                        YouTube(url).streams.first().download()
                        sg.popup_annoying('Download Successed')
                    except:
                        sg.popup_annoying('Download Failed')
                except:
                    sg.popup_annoying('Error', 'No video is selected')

            elif event == '-Audio-':
                try:
                    sg.popup_scrolled('This feature is not officially done yet','For a better experience, check out: ','https://github.com/jkelol111/tkyoutubedl','Click OK to continue')
                    url = values['Info-1']
                    YouTube(url).streams.filter(only_audio=True).first().download()
                    sg.popup_annoying('Download Successed')
                except:
                    sg.popup_annoying('Error', 'No video is selected')
                

            elif event == 'About':
                about= """
Welcome to PyKeep, an open source Python app that organize your Youtube Video Collection!

Simply input the video url and wait for a few seconds. The information will automatically be uploaded to data.json database, and you can access your record anytime you want!
"""
                sg.popup_scrolled(about, title='About')
            # print("Event" + event)
            # print(values)                
# Excute window
pykeep = app()
pykeep.readWindow()











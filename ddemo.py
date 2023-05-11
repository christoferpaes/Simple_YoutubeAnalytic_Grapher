
# import all components
# from the tkinter library
from tkinter import *
  
# import filedialog module
from tkinter import filedialog
#matplot for the figure
from matplotlib.figure import Figure
#Tool bar and figurecanvas for tkinkter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#for the file processing 
import pandas as pd
import numpy as np 
#graph functions 
import matplotlib.pyplot as plt
#math
import math
## possible secondary use for a more stylized graph library and possibley easier file processing
import altair as alt
# using as a way to encapsulate objects in python
import pickle
#wait and thread 
import logging
import threading
import time
import tkinter
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors

class fileContents:
  likes = [] 
  comments = []
  views = []
  name = []
  timeRecorded = []
  def _init_(self,likes,comments,views,timeRecorded,name):
    self.likes = likes
    self.comments = comments
    self.views = views
    self.timeRecorded = timeRecorded
    self.name = name

ss = []
parsingValues = []
array = []
name = []
comments = []
likes = [] 
views = []
timeRecorded = []

filename = [] 
fileContet_Obj = fileContents()

youtubeApiKey= "" ## api key from your youtube developer account 
youtube=discovery.build('youtube', 'v3', developerKey=youtubeApiKey) # setting what is returned from the build function to 'youtube' 
## set the "q" parameter dynamically or hard code it, for example q ="CNN", which is the channel you search by. 
snippets = youtube.search().list(part="snippet", type="channel", q="").execute() ## setting a variable to a list of youtube search, set via pass in parameters from 'list()'
channelId = snippets['items'][0]['snippet']['channelId'] # setting the variable channelId to the first records' channelId 
content = youtube.channels().list(id = channelId, part='contentDetails').execute() # return the content details 
uploadId = content['items'][0]['contentDetails']['relatedPlaylists']['uploads']

allVideos = []

# setting the nextPage token to none
nextPage_token = None

res = youtube.playlistItems().list(playlistId = uploadId, maxResults = 50, part='snippet', pageToken = nextPage_token).execute()

while 1:
  res = youtube.playlistItems().list(playlistId = uploadId, maxResults = 50, part='snippet', pageToken = nextPage_token).execute()
  allVideos += res['items']
  nextPage_token = res.get('nextPage_token')## the  next page token is used to check for the next page 
  print(nextPage_token)
  if nextPage_token is None:
    break

video_ids = list(map(lambda x:x['snippet']['resourceId']['videoId'], allVideos))

stats = []

## setting up the  loop for grabbing and appending the statistics part of the youtube JSON 

#
for i in range(0,len(video_ids), 200):
  res = (youtube).videos().list(id=','.join(video_ids[i:i+100]), part='statistics').execute()
  stats += res['items']

## arrays for the youtube data from JSON
title= []
liked = []
viewCount = []
commentCount = []
timeCurrentForEveryVideo = []



for i in range(30):
  i += 1
  title.append((allVideos[i])['snippet']['title'])
  viewCount.append(int((stats[i])['statistics']['viewCount']))
  liked.append(int((stats[i])['statistics']['likeCount']))
  commentCount.append(int((stats[i]) ['statistics']['commentCount']))
  timeCurrentForEveryVideo.append(time.strftime("%H:%M:%S"))
  

data = {'title':title, 'viewCount' :viewCount, 'likes':liked, 'commentcount' : commentCount,'CurrentTime':timeCurrentForEveryVideo} ## this is for appending columns and rows to the table



def rateOfChage(y2,y1,x2,x1):
  rate = (y2 - y1)/ (x2- x1)
  return rate
def converTimeStam(time):
  i = 0
  while i < len(time):
    if time[i] == ':':
      time = time.replace(':',  ' ')
      
    i +=1 
  return time
def convertIntoNumberOfMinutes(time):
  i = 0
  s = 0
  hours= []
  minutes = []
  while s!= 5:
    if time[i] != ' '  and s < 2:
      hours.append(time[i])
      s += 1
    if time[i] != ' '  and s >=3:
      minutes.append(time[i])
      s += 1
    if time[i] == ' ':
      s+=1
    i +=1
    
  hours = ' '.join([str(elem) for elem in hours]) 
  hours = hours.replace(' ','')
  minutes = ' '.join([str(elem) for elem in minutes]) 
  minutes = minutes.replace(' ','')
  minutes = ((int(hours) * 60) + int(minutes))
  return minutes
  #function to convert the time stamp that is a str into minutes
def clear(Event,figure):
  figure.clear()

def bar(x,y):

  figure = Figure(figsize = (5,5),
    dpi = 100)
  plot1 =figure.add_subplot()
  plot1.bar(y,x, color ='red')
  canvas = FigureCanvasTkAgg(figure,master = window)

  canvas.draw()
   # placing the canvas on the Tkinter window
  canvas.get_tk_widget().pack()
  toolbar = NavigationToolbar2Tk(canvas, window)
  toolbar.update()
  canvas.get_tk_widget().pack()

def barH(x,y):

  figure = Figure(figsize = (5,5),
    dpi = 100)
  plot1 =figure.add_subplot()

  plot1.barh(y,x)
  canvas = FigureCanvasTkAgg(figure,master = window)
 
  canvas.draw()
   # placing the canvas on the Tkinter window
  canvas.get_tk_widget().pack()
  toolbar = NavigationToolbar2Tk(canvas, window)
  toolbar.update()
  canvas.get_tk_widget().pack()
  

def scatter(x,y):
  figure = Figure(figsize = (5,5),
    dpi = 100)
  plot1 =figure.add_subplot()

  plot1.scatter(x,y)
  canvas = FigureCanvasTkAgg(figure,master = window)

  canvas.draw()
   # placing the canvas on the Tkinter window
  canvas.get_tk_widget().pack()
  toolbar = NavigationToolbar2Tk(canvas, window)
  toolbar.update()
  
  
def lineGraph(x,y):
  figure = Figure(figsize = (5,5),
    dpi = 100)
  plot1 =figure.add_subplot()

  plot1.plot(x,y)
  canvas = FigureCanvasTkAgg(figure,master = window)
 
  canvas.draw()
   # placing the canvas on the Tkinter window
  canvas.get_tk_widget().pack()
  toolbar = NavigationToolbar2Tk(canvas, window)
  toolbar.update()
  canvas.get_tk_widget().pack()


def on_click(Event):
  ss = typeofGraphChoice.get()
  return ss

def bros():
  button_explore.bind('<ButtonRelease-1>',browseFiles(Event,fileContet_Obj))
def plot(x,y,fileContet_Obj):
  dropDownVarAssX.bind('<ButtonRelease-1>', hell)
  dropDownVarAssY.bind('<ButtonRelease-1>', hell)

  ss = on_click(Event)
  x,y = hell(Event,fileContet_Obj)  

  if ss == 'Bar':
    bar(x,y)
  elif ss == 'Horizontal Bar Graph':
    barH(x,y)
  elif ss == 'line graph':
    lineGraph(x,y)
  elif ss == 'scatter plot':
    scatter(x,y)
def hello(Event):

  plot(views,name,fileContet_Obj)
def hell(Event,fileContet_Obj):
  if xVar.get() == 'Comments':
    x = fileContet_Obj.comments
  if yVar.get() == 'Comments':
    y = fileContet_Obj.comments
  if xVar.get() == 'Views':
    x = fileContet_Obj.views
  if yVar.get() == 'Views':
    y = fileContet_Obj.views
  if xVar.get() == 'Likes':
    x = fileContet_Obj.likes
  if yVar.get() == 'Likes':
    y = fileContet_Obj.likes
  if xVar.get() == "Names":
    x = fileContet_Obj.name
  if yVar.get() == "Names":
    y = fileContet_Obj.name
  return x, y
def clearClear():
  clear_Button.bind('<ButtonRelease-1>', clear(Event,window ))


def browseFiles(Event,fileContet_Obj):
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("CSV files",
                                                        "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
      
    # Change label contents
   
    label_file_explorer.configure(text="File Opened: "+filename)
    parsingValues = pd.read_csv(filename)

    likes = parsingValues.iloc[:,-3 ].values ## should be the likes Count
    fileContet_Obj.likes = likes
    comments = parsingValues.iloc[:,-2 ].values ## should be the comment Count
    fileContet_Obj.comments = comments

    timeRecorded = parsingValues.iloc[:,-1 ].values ## should be the time recorded
    fileContet_Obj.timeRecorded = timeRecorded


    views = parsingValues.iloc[:,-4 ].values ## should be the view Count
    fileContet_Obj.views = views

    name = parsingValues.iloc[:,-5 ].values   ## should be the likes Count

    fileContet_Obj.name = name
    display_Label.configure(text=parsingValues)





    i=0 # variable used to for the while loop
  
    
    return filename, likes, comments, timeRecorded,views,name, fileContet_Obj

    #while i < len(likes):
      #array.append("VIDEO NAME: " + name[i])
      #array.append("timeStamp:" + timeRecorded[i])
      #array.append("CommentCount:"+ str(comments[i])) ## arrays in python for int value must be casted to a string .. so use str() function to cast the int and return a string 
      #array.append("LikeCount:"+ str(likes[i])) ## arrays in python for int value must be casted to a string .. so use str() function to cast the int and return a string 
      #array.append("ViewCount:"+ str(views[i])) ## arrays in python for int value must be casted to a string .. so use str() function to cast the int and return a string 
      #array2.append("timeStamp:" + secondTimeRecorded[i])
      #array2.append("CommentCount:"+ str(secondComments[i])) ## arrays in python for int value must be casted to a string .. so use str() function to cast the int and return a string 
      #array2.append("LikeCount:"+ str(secondLikes[i])) ## arrays in python for int value must be casted to a string .. so use str() function to cast the int and return a string 
      #array2.append("ViewCount:"+ str(secondViews[i])) ## arrays in python for int value must be casted to a string .. so use str() function to cast the int and return a string 
    #  countsCommentsArr.append(comments[i]) 
      # countsCommentsArr.append(secondComments[i])
      #countsCommentsArr.append(thirdComments[i ])
     # timeStampArry.append(timeRecorded[i])
      #timeStampArry.append(secondTimeRecorded[i])
      #timeStampArry.append(thirdTimeRecorded[i ])
     # countsLikesArr.append(likes[i])
      #countsLikesArr.append(secondLikes[i])
      #countsLikesArr.append(thirdLikes[i ])
     # countsViewCountArr.append(views[i])
      #countsViewCountArr.append(secondViews[i])
      #countsViewCountArr.append(thirdViews[i ])
     # print(name)
      
   
   

    # return an object from the file selction ... 


      
      
                                                                                                  
# Create the root window

window = Tk()
  
# Set window title
window.title('CSV to Graph App .... written by: Christofer P. Paes ')

window.iconbitmap('barChart.ico')
# Set window size
window.geometry("500x500")
  
#Set window background color
window.config(background = "white")



# Create a File Explorer label
label_file_explorer = Label(window,
                            text = "Graph display for csv files ",
                            width = 100, height = 4,
                            fg = "blue")

  


clear_Button = Button(window, text = 'Remove the graph',command=clearClear)
display_Label = Label(window,text=parsingValues, width=100, height = 5, fg = "red")
##select drop down
var =[]
typeofGraphChoice = StringVar()
typeofGraphChoice.set("Select a type of graph")
xVar = StringVar()
yVar = StringVar()
xVar.set("Set the variable for X")
yVar.set("Set the variable for Y")
drop = OptionMenu(window,typeofGraphChoice,"Bar","Horizontal Bar Graph", "line graph", "scatter plot")
dropDownVarAssX = OptionMenu(window,xVar, "Names", "Comments", "Views", "Likes" )
dropDownVarAssY = OptionMenu(window,yVar, "Names", "Comments", "Views", "Likes" )
typeofGraphChoice.trace_add('write', lambda *args:  typeofGraphChoice.get())



button_explore = Button(window,
                        text = "Browse Files", state = NORMAL,command = bros)
button_exit = Button(window,
                     text = "Exit",
                     command = exit)


button_plot = Button(window, text = 'Plot')


#setting the widgets to their positions via a column and row arg
label_file_explorer.pack()
  
button_explore.pack()
drop.pack()
button_plot.pack()
button_exit.pack()
display_Label.pack()
dropDownVarAssY.pack()
dropDownVarAssX.pack()
clear_Button.pack()

 ## separate into arrays for each column in the table 
 

views = fileContet_Obj.views
views = views[:5]
likes = fileContet_Obj.likes
likes = likes[:5]

comments = fileContet_Obj.comments
comments = comments[:5]
name  = fileContet_Obj.name
name = name[:5]

pickeled_object = pickle.dumps(fileContet_Obj)

  
# Let the window wait for any events

#binding the widgets to an event
drop.bind('<ButtonRelease-1>', on_click)
#button_explore.bind('<Button-1>',browseFiles)

#if checkerChecker12  == 'changeState':


button_plot.bind('<Button-1>', hello)
window.mainloop()

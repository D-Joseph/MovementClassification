import tkinter as tk
import liveReader
import pandas as pd

#define global window
global window
window = tk.Tk()

#define global file path
global in_file_path
in_file_path = ''

#define model results
global result_label

#update label text to show the prediction in real time
def updateLabel():
    print("label start")
    global result_label

    #make predictions
    liveReader.liveRead() # get data and make prediction
    print("label done read")

    prediction = liveReader.prediction

    #update label text to show prediction
    result_label.config(text='Prediction: ' + prediction)
    result_label.pack()

    window.after(5000, updateLabel)

def updateLoop():
    print("loop")
    updateLabel()
    print("done loop")

#create instructions and prediction label
intro = tk.Label(text="Real-time prediction of walking or jumping", font=('Helvetica', 16))
intro.pack()

#create label to display prediction
result_label = tk.Label(text='Prediction: ', font=('Helvetica', 16))
result_label.pack()
print("gui here")

liveReader.liveInitialize()

print("reader initialized")

updateLoop()

#create window
window.geometry('1000x800+1000+700')
window.mainloop()

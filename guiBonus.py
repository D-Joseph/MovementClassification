import tkinter as tk
import liveReader

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
    global result_label

    #make predictions
    liveReader.liveRead() # get data and make prediction
    prediction = liveReader.prediction

    #update label text to show prediction
    result_label.config(text='Prediction: ' + prediction)

    #schedule next update after 5 seconds
    window.after(5000, updateLabel)

#create instructions and prediction label
intro = tk.Label(text="Real-time prediction of walking or jumping", font=('Helvetica', 16))
intro.pack()

#create label to display prediction
result_label = tk.Label(text='Prediction: ', font=('Helvetica', 16))
result_label.pack()

#create window
window.geometry('1000x800+1000+700')
window.after(5000, updateLabel) # call updateLabel function after 5 seconds
window.mainloop()
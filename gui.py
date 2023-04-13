import tkinter as tk
from tkinter import ttk, filedialog
import inputData
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#define global window
global window
window = tk.Tk()

#define canvas for plot
global canvas
canvas = FigureCanvasTkAgg(None, master=window)

#define global file path
global in_file_path
in_file_path = ''

#define model results
global result

#save CSV file with 'Walking' or 'Running' label at location selected
def saveFile():
    files = [('CSV file', '*.csv')]
    file_path = filedialog.asksaveasfile(filetypes=files, defaultextension='.csv')
    result[1].to_csv(file_path.name, index = False)

#define global save instructions
global save_dialog
save_button = tk.Button(window, text='Save', command=saveFile)
save_dialog = tk.Label(text="\nPredictions made, select location to save output file", font=('Helvetica', 16))

#plot absolute acceleration vs time along with predictions vs time for input file
#includ plot in GUI
def plotResult():
    global result
    global window
    global canvas

    canvas.get_tk_widget().destroy()    #remove previous plots from canvas
    result_copy = result[1].copy()      #create copy of results for use in plotting
    fig, ax1 = plt.subplots()

    #plot absolute acceleration vs time
    ax1.plot(result_copy['Time (s)'], result_copy['Absolute acceleration (m/s^2)'],
             label='Absolute Acceleration', color='red', zorder=1)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Absolute Acceleration (m/s^2)', color = 'red')

    #plot prediction vs time
    ax2 = ax1.twinx()
    ax2.set_ylabel('Walking or Running', color='blue')
    ax2.yaxis.set_label_coords(1.05, 0.5)
    ax2.plot(result_copy['Time (s)'], result_copy['Label'], label='Walking or Running', color='blue', zorder=2)


    #add title
    plt.title('Absolute Acceleration versus Time')

    #add plot to window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

#print overall prediction and call plotResult() when Predict button pressed
def processResults():
    global result
    global save_dialog

    #remove previous predict dialogs and save button
    save_dialog.pack_forget()
    save_button.pack_forget()

    #make predictions
    file = pd.read_csv(in_file_path)
    result = inputData.proc(file)

    #show overall prediction
    save_dialog = tk.Label(text="\nPrediction " + result[0], font=('Helvetica', 16))

    #get plot
    plotResult()

    #include save instructions and options
    save_dialog.pack()
    save_button.pack()

#create instructions and buttons for post Browse button
predict_button = tk.Button(window, text='Predict', command=processResults)
predict_dialog = tk.Label(text="\nInput file uploaded", font=('Helvetica', 16))

#Get input CSV file when Browse is pressed
def searchFile():
    global in_file_path
    global canvas
    global save_dialog

    #get csv input file path
    in_file_path = filedialog.askopenfilename(
        initialdir='/',
        title='Select a CSV file',
        filetypes=(('CSV files', '*.csv'),)
    )

    #if file found, get rid of all previous dialogs and add predict button and dialog
    if in_file_path != '':
        predict_button.pack_forget()
        canvas.get_tk_widget().destroy()
        save_dialog.pack_forget()
        save_button.pack_forget()

        predict_dialog.pack()
        predict_button.pack()


#display input instructions
intro = tk.Label(text="Upload CSV file to determine if user is running or walking", font=('Helvetica', 16))
intro.pack()

#display search button
search_button = tk.Button(window, text='Browse', command=searchFile)
search_button.pack()

#create window
window.geometry('1000x800+1000+700')
intro.pack(pady=20)
window.mainloop()
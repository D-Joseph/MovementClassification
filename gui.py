import tkinter as tk
from tkinter import ttk, filedialog
import os
import inputData

window = tk.Tk()
def saveFile():
    files = [('CSV file', '*.csv')]
    file_path = filedialog.asksaveasfile(filetypes=files, defaultextension='.csv')

    print(file_path.name)

save_button = tk.Button(window, text='Save', command=saveFile)
save_dialog = tk.Label(text="\nPredictions made, select location to save output file", font=('Helvetica', 16))


def processResults():
    save_dialog.pack()
    save_button.pack()
predict_button = tk.Button(window, text='Predict', command=processResults)
predict_dialog = tk.Label(text="\nInput file uploaded", font=('Helvetica', 16))

def searchFile():
    file_path = filedialog.askopenfilename(
        initialdir='/',
        title='Select a CSV file',
        filetypes=(('CSV files', '*.csv'),)
    )
    if file_path != '':
        predict_button.pack_forget()
        save_dialog.pack_forget()
        save_button.pack_forget()

        predict_dialog.pack()
        predict_button.pack()

intro = tk.Label(text="Upload CSV file to determine if user is running or walking", font=('Helvetica', 16))
intro.pack()

search_button = tk.Button(window, text='Browse', command=searchFile)
search_button.pack()


window.geometry('500x300+500+200')


intro.pack(pady=20)



window.mainloop()

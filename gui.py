import tkinter as tk
from tkinter import ttk, filedialog

def saveFile():
    files = [('CSV file', '*.csv')]
    file_path = filedialog.asksaveasfile(filetypes=files, defaultextension='.csv')
    print(file_path)

def searchFile():
    file_path = filedialog.askopenfilename(
        initialdir='/',
        title='Select a CSV file',
        filetypes=(('CSV files', '*.csv'),)
    )
    save_dialog = tk.Label(text="\nInput file uploaded, select location to save output file", font=('Helvetica', 16))
    save_dialog.pack()
    save_button = tk.Button(window, text='save', command=saveFile)
    save_button.pack()

window = tk.Tk()

intro = tk.Label(text="Upload CSV file to determine if user is running or walking", font=('Helvetica', 16))
intro.pack()

search_button = tk.Button(window, text='Browse', command=searchFile)
search_button.pack()


window.geometry('500x300+500+200')


intro.pack(pady=20)



window.mainloop()
import tkinter as tk
from tkinter import ttk, font, colorchooser, filedialog, messagebox
import os
import speech_recognition as sr

main_application = tk.Tk()
main_application.geometry('1200x800')
main_application.title('Vpad text editor')
main_application.wm_iconbitmap('icon.ico')

############################################## Main Menu ###################################################

main_menu = tk.Menu()

# File icons
new_icon = tk.PhotoImage(file='icons2/new.png')
open_icon = tk.PhotoImage(file='icons2/open.png')
save_icon = tk.PhotoImage(file='icons2/save.png')
save_as_icon = tk.PhotoImage(file='icons2/save_as.png')
exit_icon = tk.PhotoImage(file='icons2/exit.png')

file = tk.Menu(main_menu, tearoff=False)

# Edit icons
copy_icon = tk.PhotoImage(file='icons2/copy.png')
paste_icon = tk.PhotoImage(file='icons2/paste.png')
cut_icon = tk.PhotoImage(file='icons2/cut.png')
clear_all_icon = tk.PhotoImage(file='icons2/clear_all.png')
find_icon = tk.PhotoImage(file='icons2/find.png')

edit = tk.Menu(main_menu, tearoff=False)

# View icons
tool_bar_icon = tk.PhotoImage(file='icons2/tool_bar.png')
status_bar_icon = tk.PhotoImage(file='icons2/status_bar.png')
view = tk.Menu(main_menu, tearoff=False)

# Color theme
light_default_icon = tk.PhotoImage(file='icons2/light_default.png')
light_plus_icon = tk.PhotoImage(file='icons2/light_plus.png')
dark_icon = tk.PhotoImage(file='icons2/dark.png')
red_icon = tk.PhotoImage(file='icons2/red.png')
monokai_icon = tk.PhotoImage(file='icons2/monokai.png')
night_blue_icon = tk.PhotoImage(file='icons2/night_blue.png')
color_theme = tk.Menu(main_menu, tearoff=False)

theme_choice = tk.StringVar()
color_icons = (light_default_icon, light_plus_icon, dark_icon, red_icon, monokai_icon, night_blue_icon)

color_dict = {
    'Light Default ': ('#000000', '#ffffff'),
    'Light Plus': ('#474747', '#e0e0e0'),
    'Dark': ('#c4c4c4', '#2d2d2d'),
    'Red': ('#2d2d2d', '#ffe8e8'),
    'Monokai': ('#d3b774', '#474747'),
    'Night Blue': ('#ededed', '#6b9dc2')
}

# Cascade
main_menu.add_cascade(label='File', menu=file)
main_menu.add_cascade(label='Edit', menu=edit)
main_menu.add_cascade(label='View', menu=view)
main_menu.add_cascade(label='Color Theme', menu=color_theme)

############################################## Toolbar ###################################################

tool_bar = ttk.Label(main_application)
tool_bar.pack(side=tk.TOP, fill=tk.X)

# Font box
font_tuple = tk.font.families()
font_family = tk.StringVar()
font_box = ttk.Combobox(tool_bar, width=30, textvariable=font_family, state='readonly')
font_box['values'] = font_tuple
font_box.current(font_tuple.index('Arial'))
font_box.grid(row=0, column=0, padx=5)

# Size box
size_var = tk.IntVar()
font_size = ttk.Combobox(tool_bar, width=14, textvariable=size_var, state='readonly')
font_size['values'] = tuple(range(8, 81))
font_size.current(4)
font_size.grid(row=0, column=1, padx=5)

# Bold button
bold_icon = tk.PhotoImage(file='icons2/bold.png').subsample(2, 2)  
bold_btn = ttk.Button(tool_bar, image=bold_icon , cursor="hand")
bold_btn.grid(row=0, column=2, padx=5)

# Italic button
italic_icon = tk.PhotoImage(file='icons2/italic.png').subsample(2, 2)
italic_btn = ttk.Button(tool_bar, image=italic_icon , cursor="hand")
italic_btn.grid(row=0, column=3, padx=5)

# Underline button
underline_icon = tk.PhotoImage(file='icons2/underline.png').subsample(2, 2)
underline_btn = ttk.Button(tool_bar, image=underline_icon , cursor="hand")
underline_btn.grid(row=0, column=4, padx=5)

# Font color button
font_color_icon = tk.PhotoImage(file='icons2/font_color.png').subsample(2, 2)
font_color_btn = ttk.Button(tool_bar, image=font_color_icon , cursor="hand")
font_color_btn.grid(row=0, column=5, padx=5)

# Align left button
align_left_icon = tk.PhotoImage(file='icons2/align_left.png').subsample(2, 2)
align_left_btn = ttk.Button(tool_bar, image=align_left_icon , cursor="hand")
align_left_btn.grid(row=0, column=6, padx=5)

# Align center button
align_center_icon = tk.PhotoImage(file='icons2/align_center.png').subsample(2, 2)
align_center_btn = ttk.Button(tool_bar, image=align_center_icon , cursor="hand")
align_center_btn.grid(row=0, column=7, padx=5)

# Align right button
align_right_icon = tk.PhotoImage(file='icons2/align_right.png').subsample(2, 2)
align_right_btn = ttk.Button(tool_bar, image=align_right_icon , cursor="hand")
align_right_btn.grid(row=0, column=8, padx=5)

# Bold italic button
bold_italic_icon = tk.PhotoImage(file='icons2/bold_italic.png').subsample(2, 2)
bold_italic_btn = ttk.Button(tool_bar, image=bold_italic_icon , cursor="hand")
bold_italic_btn.grid(row=0, column=9, padx=5)

# Speech to text button
speech_to_text_icon = tk.PhotoImage(file='icons2/microphone.png').subsample(2, 2)
speech_to_text_btn = ttk.Button(tool_bar, image=speech_to_text_icon , cursor="hand")
speech_to_text_btn.grid(row=0, column=10, padx=5)

# -------------------------------------&&&&&&&& End Toolbar &&&&&&&&&&& ----------------------------------

############################################## Text Editor ###################################################

text_editor = tk.Text(main_application)
text_editor.config(wrap='word', relief=tk.FLAT)

scroll_bar = tk.Scrollbar(main_application)
text_editor.focus_set()
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
text_editor.pack(fill=tk.BOTH, expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

# Font family and font size functionality
current_font_family = 'Arial'
current_font_size = 25

def change_font(event=None):
    global current_font_family
    current_font_family = font_family.get()
    text_editor.configure(font=(current_font_family, current_font_size))

def change_fontsize(event=None):
    global current_font_size
    current_font_size = size_var.get()
    text_editor.configure(font=(current_font_family, current_font_size))

font_box.bind("<<ComboboxSelected>>", change_font)
font_size.bind("<<ComboboxSelected>>", change_fontsize)

# Bold button functionality
def toggle_bold(event=None):
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['weight'] == 'normal':
        text_editor.tag_add('bold', 'sel.first', 'sel.last')
        text_editor.tag_configure('bold', font=(current_font_family, current_font_size, 'bold'))
    elif text_property.actual()['weight'] == 'bold':
        text_editor.tag_remove('bold', 'sel.first', 'sel.last')
        text_editor.tag_configure('bold', font=(current_font_family, current_font_size, 'normal'))

bold_btn.configure(command=toggle_bold)


# Italic button functionality
def toggle_italic(event=None):
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['slant'] == 'roman':
        text_editor.tag_add('italic', 'sel.first', 'sel.last')
        text_editor.tag_configure('italic', font=(current_font_family, current_font_size, 'italic'))
    elif text_property.actual()['slant'] == 'italic':
        text_editor.tag_remove('italic', 'sel.first', 'sel.last')
        text_editor.tag_configure('italic', font=(current_font_family, current_font_size, 'roman'))

italic_btn.configure(command=toggle_italic)

# Underline button functionality
def toggle_underline(event=None):
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['underline'] == 0:
        text_editor.tag_add('underline', 'sel.first', 'sel.last')
        text_editor.tag_configure('underline', underline=True)
    elif text_property.actual()['underline'] == 1:
        text_editor.tag_remove('underline', 'sel.first', 'sel.last')
        text_editor.tag_configure('underline', underline=False)

underline_btn.configure(command=toggle_underline)

# Font color button functionality
def change_font_color(event=None):
    color_var = tk.colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])

font_color_btn.configure(command=change_font_color)

# Align left button functionality
def align_left(event=None):
    text_editor.tag_configure('center', justify=tk.CENTER)
    text_editor.tag_configure('right', justify=tk.RIGHT)
    text_editor.tag_remove('center', 'sel.first', 'sel.last')
    text_editor.tag_remove('right', 'sel.first', 'sel.last')
    text_editor.tag_configure('left', justify=tk.LEFT)
    text_editor.tag_add('left', 'sel.first', 'sel.last')

align_left_btn.configure(command=align_left)

# Align center button functionality
def align_center(event=None):
    text_editor.tag_configure('left', justify=tk.LEFT)
    text_editor.tag_configure('right', justify=tk.RIGHT)
    text_editor.tag_remove('left', 'sel.first', 'sel.last')
    text_editor.tag_remove('right', 'sel.first', 'sel.last')
    text_editor.tag_configure('center', justify=tk.CENTER)
    text_editor.tag_add('center', 'sel.first', 'sel.last')

align_center_btn.configure(command=align_center)

# Align right button functionality
def align_right(event=None):
    text_editor.tag_configure('left', justify=tk.LEFT)
    text_editor.tag_configure('center', justify=tk.CENTER)
    text_editor.tag_remove('left', 'sel.first', 'sel.last')
    text_editor.tag_remove('center', 'sel.first', 'sel.last')
    text_editor.tag_configure('right', justify=tk.RIGHT)
    text_editor.tag_add('right', 'sel.first', 'sel.last')

align_right_btn.configure(command=align_right)

# Bold italic button functionality
def toggle_bold_italic(event=None):
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['weight'] == 'normal' and text_property.actual()['slant'] == 'roman':
        text_editor.tag_add('bold_italic', 'sel.first', 'sel.last')
        text_editor.tag_configure('bold_italic', font=(current_font_family, current_font_size, 'bold italic'))
    else:
        text_editor.tag_remove('bold_italic', 'sel.first', 'sel.last')
        text_editor.tag_configure('bold_italic', font=(current_font_family, current_font_size, 'normal'))

# Bold and italic buttons
bold_btn.configure(command=toggle_bold_italic)
italic_btn.configure(command=toggle_bold_italic)

#bold and italic buttons separated 
# Bold button functionality
def toggle_bold(event=None):
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['weight'] == 'normal':
        text_editor.tag_add('bold', 'sel.first', 'sel.last')
        text_editor.tag_configure('bold', font=(current_font_family, current_font_size, 'bold'))
    elif text_property.actual()['weight'] == 'bold':
        text_editor.tag_remove('bold', 'sel.first', 'sel.last')
        text_editor.tag_configure('bold', font=(current_font_family, current_font_size, 'normal'))

bold_btn.configure(command=toggle_bold)

# Italic button functionality
def toggle_italic(event=None):
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['slant'] == 'roman':
        text_editor.tag_add('italic', 'sel.first', 'sel.last')
        text_editor.tag_configure('italic', font=(current_font_family, current_font_size, 'italic'))
    elif text_property.actual()['slant'] == 'italic':
        text_editor.tag_remove('italic', 'sel.first', 'sel.last')
        text_editor.tag_configure('italic', font=(current_font_family, current_font_size, 'roman'))

italic_btn.configure(command=toggle_italic)

# Bold italic button functionality
def toggle_bold_italic(event=None):
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['weight'] == 'normal' and text_property.actual()['slant'] == 'roman':
        text_editor.tag_add('bold_italic', 'sel.first', 'sel.last')
        text_editor.tag_configure('bold_italic', font=(current_font_family, current_font_size, 'bold italic'))
    else:
        text_editor.tag_remove('bold_italic', 'sel.first', 'sel.last')
        text_editor.tag_configure('bold_italic', font=(current_font_family, current_font_size, 'normal'))

bold_italic_btn.configure(command=toggle_bold_italic)

# Speech to text functionality

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)  # Set a timeout to stop listening after 5 seconds of silence
            print("Stopped listening...")
            recognized_text = recognizer.recognize_google(audio)
            text_editor.insert(tk.END, recognized_text)
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period")
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


speech_to_text_btn.configure(command=speech_to_text)

# -------------------------------------&&&&&&&& End Text Editor &&&&&&&&&&& ----------------------------------

############################################## Status Bar ###################################################

status_bar = ttk.Label(main_application, text='Status Bar')
status_bar.pack(side=tk.BOTTOM)

text_changed = False

def update_status_bar(event=None):
    global text_changed
    if text_editor.edit_modified():
        text_changed = True
        words = len(text_editor.get(1.0, 'end-1c').split())
        characters = len(text_editor.get(1.0, 'end-1c'))
        status_bar.config(text=f'Characters: {characters} Words: {words}')
    text_editor.edit_modified(False)

text_editor.bind('<<Modified>>', update_status_bar)

# -------------------------------------&&&&&&&& End Status Bar &&&&&&&&&&& ----------------------------------

############################################## Main Menu Functionality ###################################################

# New file functionality
def new_file(event=None):
    global url
    url = ''
    text_editor.delete(1.0, tk.END)

file.add_command(label='New', image=new_icon, compound=tk.LEFT, accelerator='Ctrl+N', command=new_file)

# Open file functionality
def open_file(event=None):
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
    try:
        with open(url, 'r') as fr:
            text_editor.delete(1.0, tk.END)
            text_editor.insert(1.0, fr.read())
    except FileNotFoundError:
        return
    except:
        return
    main_application.title(os.path.basename(url))

file.add_command(label='Open', image=open_icon, compound=tk.LEFT, accelerator='Ctrl+O', command=open_file)

# Save file functionality
def save_file(event=None):
    global url
    try:
        if url:
            content = str(text_editor.get(1.0, tk.END))
            with open(url, 'w', encoding='utf-8') as fw:
                fw.write(content)
        else:
            url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
            content2 = text_editor.get(1.0, tk.END)
            url.write(content2)
            url.close()
    except:
        return

file.add_command(label='Save', image=save_icon, compound=tk.LEFT, accelerator='Ctrl+S', command=save_file)

# Save as functionality
def save_as(event=None):
    global url
    try:
        content = text_editor.get(1.0, tk.END)
        url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
        url.write(content)
        url.close()
    except:
        return

file.add_command(label='Save As', image=new_icon, compound=tk.LEFT, accelerator='Ctrl+Alt+S', command=save_as)

# Exit functionality
def exit_func(event=None):
    global url, text_changed
    try:
        if text_changed:
            mbox = messagebox.askyesnocancel('Warning', 'Do you want to save the file?')
            if mbox is True:
                if url:
                    content = text_editor.get(1.0, tk.END)
                    with open(url, 'w', encoding='utf-8') as fw:
                        fw.write(content)
                    main_application.destroy()
                else:
                    content2 = str(text_editor.get(1.0, tk.END))
                    url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
                    url.write(content2)
                    url.close()
                    main_application.destroy()
            elif mbox is False:
                main_application.destroy()
        else:
            main_application.destroy()
    except:
        return

file.add_command(label='Exit', image=exit_icon, compound=tk.LEFT, accelerator='Ctrl+Q', command=exit_func)

# -------------------------------------&&&&&&&& End Main Menu Functionality &&&&&&&&&&& ----------------------------------

############################################## Bindings ###################################################

main_application.config(menu=main_menu)

############################################## Main Loop ###################################################

main_application.mainloop()

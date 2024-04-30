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

# Button icons
button_icons = {
    'bold': tk.PhotoImage(file='icons2/bold.png'),
    'italic': tk.PhotoImage(file='icons2/italic.png'),
    'underline': tk.PhotoImage(file='icons2/underline.png'),
    'font_color': tk.PhotoImage(file='icons2/font_color.png'),
    'align_left': tk.PhotoImage(file='icons2/align_left.png'),
    'align_center': tk.PhotoImage(file='icons2/align_center.png'),
    'align_right': tk.PhotoImage(file='icons2/align_right.png'),
    'bold_italic': tk.PhotoImage(file='icons2/bold_italic.png'),
    'speech_to_text': tk.PhotoImage(file='icons2/microphone.png')
}

# Button names and corresponding toggle functions
button_toggle_functions = {
    'bold': 'toggle_bold',
    'italic': 'toggle_italic',
    'underline': 'toggle_underline',
    'font_color': 'change_font_color',
    'align_left': 'align_left',
    'align_center': 'align_center',
    'align_right': 'align_right',
    'bold_italic': 'toggle_bold_italic',
    'speech_to_text': 'speech_to_text'
}

# Create and configure buttons
buttons = {}
for i, (name, icon) in enumerate(button_icons.items()):
    btn = ttk.Button(tool_bar, image=icon)
    btn.grid(row=0, column=i + 2, padx=5)
    buttons[name] = btn

# Toggle function
def toggle(event=None, tag=None, font=None):
    if tag:
        text_editor.tag_add(tag, 'sel.first', 'sel.last')
        text_editor.tag_configure(tag, font=font)
    else:
        text_editor.tag_remove(tag, 'sel.first', 'sel.last')
        text_editor.tag_configure(tag, font=font)

# Configure buttons with toggle functionality
for name, btn in buttons.items():
    toggle_func = button_toggle_functions[name]
    if toggle_func in globals():
        btn.configure(command=lambda event=None, toggle_func=toggle_func, name=name: globals()[toggle_func](event, name))

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
current_font_size = 12

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
def toggle_bold(event=None, name=None):
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['weight'] == 'normal':
        toggle(tag='bold', font=(current_font_family, current_font_size, 'bold'))
    elif text_property.actual()['weight'] == 'bold':
        toggle(tag='bold', font=(current_font_family, current_font_size, 'normal'))

# Italic button functionality
def toggle_italic(event=None, name=None):
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['slant'] == 'roman':
        toggle(tag='italic', font=(current_font_family, current_font_size, 'italic'))
    elif text_property.actual()['slant'] == 'italic':
        toggle(tag='italic', font=(current_font_family, current_font_size, 'roman'))

# Underline button functionality
def toggle_underline(event=None, name=None):
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['underline'] == 0:
        toggle(tag='underline', font=(current_font_family, current_font_size, 'normal'))
    elif text_property.actual()['underline'] == 1:
        toggle(tag='underline', font=(current_font_family, current_font_size, 'underline'))

# Font color button functionality
def change_font_color(event=None, name=None):
    color_var = tk.colorchooser.askcolor()
    if color_var:
        text_editor.configure(fg=color_var[1])

# Align left button functionality
def align_left(event=None, name=None):
    text_editor.tag_configure('center', justify=tk.CENTER)
    text_editor.tag_configure('right', justify=tk.RIGHT)
    text_editor.tag_remove('center', 'sel.first', 'sel.last')
    text_editor.tag_remove('right', 'sel.first', 'sel.last')
    text_editor.tag_configure('left', justify=tk.LEFT)
    text_editor.tag_add('left', 'sel.first', 'sel.last')

# Align center button functionality
def align_center(event=None, name=None):
    text_editor.tag_configure('left', justify=tk.LEFT)
    text_editor.tag_configure('right', justify=tk.RIGHT)
    text_editor.tag_remove('left', 'sel.first', 'sel.last')
    text_editor.tag_remove('right', 'sel.first', 'sel.last')
    text_editor.tag_configure('center', justify=tk.CENTER)
    text_editor.tag_add('center', 'sel.first', 'sel.last')

# Align right button functionality
def align_right(event=None, name=None):
    text_editor.tag_configure('left', justify=tk.LEFT)
    text_editor.tag_configure('center', justify=tk.CENTER)
    text_editor.tag_remove('left', 'sel.first', 'sel.last')
    text_editor.tag_remove('center', 'sel.first', 'sel.last')
    text_editor.tag_configure('right', justify=tk.RIGHT)
    text_editor.tag_add('right', 'sel.first', 'sel.last')

# Bold italic button functionality
def toggle_bold_italic(event=None, name=None):
    text_property = tk.font.Font(font=text_editor['font'])
    if text_property.actual()['weight'] == 'normal' and text_property.actual()['slant'] == 'roman':
        toggle(tag='bold_italic', font=(current_font_family, current_font_size, 'bold italic'))
    else:
        toggle(tag='bold_italic', font=(current_font_family, current_font_size, 'normal'))

# Speech to text functionality
def speech_to_text(event=None, name=None):
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

# Bind buttons to their corresponding functionality
buttons['bold'].configure(command=lambda event=None, name='bold': toggle_bold(event, name))
buttons['italic'].configure(command=lambda event=None, name='italic': toggle_italic(event, name))
buttons['underline'].configure(command=lambda event=None, name='underline': toggle_underline(event, name))
buttons['font_color'].configure(command=lambda event=None, name='font_color': change_font_color(event, name))
buttons['align_left'].configure(command=lambda event=None, name='align_left': align_left(event, name))
buttons['align_center'].configure(command=lambda event=None, name='align_center': align_center(event, name))
buttons['align_right'].configure(command=lambda event=None, name='align_right': align_right(event, name))
buttons['bold_italic'].configure(command=lambda event=None, name='bold_italic': toggle_bold_italic(event, name))
buttons['speech_to_text'].configure(command=lambda event=None, name='speech_to_text': speech_to_text(event, name))

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

############################################## Bindings ###################################################

main_application.config(menu=main_menu)

############################################## Main Loop ###################################################

main_application.mainloop()

import tkinter as tk

def make_bold_italic(text_widget, start, end):
    text_widget.tag_add("bold_italic", start, end)
    text_widget.tag_config("bold_italic", font=("Helvetica", 12, "bold italic"))

root = tk.Tk()

text_widget = tk.Text(root)
text_widget.pack()

text_widget.insert("end", "")
end_index = text_widget.index("end-1c")
print(end_index)
# make_bold_italic(text_widget, "1.0")  # Apply bold italic style to the word "This"

root.mainloop()

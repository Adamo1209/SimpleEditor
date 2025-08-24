# __main__.py

import tkinter as tk

import utility

main_win_title = "Simple Editor"
main_win_initial_size = (600,600)
ui_font = ("Maple Mono NF CN",11)
edit_zone_font = ("Maple Mono NF CN",11)

root = tk.Tk()
root.title(main_win_title)
utility.set_window_center(root,size=main_win_initial_size)

def main():
    edit_zone = tk.Text(font=edit_zone_font)
    file = utility.FileProcesser(edit_zone)
    clipboard = utility.Clipboard(edit_zone)
    text = utility.TextProcesser(root=root,w_text=edit_zone)
    edit_zone.config(undo=True)
    edit_zone.pack(side="top",fill="both",expand=True)

    menu_bar = tk.Menu(root,background="white",tearoff=False)

    menu_file = tk.Menu(menu_bar,background="white",font=ui_font,tearoff=False)
    menu_file.add_command(label="new",command=file.create_new)
    menu_file.add_command(label="open",command=file.open_file)
    menu_file.add_command(label="save",command=file.save_file)
    menu_file.add_command(label="save as",command=file.save_as_file)

    menu_edit = tk.Menu(menu_bar,background="white",font=ui_font,tearoff=False)
    menu_edit.add_command(label="undo",command=edit_zone.edit_undo)
    menu_edit.add_separator()
    menu_edit.add_command(label="copy",command=clipboard.copy)
    menu_edit.add_command(label="cut",command=clipboard.cut)
    menu_edit.add_command(label="paste",command=clipboard.paste)
    menu_edit.add_separator()
    menu_edit.add_command(label="search",command=text.action_search)
    menu_edit.add_command(label="replace",command=None)
    
    menu_view = tk.Menu(menu_bar,background="white",font=ui_font,tearoff=False)
    menu_view.add_checkbutton(label="word wrap",variable=text.word_wrap_boolvar,command=text.word_wrap)

    menu_bar.add_cascade(label="File",menu=menu_file)
    menu_bar.add_cascade(label="Edit",menu=menu_edit)
    menu_bar.add_cascade(label="View",menu=menu_view)
    menu_bar.add_command(label="About")
    root.config(menu=menu_bar)

    root.mainloop()

if __name__ == "__main__":
    main()
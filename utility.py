# utility.py

from pathlib import Path
import tkinter as tk
import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfdlg
import sys

import widget

def main():
    return None

def set_window_center(master:tk.Tk,*,size:tuple[int,int]=(0,0)) -> None:
    screen_x = master.winfo_screenwidth()
    screen_y = master.winfo_screenheight()
    if all(list(map(lambda x:x>0,size))):
        master.geometry(newGeometry=f"{size[0]}x{size[1]}+{int((screen_x/2)-(size[0]/2))}+{int((screen_y/2)-(size[1]/1.75))}")
        return None
    else:
        win_x = int(master.geometry().split("x")[0])
        win_y = int(master.geometry().split("x")[-1].split("+")[0])
        master.geometry(newGeometry=f"{win_x}x{win_y}+{int((screen_x/2)-(win_x/2))}+{int((screen_y/2)-(win_y/1.75))}")
        return None
    
def resource_direct(relative_path:str) -> Path:
    path:Path = Path(__file__).parent / Path(relative_path)
    if getattr(sys,"frozen",False):
        path = Path(sys._MEIPASS) / path
        return path
    else:
        return path

def about():
    tkmsg.showinfo(title="About SimpleEditor",message="Author: Adamo1209\nVersion: 0.1.0\nBuildTime: 20250908(BJT)")

# setting references
class References:
    # reference vars
    main_win_title = "Simple Editor"
    main_win_initial_size = (600,600)
    ui_font = ("Arial",11)
    edit_zone_font = ("Arial",15)
    top_lable_font = ("Arial",15)

    def setting(self,**kwargs):
        for var,value in kwargs.items():
            self.__dict__[var] = value

    def __init__(self,**kwargs):
        self.setting(self,**kwargs)

class TextProcesser:
    word_wrap_boolvar:tk.BooleanVar = None

    __root:tk.Tk = None
    __w_text:tk.Text = None
    __search_dialog:widget.SearchDialog = None

    @property
    def __seleted_text_content(self) -> str:
        return self.__w_text.get(tk.SEL_FIRST,tk.SEL_LAST)

    @property
    def __seleted_text_index(self) -> tuple[str,str]:
        sel_first = self.__w_text.index(tk.SEL_FIRST)
        sel_last = self.__w_text.index(tk.SEL_LAST)
        return (sel_first,sel_last) 

    def __init__(self,root:tk.Tk,w_text:tk.Text):
        self.__root = root
        self.__w_text = w_text
        self.word_wrap_boolvar = tk.BooleanVar(self.__w_text)
        self.word_wrap_boolvar.set(True)

    def word_wrap(self):
        if self.word_wrap_boolvar.get():
            self.__w_text.config(wrap="word")
        else:
            self.__w_text.config(wrap="none")

    def action_search(self):
        search_dialog = widget.SearchDialog(self.__root,self.__w_text)

    def action_replace(self):
        replace_dialog = widget.ReplaceDialog(self.__root,self.__w_text)
    
class FileProcesser:
    __w_text:tk.Text = None
    __file_path:Path = None

    def __init__(self,w_text:tk.Text):
        self.__w_text = w_text

    @property
    def __text_content(self):
        return self.__w_text.get("0.0",tk.END)
        
    @property
    def __file_content(self) -> str:
        if self.__file_path == None:
            return f"{chr(10)}"
        else:
            with open(self.__file_path,mode="r",encoding="utf-8") as file:
                content = file.read()
                return content

    @property
    def __is_saved(self) -> bool:
        # print(f">> {self.__text_content == self.__file_content}")
        # print("-"*50)
        # print(f">> self.__text_content({len(self.__text_content)}):\n{self.__text_content.replace(chr(10),'^')}")
        # print("-"*50)
        # print(f">> self.__file_content({len(self.__file_content)}):\n{self.__file_content.replace(chr(10),'^')}")
        return self.__text_content == self.__file_content
    
    def __initial(self):
        self.__w_text.delete("0.0",tk.END)
        self.__file_path = None

    def create_new(self):
        if self.__is_saved:
            self.__initial()
        else:
            ask = tkmsg.askyesno(title="create new?",message="The current editing content has not been saved.\nAre you sure to create a new?")
            if ask:
                self.__initial()

    def open_file(self,yes:bool=False):
        if self.__is_saved or yes:
            file_path = tkfdlg.askopenfilename(title="open file")
            if file_path == "":
                return None
            if Path(file_path).exists:
                self.__file_path = Path(file_path)
                self.__w_text.delete("0.0",tk.END)
                self.__w_text.insert("0.0",self.__file_content)
                self.__w_text.delete(tk.INSERT,tk.END)
            else:
                tkmsg.showerror(title="open error",message=f"The path({file_path.absolute}) don't exist!\nopen failed!")
        else:
            ask = tkmsg.askyesno(title="open new?",message="The current editing content has not been saved.\nAre you sure to open a new?")
            if ask:
                self.open_file(yes=True)
    
    def save_file(self):
        if self.__file_path == None:
            file_path = tkfdlg.asksaveasfilename(title="save")
            if file_path == "":
                return None
            self.__file_path = Path(file_path)
        else:
            with open(self.__file_path,mode="w",encoding="utf-8") as file:
                file.write(self.__text_content)
            tkmsg.showinfo(title="save",message="save done!")

    def save_as_file(self):
        file_path = tkfdlg.asksaveasfilename(title="save file as")
        if file_path == "":
            return None
        self.__file_path = Path(file_path)
        self.save_file()

class Clipboard:
    __w_text:tk.Text = None

    def __init__(self,w_text:tk.Text):
        self.__w_text = w_text

    @property
    def __seleted_text_content(self) -> str:
        return self.__w_text.get(tk.SEL_FIRST,tk.SEL_LAST)
    
    @property
    def __seleted_text_index(self) -> tuple[str,str]:
        sel_first = self.__w_text.index(tk.SEL_FIRST)
        sel_last = self.__w_text.index(tk.SEL_LAST)
        return (sel_first,sel_last) 
    
    @property
    def clipboard_text(self):
        return self.__w_text.selection_get(selection="CLIPBOARD")
    
    def copy(self):
        self.__w_text.clipboard_clear()
        self.__w_text.clipboard_append(self.__seleted_text_content)

    def cut(self):
        self.__w_text.clipboard_clear()
        self.__w_text.clipboard_append(self.__seleted_text_content)
        self.__w_text.delete(*self.__seleted_text_index)

    def paste(self):
        self.__w_text.insert(tk.INSERT,self.clipboard_text)

if __name__ == "__main__":
    main()
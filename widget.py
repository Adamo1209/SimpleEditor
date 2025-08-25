# widget.py

import tkinter as tk
import tkinter.messagebox as tkmsg

class SearchDialog:
    ui_font:tuple[str,int] = ("Maple Mono NF CN",11)
    top_lable_font:tuple[str,int] = ("Maple Mono NF CN",15)
    dialog_size:str = "450x150"
    dialog_title = "search dialog"
    searched_style = {"background":'yellow',"foreground":'red'}
    normal_text_style = {"background":'white',"foreground":'black'}
    search_tag = []

    __search_top:tk.Toplevel = None
    __search_text:tk.Text = None
    __w_text:tk.Text = None

    def __init__(self,root:tk.Tk,w_text:tk.Text):
        self.__w_text = w_text

        self.__search_top = tk.Toplevel(root)
        self.__search_top.bind("<Destroy>",self.__search_dialog_close)
        self.__search_top.geometry(self.dialog_size)
        self.__search_top.title(self.dialog_title)
        self.__search_top.resizable(False,False)

        tk.Label(self.__search_top,text=self.dialog_title,font=self.top_lable_font,background="white").pack(side="top",fill="both")

        frame = tk.Frame(self.__search_top,background="white")
        frame.pack(side="top",fill="both",expand=True)
        frame.rowconfigure([0,1],weight=1)
        frame.columnconfigure([0,1,2,3],weight=1)

        tk.Label(frame,text="search:",font=self.ui_font,background="white").grid(column=0,row=0)
        self.__search_text = tk.Text(frame,font=self.ui_font,height=1.25,width=25,borderwidth=3,relief="groove")
        self.__search_text.grid(column=1,row=0)
        tk.Button(frame,text="sarch",font=self.ui_font,command=self.search).grid(column=3,row=0)
        self.__search_top.mainloop()

    @property
    def search_text(self) -> str:
        text:str = self.__search_text.get("0.0",tk.END)
        if chr(10) in text:
            text = text.replace(chr(10),"")
        return text

    def search(self):
        search_text = self.search_text
        if search_text:
            search_result_index_start = self.__w_text.search(pattern=search_text,index="0.0",stopindex=tk.END)
            while search_result_index_start != "":
                search_result_index_end_cache = list(map(int,search_result_index_start.split(".")))
                search_result_index_end_cache[1] += (len(search_text))
                search_result_index_end = ".".join(map(str,search_result_index_end_cache))

                self.__w_text.tag_add(f"search_{search_text}",search_result_index_start,search_result_index_end)
                if (f"search_{search_text}") not in self.search_tag:
                    self.search_tag.append(f"search_{search_text}")
                self.__w_text.tag_config(f"search_{search_text}",**self.searched_style)
                
                search_result_index_start = self.__w_text.search(pattern=search_text,index=search_result_index_end,stopindex=tk.END)
        else:
            tkmsg.showwarning(title="search",message="No search text!")

    def __search_dialog_close(self,event):
        if self.search_tag:
            for i in self.search_tag:
                if i in self.__w_text.tag_names():
                    self.__w_text.tag_config(i,**self.normal_text_style)
                    self.__w_text.tag_delete(i)
            self.search_tag.clear()

class ReplaceDialog:
    ui_font:tuple[str,int] = ("Maple Mono NF CN",11)
    top_lable_font:tuple[str,int] = ("Maple Mono NF CN",15)
    dialog_size:str = "450x150"
    dialog_title = "replace dialog"
    replaced_style = {"background":'yellow',"foreground":'red'}
    normal_text_style = {"background":'white',"foreground":'black'}
    replace_tag = []

    __replace_top:tk.Toplevel = None
    __search_text:tk.Text = None
    __replace_text:tk.Text = None
    __w_text:tk.Text = None

    def __init__(self,root:tk.Tk,w_text:tk.Text):
        self.__w_text = w_text

        self.__replace_top = tk.Toplevel(root)
        self.__replace_top.bind("<Destroy>",self.__replace_dialog_close)
        self.__replace_top.geometry(self.dialog_size)
        self.__replace_top.title(self.dialog_title)
        self.__replace_top.resizable(False,False)

        tk.Label(self.__replace_top,text=self.dialog_title,font=self.top_lable_font,background="white").pack(side="top",fill="both")

        frame = tk.Frame(self.__replace_top,background="white")
        frame.pack(side="top",fill="both",expand=True)
        frame.rowconfigure([0,1],weight=1)
        frame.columnconfigure([0,1,2,3],weight=1)

        tk.Label(frame,text="search:",font=self.ui_font,background="white").grid(column=0,row=0)
        self.__search_text = tk.Text(frame,font=self.ui_font,height=1.25,width=25,borderwidth=3,relief="groove")
        self.__search_text.grid(column=1,row=0)
        tk.Label(frame,text="replace:",font=self.ui_font,background="white").grid(column=0,row=1)
        self.__replace_text = tk.Text(frame,font=self.ui_font,height=1.25,width=25,borderwidth=3,relief="groove")
        self.__replace_text.grid(column=1,row=1)
        tk.Button(frame,text="replace",font=self.ui_font,command=self.replace).grid(column=3,row=1)
        self.__replace_top.mainloop()

    @property
    def search_text(self) -> str:
        text:str = self.__search_text.get("0.0",tk.END)
        if chr(10) in text:
            text = text.replace(chr(10),"")
        return text
    
    @property
    def replace_text(self) -> str:
        text:str = self.__replace_text.get("0.0",tk.END)
        if chr(10) in text:
            text = text.replace(chr(10),"")
        return text

    def replace(self):
        search_text = self.search_text
        replace_text = self.replace_text
        if search_text:
            search_result_index_start = self.__w_text.search(pattern=search_text,index="0.0",stopindex=tk.END)
            if search_result_index_start:
                search_result_index_end_cache = list(map(int,search_result_index_start.split(".")))
                search_result_index_end_cache[1] += (len(search_text))
                search_result_index_end = ".".join(map(str,search_result_index_end_cache))
                self.__w_text.delete(search_result_index_start,search_result_index_end)
                self.__w_text.insert(search_result_index_start,replace_text)
                if replace_text:
                    search_result_index_end_cache = list(map(int,search_result_index_start.split(".")))
                    search_result_index_end_cache[1] += (len(replace_text))
                    search_result_index_end = ".".join(map(str,search_result_index_end_cache))

                    self.__w_text.tag_add(f"replace_{search_text}_{replace_text}",search_result_index_start,search_result_index_end)
                    if (f"replace_{search_text}_{replace_text}") not in self.replace_tag:
                        self.replace_tag.append(f"replace_{search_text}_{replace_text}")
                    self.__w_text.tag_config(f"replace_{search_text}_{replace_text}",**self.replaced_style)
            else:
                tkmsg.showinfo(title="replace",message="No replaceable text!")
        else:
            tkmsg.showwarning(title="replace",message="No search text!")

    def __replace_dialog_close(self,event):
        if self.replace_tag:
            for i in self.replace_tag:
                if i in self.__w_text.tag_names():
                    self.__w_text.tag_config(i,**self.normal_text_style)
                    self.__w_text.tag_delete(i)
            self.replace_tag.clear()

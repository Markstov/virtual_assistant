import tkinter as tk
from tkinter import ttk
from tts import va_speak

GENDER = [("М", "male"), ("Ж", "female")]
VOICES_M_NAMES = ["aidar", "eugene"]
VOICES_F_NAMES = ["baya", "kseniya", "xenia"]
VOICES_M = ["1", "2"]
VOICES_F = ["1", "2", "3"]

class BotSetting:

    def __init__ (self, name, gender, voice, sql_data):
        self.data = sql_data
        self.window = tk.Tk()
        self.window.title("Настройка бота")
        self.window.geometry("470x300")

        self.bot_name = tk.StringVar()
        self.bot_name.set(name)

        self.cur_gender = tk.StringVar()
        self.cur_gender.set(gender)

        if self.cur_gender.get() == GENDER[0][1]:
            self.cur_voices_list = VOICES_M
            self.voice_index = VOICES_M_NAMES.index(voice)

        elif self.cur_gender.get() == GENDER[1][1]:
            self.cur_voices_list = VOICES_F
            self.voice_index = VOICES_F_NAMES.index(voice)

        self.cur_voice = tk.StringVar()
        self.cur_voice.set(self.cur_voices_list[self.voice_index])
        self.voice = voice

    def run(self):
        lbl_name = tk.Label(text="Имя бота")
        lbl_name.grid(row=0, column=1, padx=15, pady=5)

        txt_edit = tk.Entry(self.window, width=20, textvariable=self.bot_name)
        txt_edit.grid(row=1, column=1, padx=15, pady=5)

        lbl_gender = tk.Label(text="Пол")
        lbl_gender.grid(row=2, column=1, padx=15, pady=5)

        buttons = [self.create_radio(s) for s in GENDER]
        for i in range(len(buttons)):
            buttons[i].grid(row=3, column=i*2, padx=5, pady=5)  

        lbl_voice = tk.Label(text="Голоса")
        lbl_voice.grid(row=4, column=1, padx=15, pady=5)

        self.combobox_voices = ttk.Combobox(textvariable=self.cur_voice, values=self.cur_voices_list, state="readonly")
        self.combobox_voices.grid(row=5, column=1, padx=15, pady=5)

        listen_voice = tk.Button(text="Прослушать голос", command=self.listen)
        listen_voice.grid(row=6, column=0, padx=15, pady=5)

        sql_data = tk.Button(text="Программы", command=self.sql_settings)
        sql_data.grid(row=6, column=2, padx=15, pady=5)

        confirm = tk.Button(text="Принять изменения", command=self.confirm_changes)
        confirm.grid(row=7, column=1, padx=15, pady=5)

        self.window.mainloop()
        print("EXIT FROM GUI")

    def create_radio(self, option):
        text, value = option
        return tk.Radiobutton(text=text, value=value,
                                command=self.change_voices_list,
                                variable=self.cur_gender)

    def change_voices_list(self):
        print(self.cur_gender.get())
        if self.cur_gender.get() == GENDER[0][1]:
            self.cur_voices_list = VOICES_M
        elif self.cur_gender.get() == GENDER[1][1]:
            self.cur_voices_list = VOICES_F

        self.combobox_voices.configure(values=self.cur_voices_list)
        self.cur_voice.set(self.cur_voices_list[0])

    def listen(self):
        if self.cur_gender.get() == GENDER[0][1]:
            self.voice = VOICES_M_NAMES[VOICES_M.index(self.cur_voice.get())]
        elif self.cur_gender.get() == GENDER[1][1]:
            self.voice = VOICES_F_NAMES[VOICES_F.index(self.cur_voice.get())]

        va_speak(f"Привет, меня зовут {self.bot_name.get()}", self.voice)
        print(f"Пол: {self.cur_gender.get()}, Голос: {self.cur_voice.get()}")

    def confirm_changes(self):
        if self.cur_gender.get() == GENDER[0][1]:
            self.voice = VOICES_M_NAMES[VOICES_M.index(self.cur_voice.get())]
        elif self.cur_gender.get() == GENDER[1][1]:
            self.voice = VOICES_F_NAMES[VOICES_F.index(self.cur_voice.get())]
        print(f"Save setting - Пол: {self.cur_gender.get()}, Голос: {self.cur_voice.get()}, Имя: {self.bot_name.get()}")
        self.window.destroy()

    def sql_settings(self):
        root = tk.Tk()
        root.title("Программы")
        table = Table(root, headings=('Name', 'Path', 'Alias'), rows=self.data)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        butt_add = tk.Button(root, text="Добавить")
        butt_add.pack(expand=tk.YES, fill=tk.BOTH)
        butt_conf = tk.Button(root, text="Сохранить изменения")
        butt_conf.pack(expand=tk.YES, fill=tk.BOTH)
        root.mainloop()


class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)
  
        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings
  
        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)
  
        for row in rows:
            table.insert('', tk.END, values=tuple(row))
  
        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Программы")
    table = Table(root, headings=('Name', 'Path', 'Alias'), rows=((1,2,3), (4,5,6), (4,5,6), (4,5,6), (4,5,6), (4,5,6), (4,5,6), (4,5,6), (4,5,6), (7,8,9), (7,8,9), (7,8,9), (7,8,9)))
    table.pack(expand=tk.YES, fill=tk.BOTH)
    butt_add = tk.Button(root, text="Добавить")
    butt_add.pack(expand=tk.YES, fill=tk.BOTH)
    butt_conf = tk.Button(root, text="Сохранить изменения")
    butt_conf.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
    # bs = BotSetting()
    # bs.run()
# window.title("Настройка бота")
# window.geometry("300x400")
# bot_name = tk.StringVar()
# bot_name.set("Олежа")
# lbl_name = tk.Label(text="Имя бота")
# lbl_name.grid(row=0, column=1, padx=15, pady=5)

# txt_edit = tk.Entry(window, width=20, textvariable=bot_name)
# txt_edit.grid(row=1, column=1, padx=15, pady=5)

# lbl_gender = tk.Label(text="Пол")
# lbl_gender.grid(row=2, column=1, padx=15, pady=5)

# cur_gender = tk.StringVar()
# cur_gender.set(gender[0][1])
# buttons = [create_radio(s) for s in gender]
# for i in range(len(buttons)):
#     buttons[i].grid(row=3, column=i*2, padx=15, pady=5)  

# lbl_voice = tk.Label(text="Голоса")
# lbl_voice.grid(row=4, column=1, padx=15, pady=5)

# cur_voices_list = VOICES_M
# cur_voice = tk.StringVar()
# cur_voice.set(cur_voices_list[0])
# combobox_voices = ttk.Combobox(textvariable=cur_voice, values=cur_voices_list, state="readonly")
# combobox_voices.grid(row=5, column=1, padx=15, pady=5)

# window.mainloop()
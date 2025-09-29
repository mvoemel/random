import tkinter
import tkinter.messagebox
from tkinter import ttk
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()



        # configure window
        self.title("Pruefmittel")
        self.geometry(f"{1100}x{580}")



        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)



        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Pruefmittel", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.radio_var = tkinter.IntVar(value=0) # 0 = aktuellen, 1 = gesperrt
        self.label_radio_group = customtkinter.CTkLabel(master=self.sidebar_frame, text="Anzeige von:")
        self.label_radio_group.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.sidebar_frame, text="aktuellen", variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=2, column=0, pady=10, padx=10, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.sidebar_frame, text="gesperrt", variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=3, column=0, pady=10, padx=10, sticky="n")

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Neues Pruefsmittel", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=5, column=0, padx=20, pady=10, sticky="n")
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))



        # ---------- create main table ---------------------------------------------------
        self.main_table_frame = customtkinter.CTkFrame(self)
        self.main_table_frame.grid(row=0, column=1, columnspan=1, sticky="nsew")

        treeviewStyle = ttk.Style()
        # treeviewStyle.theme_use("clam")
        treeviewStyle.configure("main_table_style.Treeview", #configure treeview
                                background="white",
                                foreground="black",
                                fieldbackground="white",
                                rowheight=30, 
                                highlightthickness=0, 
                                bd=0, 
                                font=("Arial", 18)
        )
        treeviewStyle.configure("main_table_style.Treeview.Heading", #configure heading
                                rowheight=50, 
                                font=('Arial', 15,'bold')
        )

        self.main_table = ttk.Treeview(self.main_table_frame, style="main_table_style.Treeview")

        # define columns
        self.main_table['columns'] = ('type', 'designation', 'test_equipment_number', 'repository', 'binder', 'w_interval', 'next_maintanance', 'serial_test_equipment')

        headerValues = ["Typ", "Bezeichnung", "Prüfmittelnummer", "Aufbewahrungsort", "Ordner", "W-Intervall in Monaten", "Nächste Wartung", "Serienprüfmittel"]
        examples = [["Gerät", "Gugus", "0192", "Büro", "1", "12", "24.07.2023", "ja"],
                    ["Wage", "Hello", "9374", "Labor", "2", "24", "01.01.2024", "ja"],
                    ["Gerät", "Fisch", "8374", "Labor", "2", "36", "05.05.2023", "nein"],
                    ["Bohrer", "Bosch", "8375", "Werkstatt", "3", "6", "07.07.2023", "nein"],
                    ["Ofen", "Heiss", "6634", "Labor", "2", "4", "09.10.2023", "ja"],
                    ["Schraubenzieher", "Kiste", "7752", "Werkstatt", "3", "3", "30.05.2023", "nein"]
        ]
        
        # format columns
        self.main_table.column("#0", width=0,  stretch="NO")
        self.main_table.column("type",anchor="center")
        self.main_table.column("designation",anchor="center")
        self.main_table.column("test_equipment_number",anchor="center")
        self.main_table.column("repository",anchor="center")
        self.main_table.column("binder",anchor="center")
        self.main_table.column("w_interval",anchor="center")
        self.main_table.column("next_maintanance",anchor="center")
        self.main_table.column("serial_test_equipment",anchor="center")

        # create headings
        self.main_table.heading("#0", text="",anchor="center")
        self.main_table.heading("type", text=headerValues[0], anchor="center")
        self.main_table.heading("designation", text=headerValues[1], anchor="center")
        self.main_table.heading("test_equipment_number", text=headerValues[2], anchor="center")
        self.main_table.heading("repository", text=headerValues[3], anchor="center")
        self.main_table.heading("binder", text=headerValues[4], anchor="center")
        self.main_table.heading("w_interval", text=headerValues[5], anchor="center")
        self.main_table.heading("next_maintanance", text=headerValues[6], anchor="center")
        self.main_table.heading("serial_test_equipment", text=headerValues[7], anchor="center")

        # insert data
        self.main_table.insert(parent='',index='end',iid=0,text='',
                        values=(examples[0][0],examples[0][1],examples[0][2],examples[0][3],examples[0][4],examples[0][5],examples[0][6],examples[0][7]),
                        tags=('even',))
        self.main_table.insert(parent='',index='end',iid=1,text='',
                        values=(examples[1][0],examples[1][1],examples[1][2],examples[1][3],examples[1][4],examples[1][5],examples[1][6],examples[1][7]),
                        tags=('odd',))
        self.main_table.insert(parent='',index='end',iid=2,text='',
                        values=(examples[2][0],examples[2][1],examples[2][2],examples[2][3],examples[2][4],examples[2][5],examples[2][6],examples[2][7]),
                        tags=('even',))
        self.main_table.insert(parent='',index='end',iid=3,text='',
                        values=(examples[3][0],examples[3][1],examples[3][2],examples[3][3],examples[3][4],examples[3][5],examples[3][6],examples[3][7]),
                        tags=('odd',))
        self.main_table.insert(parent='',index='end',iid=4,text='',
                        values=(examples[4][0],examples[4][1],examples[4][2],examples[4][3],examples[4][4],examples[4][5],examples[4][6],examples[4][7]),
                        tags=('even',))
        self.main_table.insert(parent='',index='end',iid=5,text='',
                        values=(examples[5][0],examples[5][1],examples[5][2],examples[5][3],examples[5][4],examples[5][5],examples[5][6],examples[5][7]),
                        tags=('odd',))


        self.main_table.tag_configure('odd', background='#E8E8E8')
        self.main_table.tag_configure('even', background='#DFDFDF')

        self.main_table.pack(fill="both", expand=1) # to fill treeview to full frame size



        # set default values
        self.appearance_mode_optionemenu.set("System")

        # detailed item frame
        # self.item_detailed_frame = customtkinter.CTkFrame(self)
        # self.item_detailed_frame.grid(row=0, column=1, columnspan=1, sticky="nsew")

    # ----------end init function--------------------------------------------------------


    def sidebar_button_event(self):
        # TODO: implement "Neues Pruefsmittel" button
        # opens a new window where you can define all information for a new pruefmittel item and then with save
        # you can add this new item to the DB and then the window closes itself
        print("sidebar_button click")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        # TODO: should also change the ttk and tkinter widgets to have the right color
        customtkinter.set_appearance_mode(new_appearance_mode)

    def clear_widgets():
        return

    def load_frame_1():
        return

    def load_frame_2():
        return
    
    def fetch_db():
        return
    





if __name__ == "__main__":
    app = App()
    app.mainloop()
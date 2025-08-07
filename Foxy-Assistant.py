import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pluginsList
import threading

class FoxyAssistant:
    def __init__(self, root):
        # load root window
        self.root = root
        self.root.title("Foxy Assistant")
        self.root.geometry("640x480")
        self.message_labels = []
        
        # Load avatar image
        self.avatar_user = ImageTk.PhotoImage(Image.open("avatar.png").resize((32, 32)))
        self.avatar_foxy = ImageTk.PhotoImage(Image.open("foxy.png").resize((32, 32)))

        # set global vars
        self.reset_globals()

        # start GUI
        self.__build_ui()
    
    def reset_globals(self):
        self.SETTINGS = {}
        self.SETTINGS_FILE_LOCATION = None
        self.SELECTED_PLUGIN = None
        self.SELECTED_PLUGIN_HEADER = ""
    #########################################################################################
    #########                            PUBLIC FUNCTIONS                           #########
    #########################################################################################
    
    def start(self):
        # setup main menu text
        text = "שלום! אני שועלי, העוזר הוירטואלי"+"\n"
        text += "?"
        text += "מה תרצו לעשות היום"
        
        # setup main menu options
        options = pluginsList.Apps

        # displays menu
        self.menu(text, options)

    def menu(self, txt, options):
        # setup text
        i = 0
        txt += "\n"
        txt += "בחרו את האופציה הרצויה על ידי שליחת המספר הרלוונטי"
        txt += "\n"
        available_options = []
        for option in options:
            i += 1
            txt += option[0]+" "
            txt += "("+str(i)+")"
            txt += "\n"
            available_options.append(str(i))
        txt = txt[:-1]

        # get input
        choice = self.input(txt)
        while not choice in available_options:
            choice = self.input("בחירה לא תקינה, נסו שוב")
        
        # activate the selected function
        if self.SELECTED_PLUGIN == None:
            self.SELECTED_PLUGIN_HEADER = "בחרתם "
            self.SELECTED_PLUGIN_HEADER += options[int(choice)-1][0]
            self.SELECTED_PLUGIN = options[int(choice)-1][1]
            self.SETTINGS_FILE_LOCATION = "Plugins/"+options[int(choice)-1][2]+"/settings.txt"
            thread = threading.Thread(target= lambda:self.SELECTED_PLUGIN(self))
            thread.start()
        else:
            options[int(choice)-1][1]()
    
    def print(self, txt):
        self.__display_message(txt, sender='foxy')  # tell it this is Foxy

    def input(self, txt):
        delay_done = tk.BooleanVar()
        root.after(200, lambda: delay_done.set(True))  # 500 ms delay
        root.wait_variable(delay_done)
        self.__display_message(txt, sender='foxy')  # tell it this is Foxy
        self.entry.config(state='normal')
        self.send_button.config(state='normal')
        self.entry.focus()
        self.user_responce = tk.StringVar()
        root.wait_variable(self.user_responce)
        return self.user_responce.get()
    
    def update_progress_bar(self, percentage):
        self.loading_bar['value'] = percentage
    
    def launch(self, options, settings):
        # main menu text
        txt = self.SELECTED_PLUGIN_HEADER

        # load settings
        if len(settings):
            # add standard options 
            options.append(("הגדרות",self.__set_settings))
            txt += "\n\n"
            txt += ":"
            txt += "הגדרות"
            txt += "\n"
            settings_file = open(self.SETTINGS_FILE_LOCATION, 'a')
            settings_file.close()
            settings_file = open(self.SETTINGS_FILE_LOCATION, 'r')
            lines = settings_file.readlines()
            settings_file.close()
            
            for line in lines:
                line = line.split(">")
                key = line[0].strip()
                val = line[1].strip()
                if key in settings:
                    self.SETTINGS[key] = (settings[key],val)
            
            for key, val in settings.items():
                if key in self.SETTINGS:
                    txt += self.SETTINGS[key][1]
                    txt += " :"
                    txt += val
                else:
                    txt += val
                    txt += ": "
                    txt += "לא מוגדר"
                    self.SETTINGS[key] = (settings[key], "None")
                txt += "\n"
        
        options.append(("יציאה",self.__exit_plugin))

        # display menu
        self.menu(txt, options)
    
    def question(self, txt):
        options = []
        options.append("כן")
        options.append("לא")

        # setup text
        i = 0
        txt += "\n"
        txt += "בחרו את האופציה הרצויה על ידי שליחת המספר הרלוונטי"
        txt += "\n"
        available_options = []
        for option in options:
            i += 1
            txt += option+" "
            txt += "("+str(i)+")"
            txt += "\n"
            available_options.append(str(i))
        txt = txt[:-1]

        # get input
        choice = self.input(txt)
        while not choice in available_options:
            choice = self.input("בחירה לא תקינה, נסו שוב")
        
        # activate the selected function
        return int(choice)-1 == 0

    def restart(self):
        # restart
        self.update_progress_bar(0)
        self.SELECTED_PLUGIN(self)

    #########################################################################################
    #########                           PRIVATE FUNCTIONS                           #########
    #########################################################################################
    
    def __set_settings(self):
        # get new settings
        for key, val in self.SETTINGS.items():
            hebrew_name = val[0]
            value = val[1]
            txt = ""
            txt += value
            txt += " :"
            txt += "הגדרה נוכחית עבור "
            txt += hebrew_name
            txt += "\n"
            txt += "?האם תרצו לשנות את הערך הנוכחי"
            if self.question(txt):
                txt = "הכניסו את הערך החדש עבור:"
                txt += " "
                txt += hebrew_name
                self.SETTINGS[key] = (hebrew_name,self.input(txt))
                txt = ""
                txt += "עבור הגדרה"
                txt += ":"
                txt += " "
                txt += hebrew_name
                txt += "\n"
                txt += "נקלט ערך חדש"
                txt += "\n"
                txt += self.SETTINGS[key][1]
                self.print(txt)
            else:
                self.print("הערך הנוכחי יישמר")
        
        # save new settings
        file = open(self.SETTINGS_FILE_LOCATION, 'w')
        for key, val in self.SETTINGS.items():
            file.write(key+" > "+val[1]+"\n")
        
        # restart
        self.restart()
    
    def __exit_plugin(self):
        self.reset_globals()
        self.start()

    #########################################################################################
    #########                       PRIVATE GUI FUNCTIONS                           #########
    #########################################################################################

    def __build_ui(self):
        # ---- TOP CHAT DISPLAY ----
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(chat_frame, bg="#add8e6", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(chat_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=lambda *args: [self.__on_scroll(*args), self.canvas.yview(*args)])  # Call on_scroll and scroll
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.is_scrolling = False

        self.messages_frame = tk.Frame(self.canvas, bg="#add8e6")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")

        self.canvas.bind("<Configure>", self.__on_canvas_configure)
        self.messages_frame.bind("<Configure>", self.__on_frame_configure)

        # ---- BOTTOM INPUT FRAME ----
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.entry = tk.Entry(input_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry.bind("<Return>", self.__send_message)

        self.send_button = tk.Button(input_frame, text="שלח", command=self.__send_message)
        self.send_button.pack(side=tk.RIGHT)
        self.entry.delete(0, tk.END)
        self.entry.config(state='disabled')
        self.send_button.config(state='disabled')
        
        # ---- LOADING BAR ----
        self.loading_bar = ttk.Progressbar(self.root, orient="horizontal", mode="determinate")
        self.loading_bar.pack(fill=tk.X, padx=5, pady=(0, 0))  # Place above the input frame

        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        self.start()
    
    def __send_message(self, event=None):
        message = self.entry.get()
        if message.strip():
            self.__display_message(message, sender='user')
            self.entry.delete(0, tk.END)
            self.entry.config(state='disabled')
            self.send_button.config(state='disabled')
            self.user_responce.set(message)
    
    def __display_message(self, message_text, sender='user'):
        self.is_scrolling = False
        msg_row = tk.Frame(self.messages_frame, bg="#add8e6")
        if sender == 'user':
            msg_row.pack(fill='x', padx=10, pady=5, anchor='w')
            avatar_img = self.avatar_user
            bubble_color = "#ccffcc"

            avatar_label = tk.Label(msg_row, image=avatar_img, bg="#add8e6")
            avatar_label.pack(side='left', padx=(0, 10), anchor='n')

            msg_frame = tk.Frame(msg_row, bg="#add8e6")
            msg_frame.pack(side='left', fill='x', expand=True)

            msg_label = tk.Label(
                msg_frame,
                text=message_text,
                bg=bubble_color,
                fg="black",
                justify='left',
                anchor='w',
                padx=10,
                pady=5,
                wraplength=self.canvas.winfo_width() - 100
            )
            msg_label.pack(fill='x', expand=True)

        else:  
            # Foxy
            msg_row.pack(fill='x', padx=10, pady=5, anchor='e')
            avatar_img = self.avatar_foxy
            bubble_color = "#ffe6cc"

            # Avatar on LEFT for Foxy
            avatar_label = tk.Label(msg_row, image=avatar_img, bg="#add8e6")
            avatar_label.pack(side='right', padx=(10, 0), anchor='n')

            # Message bubble on RIGHT
            msg_frame = tk.Frame(msg_row, bg="#add8e6")
            msg_frame.pack(side='right', fill='x', expand=True)

            msg_label = tk.Label(
                msg_frame,
                text=message_text,
                bg=bubble_color,
                fg="black",
                justify='right',
                anchor='e',
                padx=10,
                pady=5,
                wraplength=self.canvas.winfo_width() - 100
            )
            msg_label.pack(fill='x', expand=True)
        
    def __on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        wrap_width = event.width - 40
        for label in self.message_labels:
            label.config(wraplength=wrap_width)

    def __on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        if not self.is_scrolling:
            self.canvas.yview_moveto(1.0)

    def __on_scroll(self, *args):
        # This method will be called whenever the scrollbar moves
        self.is_scrolling = True  # Set your variable to False or carry out any other logic here

if __name__ == "__main__":
    root = tk.Tk()
    app = FoxyAssistant(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pluginsList

class FoxyAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Foxy Assistant")
        self.root.geometry("640x480")
        self.message_labels = []
        # Load avatar image
        self.avatar_user = ImageTk.PhotoImage(Image.open("avatar.png").resize((32, 32)))
        self.avatar_foxy = ImageTk.PhotoImage(Image.open("foxy.png").resize((32, 32)))
        self.build_ui()
        self.bind_scroll_events()

    def build_ui(self):
        # ---- TOP CHAT DISPLAY ----
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(chat_frame, bg="#add8e6", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(chat_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.messages_frame = tk.Frame(self.canvas, bg="#add8e6")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")

        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.messages_frame.bind("<Configure>", self.on_frame_configure)

        # ---- BOTTOM INPUT FRAME ----
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.entry = tk.Entry(input_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(input_frame, text="שלח", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        self.entry.delete(0, tk.END)
        self.entry.config(state='disabled')
        self.send_button.config(state='disabled')
        self.main_menu()
    
    def main_menu(self):
        text = "שלום! אני שועלי, העוזר הוירטואלי"+"\n"
        text += "?"
        text += "מה תרצו לעשות היום"
        options = []
        for plugin in pluginsList.Apps:
            options.append(plugin[0])
        choice = self.choose(text, options)
        try:
            pluginsList.Apps[int(choice)-1][1](self)
        except:
            self.print("בחירה לא תקינה, נסו שוב")


    def choose(self, text, options):
        i = 0
        text += "\n"
        text += "בחרו את האופציה הרצויה על ידי שליחת המספר הרלוונטי"
        text += "\n"
        available_options = []
        for option in options:
            i += 1
            text += option+" "
            text += "("+str(i)+")"
            text += "\n"
            available_options.append(str(i))
        text = text[:-1]
        choice = self.input(text)
        while not choice in available_options:
            choice = self.input("בחירה לא תקינה, נסו שוב")
        return choice
    
    def print(self, text):
        self.display_message(text, sender='foxy')  # tell it this is Foxy

    def input(self, text):
        delay_done = tk.BooleanVar()
        root.after(500, lambda: delay_done.set(True))  # 500 ms delay
        root.wait_variable(delay_done)
        self.display_message(text, sender='foxy')  # tell it this is Foxy
        self.entry.config(state='normal')
        self.send_button.config(state='normal')
        self.entry.focus()
        self.user_responce = tk.StringVar()
        root.wait_variable(self.user_responce)
        return self.user_responce.get()
    
    def send_message(self, event=None):
        message = self.entry.get()
        if message.strip():
            self.display_message(message, sender='user')
            self.entry.delete(0, tk.END)
            self.entry.config(state='disabled')
            self.send_button.config(state='disabled')
            self.user_responce.set(message)
            #self.root.after(800, self.respond)  # Simulate delay before bot responds

    def respond(self, response_text):
        self.display_message(response_text, sender='foxy')  # tell it this is Foxy
        self.entry.config(state='normal')
        self.send_button.config(state='normal')
        self.entry.focus()

    def display_message(self, message_text, sender='user'):
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
                text=message_text,  # Force RTL direction
                bg=bubble_color,
                fg="black",
                justify='right',
                anchor='e',
                padx=10,
                pady=5,
                wraplength=self.canvas.winfo_width() - 100
            )
            msg_label.pack(fill='x', expand=True)
        
        self.canvas.yview_moveto(1.0)
        
    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        wrap_width = event.width - 40
        for label in self.message_labels:
            label.config(wraplength=wrap_width)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def bind_scroll_events(self):
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)
        self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            direction = -1 if event.delta > 0 else 1
            self.canvas.yview_scroll(direction, "units")


if __name__ == "__main__":
    root = tk.Tk()
    app = FoxyAssistant(root)
    root.mainloop()

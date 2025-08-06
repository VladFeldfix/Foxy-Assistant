class main:
    def __init__(self, master):
        self.top = master
        self.start()
    
    def start(self):
        from_folder = "D:/Users/Vlad/Projects/Applications/Foxy-Assistant"
        to_folder = "D:/Users/Vlad/Projects/Applications/Foxy-Assistant"
        text = "בחרתם לסדר אלבום תמונות"
        text += "\n"
        text += from_folder
        text += " : "
        text += "תיקיית מוצא"
        text += "\n"
        text += to_folder
        text += " : "
        text += "תיקיית יעד"
        options = []
        options.append("התחל")
        options.append("הגדרות")
        choice = self.top.choose(text, options)
        if choice == "1":
            self.run()

    def run(self):
        self.top.print("RUNING...")
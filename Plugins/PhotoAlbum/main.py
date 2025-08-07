class mainClass:
    def __init__(self, master):
        self.top = master
        self.start()
    
    def start(self):
        # setup main menu
        options = []
        options.append(("התחל",self.run))

        # setup settings
        required_settings = {}
        required_settings["SOURCE FOLDER"] = "תקיית מוצא"
        required_settings["DESTINATION FOLDER"] = "תקיית יעד"

        # display plugin main menu
        self.top.launch(options, required_settings)

    def run(self):
        # restart
        self.top.restart()
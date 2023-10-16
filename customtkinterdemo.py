import tkinter
import customtkinter
import colorsys
import subprocess

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

isDiscordOn = False



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Raspberry LCD + Temperature Sensor + Joystick + Button")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        # make a 2x2 grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="MyProject",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.activate_bot
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.deactivate_bot
        )
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame
        )
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # Horizontal progress bar
        self.horizontal_progressbar = customtkinter.CTkProgressBar(
            self, orientation="horizontal"
        )
        self.horizontal_progressbar.grid(
            row=2, column=1, padx=(20, 0), pady=(0, 20), sticky="ew"
        )

        # Vertical progress bar
        self.vertical_progressbar = customtkinter.CTkProgressBar(
            self, orientation="vertical"
        )
        self.vertical_progressbar.grid(
            row=1, column=2, padx=(0, 20), pady=(20, 0), sticky="ns"
        )

        # Canvas for joystick representation
        self.canvas = tkinter.Canvas(self, width=200, height=200)
        self.canvas.grid(row=1, column=1, padx=20, pady=20)
        self.circle = self.canvas.create_oval(
            90, 90, 110, 110, fill="blue"
        )  # Initial position

        # set default values
        self.sidebar_button_1.configure(text="Turn On Discord Bot")
        self.sidebar_button_2.configure(text="Turn Off Discord Bot")

    def activate_bot(self):
        global isDiscordOn
        if not isDiscordOn:
            process = subprocess.Popen(["python3", "main.py"])
            isDiscordOn = True

    
    def deactivate_bot(self):
        global isDiscordOn
        if isDiscordOn:
            self.sidebar_button_2.configure(text="Turn On Raspberry Pi")
            isDiscordOn = False
        else:
            self.sidebar_button_2.configure(text="Turn Off Raspberry Pi")
            isDiscordOn = True

    def update_joystick_position(self, x, y):
        # Update progress bars
        self.horizontal_progressbar.set(x)
        self.vertical_progressbar.set(y)

        # Update circle position on canvas
        self.canvas.coords(self.circle, x - 10, y - 10, x + 10, y + 10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
 
import tkinter
import customtkinter
import colorsys
import subprocess
import global_variables
from colorsys import rgb_to_hls
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import cooldown, BucketType
import time
import lirc
import RPi_I2C_driver
import RPi.GPIO as GPIO
import Adafruit_DHT
import openai
import ADC0834




GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
ADC0834.setup()
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

isDiscordOn = False

process = None

isJoystickOn = False



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

        # temperature and humidity frame side by side with button to get temperature and humidity
        self.temperature_humidity_frame = customtkinter.CTkFrame(
            self, corner_radius=0
        )

        self.temperature_humidity_frame.grid(
            row=0, column=1, sticky="nsew", padx=20, pady=20
        )

        self.temperature_textbox = customtkinter.CTkLabel(
            self.temperature_humidity_frame,
            text="Temperature: 0°C",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )

        self.temperature_textbox.grid(row=0, column=0, padx=20, pady=10)

        self.humidity_textbox = customtkinter.CTkLabel(
            self.temperature_humidity_frame,
            text="Humidity: 0%",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )

        self.humidity_textbox.grid(row=0, column=1, padx=20, pady=10)

        self.get_temperature_button = customtkinter.CTkButton(
            self.temperature_humidity_frame, command=self.get_values
        )

        self.get_temperature_button.grid(row=0, column=2, padx=20, pady=10)

        self.loading_textbox = customtkinter.CTkLabel(
            self.temperature_humidity_frame,
            text=" ",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )



        # set default values
        self.sidebar_button_1.configure(text="Turn On Discord Bot")
        self.temperature_textbox.configure(text="Temperature: 0°C")
        self.humidity_textbox.configure(text="Humidity: 0%")
        self.get_temperature_button.configure(text="Get Temperature and Humidity")


    def activate_bot(self):
        global isDiscordOn
        if not isDiscordOn:
            self.sidebar_button_1.configure(text="Turn Off Discord Bot")
            process = subprocess.Popen(["python3", "main.py"])
            isDiscordOn = True
        else:
            self.sidebar_button_1.configure(text="Turn On Discord Bot")
            process.kill()
            isDiscordOn = False

    
    def update_temperature(self, temperature):
        self.temperature_textbox.configure(text=f"Temperature: {temperature}°C")

    def update_humidity(self, humidity):
        self.humidity_textbox.configure(text=f"Humidity: {humidity}%")
    
    def get_values(self):
        temperature, humidity = global_variables.get_temperature_and_humidity()
        self.update_temperature(temperature)
        self.update_humidity(humidity)
    

    

    
    



if __name__ == "__main__":
    app = App()
    app.mainloop()

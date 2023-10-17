import os
import signal
import customtkinter
import subprocess
import global_variables
import ADC0834


is_discord_on = False
process = None

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Raspberry LCD + Temperature Sensor + Joystick + Button")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

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

        self.temperature_humidity_frame = customtkinter.CTkFrame(
            self, corner_radius=10
        )

        self.temperature_humidity_frame.grid(
            row=0, column=1, sticky="nsew", padx=20, pady=10
        )

        self.joystick_position_frame = customtkinter.CTkFrame(
            self, corner_radius=10
        )

        self.joystick_position_frame.grid(
            row=1, column=1, sticky="nsew", padx=20, pady=10
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

        self.loading_textbox.grid(row=0, column=3, padx=20, pady=10)

        self.display_joystick_x_textbox = customtkinter.CTkLabel(
            self.joystick_position_frame,
            text="X: 0",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )

        self.display_joystick_x_textbox.grid(row=0, column=0, padx=20, pady=10)

        self.display_joystick_y_textbox = customtkinter.CTkLabel(
            self.joystick_position_frame,
            text="Y: 0",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )

        self.display_joystick_y_textbox.grid(row=0, column=1, padx=20, pady=10)

        self.start_monitoring_button = customtkinter.CTkButton(
            self.joystick_position_frame, command=self.start_monitoring
        )

        self.start_monitoring_button.grid(row=0, column=2, padx=20, pady=10)

        self.sidebar_button_1.configure(text="Turn On Discord Bot")
        self.temperature_textbox.configure(text="Temperature: 0°C")
        self.humidity_textbox.configure(text="Humidity: 0%")
        self.get_temperature_button.configure(text="Get Temperature and Humidity")
        self.loading_textbox.configure(text=" ")
        self.start_monitoring_button.configure(text="Start Monitoring")


    def activate_bot(self):

        global is_discord_on, process

        if not is_discord_on:
            self.sidebar_button_1.configure(text="Turn Off Discord Bot")

            try:
                #end process
                process.kill()
            except AttributeError:
                pass

            process = subprocess.Popen(["python3", "main.py"])
            
            is_discord_on = True
        else:
            self.sidebar_button_1.configure(text="Turn On Discord Bot")

            try:
                #end process
                process.kill()
            except AttributeError:
                pass

            is_discord_on = False
    
    def update_temperature(self, temperature):

        self.temperature_textbox.configure(text=f"Temperature: {temperature}°C")

    def update_humidity(self, humidity):

        self.humidity_textbox.configure(text=f"Humidity: {humidity}%")
    
    def get_values(self):

        self.loading_textbox.configure(text="Loading...")
        self.loading_textbox.update()

        temperature, humidity = global_variables.get_temperature_and_humidity()

        self.update_temperature(temperature)
        self.update_humidity(humidity)

        self.loading_textbox.configure(text=" ")
        self.loading_textbox.update()

    def start_monitoring(self):

        global_variables.is_monitoring = not global_variables.is_monitoring

        if global_variables.is_monitoring:
            self.start_monitoring_button.configure(text="Stop Monitoring")
            self.start_monitoring_button.update()
            ADC0834.setup()
            self.monitor_loop()
        else:
            self.start_monitoring_button.configure(text="Start Monitoring")
            self.start_monitoring_button.update()
            

    def monitor_loop(self):

        if not global_variables.is_monitoring:
            self.start_monitoring_button.configure(text="Start Monitoring")
            self.start_monitoring_button.update()
            return
        
        x_val = ADC0834.getResult(0)
        y_val = ADC0834.getResult(1)

        self.display_joystick_x_textbox.configure(text=f"X: {x_val}")
        self.display_joystick_y_textbox.configure(text=f"Y: {y_val}")
        self.display_joystick_x_textbox.update()
        self.display_joystick_y_textbox.update()
        
        self.after(1, self.monitor_loop)


if __name__ == "__main__":
    app = App()
    app.mainloop()

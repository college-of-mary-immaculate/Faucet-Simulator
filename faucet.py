import tkinter as tk
import os
import sys
from PIL import Image, ImageTk

class FTC:
    def __init__(self, root):
        self.root = root
        self.active_update = False
        self.input_temp = 0
        self.target_temp = 0
        self.setup_ui()
        self.last_color = self.get_color(self.input_temp)

    def setup_ui(self):

        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.canvas = tk.Canvas(main_frame, bg="white")
        temp_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.temp_label = tk.Label(temp_frame, text=f"{self.input_temp:.1f}°C",
                                fg="black", bg="#007acc", font=("Helvetica", 32, "bold"),
                                padx=2, pady=10, relief=tk.RAISED)
        self.cold_percentage_label = tk.Label(temp_frame, text="Cold: 0%", bg="#f0f0f0", font=("Helvetica", 14))
        self.warm_percentage_label = tk.Label(temp_frame, text="Warm: 0%", bg="#f0f0f0", font=("Helvetica", 14))
        self.hot_percentage_label = tk.Label(temp_frame, text="Hot: 0%", bg="#f0f0f0", font=("Helvetica", 14))
        update_button = tk.Button(temp_frame, text="Set Temperature", command=self.set_temp_from_input,
                                bg="#007acc", fg="white", font=("Helvetica", 14), relief=tk.RAISED)
        self.temp_input = tk.Entry(temp_frame, font=("Helvetica", 16))
        reset_button = tk.Button(temp_frame, text="Reset", command=self.reset_temp,
                                bg="#ffa500", fg="white", font=("Helvetica", 14), relief=tk.RAISED)
        quit_button = tk.Button(temp_frame, text="Quit", command=self.root.quit,
                                bg="#ff4d4d", fg="white", font=("Helvetica", 14), relief=tk.RAISED)
        
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        temp_frame.grid(row=1, column=0, sticky="nsew")
        self.load_images()
        self.temp_label.grid(row=0, column=0, columnspan=6, sticky="nsew")
        self.cold_percentage_label.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.warm_percentage_label.grid(row=2, column=2, columnspan=2, sticky="nsew")
        self.hot_percentage_label.grid(row=2, column=4, columnspan=2, sticky="nsew")
        update_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.temp_input.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        reset_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        quit_button.grid(row=1, column=5, padx=10, pady=10, sticky="ew")

        update_button.bind("<Enter>", lambda e: update_button.config(bg="#005f8f"))
        update_button.bind("<Leave>", lambda e: update_button.config(bg="#007acc"))
        reset_button.bind("<Enter>", lambda e: reset_button.config(bg="#e6b800"))
        reset_button.bind("<Leave>", lambda e: reset_button.config(bg="#ffcc00"))
        quit_button.bind("<Enter>", lambda e: quit_button.config(bg="#D2042D"))
        quit_button.bind("<Leave>", lambda e: quit_button.config(bg="#ff4d4d"))

        self.water = self.canvas.create_rectangle(800, 410, 865, 272, fill=self.get_color(self.input_temp))

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        temp_frame.rowconfigure(0, weight=1)
        temp_frame.rowconfigure(2, weight=1)
        for i in range(6):
            temp_frame.columnconfigure(i, weight=1)

    def load_images(self):
        def resource_path(relative_path):
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)

        try:
            self.bg_image = Image.open(resource_path("assets/BR.jpg")).resize((1500, 720), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

            self.faucet_image = Image.open(resource_path("assets/faucet.png")).resize((300, 300), Image.LANCZOS)
            self.faucet_photo = ImageTk.PhotoImage(self.faucet_image)
            self.canvas.create_image(950, 10, anchor=tk.N, image=self.faucet_photo)

            self.bathroom_image = Image.open(resource_path("assets/bathroom.jpg")).resize((300, 675), Image.LANCZOS)
            self.bathroom_photo = ImageTk.PhotoImage(self.bathroom_image)
            self.canvas.create_image(1250, 10, anchor=tk.N, image=self.bathroom_photo)

            self.sink_image = Image.open(resource_path("assets/sink.png")).resize((600, 300), Image.LANCZOS)
            self.sink_photo = ImageTk.PhotoImage(self.sink_image)
            self.canvas.create_image(825, 400, anchor=tk.N, image=self.sink_photo)
        except Exception as e:
            print(f"Error loading images: {e}")

    def get_color(self, temp):
        cold_perc, warm_perc, hot_perc = self.triangular_membership(temp)

        self.cold_percentage_label.config(text=f"Cold: {cold_perc:.1f}%", font=("Helvetica", 14, "bold"),
                                           bg=self.interpolate_color("#0000ff", "#add8e6", cold_perc / 100))
        self.warm_percentage_label.config(text=f"Warm: {warm_perc:.1f}%", font=("Helvetica", 14, "bold"),
                                           bg=self.interpolate_color("#ffcc00", "#ff9900", warm_perc / 100))
        self.hot_percentage_label.config(text=f"Hot: {hot_perc:.1f}%", font=("Helvetica", 14, "bold"),
                                          bg=self.interpolate_color("#ff4500", "#8b0000", hot_perc / 100))

        if cold_perc > 0:
            return self.interpolate_color("#0000ff", "#add8e6", cold_perc / 100)
        elif warm_perc > 0:
            return self.interpolate_color("#ffcc00", "#ff9900", warm_perc / 100)
        else:
            return self.interpolate_color("#ff4500", "#8b0000", hot_perc / 100)   

    def triangular_membership(self, temp):
        temp = max(0, min(100, temp))

        if temp < 10:
            cold_perc = 100
            warm_perc = 0
            hot_perc = 0
        elif 10 <= temp < 30:
            cold_perc = max(0, 100 - (temp - 10) * 5)
            warm_perc = (temp - 10) * 5
            hot_perc = 0
        elif 30 <= temp < 50:
            cold_perc = 0
            warm_perc = max(0, 100 - (temp - 30) * 5)
            hot_perc = (temp - 30) * 5 
        else: 
            cold_perc = 0
            warm_perc = 0
            hot_perc = 100
        return cold_perc, warm_perc, hot_perc

    def interpolate_color(self, color1, color2, factor):
        factor = max(0, min(1, factor))

        r1, g1, b1 = self.hex_to_rgb(color1)
        r2, g2, b2 = self.hex_to_rgb(color2)
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def set_temp_from_input(self):
        try:
            self.target_temp = float(self.temp_input.get())
            if 0 <= self.target_temp <= 100:
                self.active_update = True
                self.update_temperature()
            else:
                self.show_custom_message("Input Error", "Please enter a valid temperature!\n0°C to 100°C")
        except ValueError:
            self.show_custom_message("Input Error", "Please enter a valid temperature!\n0°C to 100°C")


    def update_temperature(self):
        
        if self.active_update:
            if self.input_temp < self.target_temp:
                self.input_temp += 0.1
            elif self.input_temp > self.target_temp:
                self.input_temp -= 0.1
            self.input_temp = round(self.input_temp, 1)
            self.temp_label.config(text=f"{self.input_temp:.1f}°C")
            self.canvas.itemconfig(self.water, fill=self.get_color(self.input_temp))
            if abs(self.input_temp - self.target_temp) < 0.1:
                self.active_update = False
                self.show_temperature_message(self.input_temp)
            self.root.after(10, self.update_temperature)

    def show_temperature_message(self, temp):

        cold_perc, warm_perc, hot_perc = self.triangular_membership(temp)

        if cold_perc >= warm_perc and cold_perc >= hot_perc:
            self.show_custom_message("Temperature Status", "It's freezing cold!")
        elif warm_perc >= cold_perc and warm_perc >= hot_perc:
            self.show_custom_message("Temperature Status", "It's warm and ready to use!")
        else:
            self.show_custom_message("Temperature Status", "It's boiling hot")

    def show_custom_message(self, title, message):
        message_box = tk.Toplevel(self.root)
        message_box.title(title)
        message_box.geometry("400x200")
        message_box.configure(bg="#bdd4dd")
        message_label = tk.Label(message_box, text=message, padx=20, pady=20, font=("Helvetica", 14, "bold"), 
                                fg="#333333", bg="#bdd4dd")
        message_label.pack(pady=10)
        ok_button = tk.Button(message_box, text="OK", command=message_box.destroy, 
                            bg="#007acc", fg="white", font=("Helvetica", 12), 
                            relief=tk.RAISED, bd=2)  
        ok_button.pack(pady=(10, 20))  
        ok_button.bind("<Enter>", lambda e: ok_button.config(bg="#005f8f"))
        ok_button.bind("<Leave>", lambda e: ok_button.config(bg="#007acc"))

    def reset_temp(self):
        self.input_temp = 0
        self.temp_label.config(text=f"{self.input_temp:.1f}°C")
        self.canvas.itemconfig(self.water, fill=self.get_color(self.input_temp))
        self.temp_input.delete(0, tk.END)
        self.active_update = False

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Water Temperature Control")
    root.attributes("-fullscreen", True)
    app = FTC(root)
    root.mainloop()

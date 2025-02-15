import tkinter as tk
from tkinter import messagebox
import time
import winsound

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("800x600")
        self.root.configure(bg="#2C3E50")

        self.time_left = 0
        self.running = False

        tk.Label(root, text="Enter time (minutes.seconds):", fg="white", bg="#2C3E50", font=("Arial", 14)).pack(pady=10)
        self.entry = tk.Entry(root, font=("Arial", 16), justify='center')
        self.entry.pack(pady=5)

        self.label = tk.Label(root, text="00:00", font=("Arial", 140, "bold"), fg="white", bg="#2C3E50")
        self.label.pack(expand=True)

        button_frame = tk.Frame(root, bg="#2C3E50")
        button_frame.pack(pady=20, fill=tk.X)

        self.start_btn = tk.Button(button_frame, text="Start", command=self.start, font=("Arial", 14), bg="#27AE60", fg="white")
        self.start_btn.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        self.pause_btn = tk.Button(button_frame, text="Pause", command=self.pause, font=("Arial", 14), bg="#F1C40F", fg="black")
        self.pause_btn.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        self.reset_btn = tk.Button(button_frame, text="Reset", command=self.reset, font=("Arial", 14), bg="#E74C3C", fg="white")
        self.reset_btn.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        self.entry.bind("<Return>", lambda event: self.start())

    def update_timer(self):
        if self.time_left > 0 and self.running:
            mins, secs = divmod(self.time_left, 60)
            self.label.config(text=f"{mins:02}:{secs:02}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0 and self.running:
            self.running = False
            self.label.config(text="00:00")
            self.play_sound()
            messagebox.showinfo("Time's up!", "Countdown finished!")

    def play_sound(self):
        try:
            winsound.PlaySound("ac-bel-105874.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            time.sleep(2)
            winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception as e:
            messagebox.showwarning("Sound Error", f"Could not play sound: {e}")

    def start(self):
        if not self.running:
            try:
                time_value = self.entry.get()
                if "." in time_value:
                    minutes, seconds = map(int, time_value.split("."))
                else:
                    minutes, seconds = int(time_value), 0

                if seconds >= 60:
                    raise ValueError("Seconds must be between 0 and 59")

                self.time_left = (minutes * 60) + seconds
                self.running = True
                self.update_timer()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid time format (e.g., 5.30 for 5 minutes 30 seconds)")

    def pause(self):
        self.running = False

    def reset(self):
        self.running = False
        self.time_left = 0
        self.label.config(text="00:00")
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()

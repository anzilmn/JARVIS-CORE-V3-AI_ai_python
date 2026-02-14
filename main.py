import customtkinter as ctk
import threading
import math
import engine # Import the whole module
from actions import perform_action

ctk.set_appearance_mode("dark")

class AyshuOS(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Link this UI instance to the engine
        engine.ui_app = self

        self.title("AYSHU INTELLIGENCE - CORE v3.0")
        self.geometry("1100x750")
        self.configure(fg_color="#000000") 

        self.pulse_val = 0
        self.is_listening = False

        # --- THE HUD ---
        self.canvas = ctk.CTkCanvas(self, width=600, height=500, bg="black", highlightthickness=0)
        self.canvas.pack(pady=(20, 0), expand=True)
        self.create_premium_hud()

        # --- CONSOLE HUD ---
        self.console = ctk.CTkTextbox(self, width=320, height=200, fg_color="#050505", 
                                     border_color="#00f2ff", border_width=1, 
                                     font=("Consolas", 12), text_color="#00f2ff")
        self.console.place(x=30, y=30)

        # --- INPUT AREA ---
        self.input_container = ctk.CTkFrame(self, fg_color="transparent")
        self.input_container.pack(side="bottom", fill="x", padx=100, pady=60)

        self.text_input = ctk.CTkEntry(self.input_container, placeholder_text="AWAITING COMMAND...", 
                                      height=60, fg_color="#0a0a0a", border_color="#00f2ff", 
                                      font=("Segoe UI", 18), corner_radius=30, border_width=2)
        self.text_input.pack(side="left", fill="x", expand=True, padx=(0, 20))
        self.text_input.bind("<Return>", self.process_text)

        self.mic_btn = ctk.CTkButton(self.input_container, text="🎤", width=80, height=60, 
                                     corner_radius=30, fg_color="#ff00ff", hover_color="#d900d9", 
                                     font=("Arial", 24, "bold"), command=self.start_voice)
        self.mic_btn.pack(side="right")

        self.animate()
        
        # Initial greeting in a thread so UI doesn't lag
        threading.Thread(target=lambda: engine.speak("Ayshu online. Systems are green, vro."), daemon=True).start()

    def create_premium_hud(self):
        cx, cy = 300, 250
        self.canvas.create_oval(cx-210, cy-210, cx+210, cy+210, outline="#0a1a1f", width=1)
        self.canvas.create_oval(cx-180, cy-180, cx+180, cy+180, outline="#0f2d36", width=2)
        self.outer_glow = self.canvas.create_oval(cx-140, cy-140, cx+140, cy+140, outline="#00f2ff", width=1)
        self.inner_core = self.canvas.create_oval(cx-115, cy-115, cx+115, cy+115, outline="#00f2ff", width=5)
        self.canvas.create_text(cx, cy, text="AYSHU", fill="#00f2ff", font=("Orbitron", 32, "bold"))
        self.status_text = self.canvas.create_text(cx, cy+40, text="READY", fill="#00f2ff", font=("Segoe UI", 10, "bold"))

    def animate(self):
        self.pulse_val += 0.06
        pulse1 = (math.sin(self.pulse_val) * 12) + 120
        pulse2 = (math.sin(self.pulse_val * 0.5) * 20) + 150
        core_color = "#ff00ff" if self.is_listening else "#00f2ff"
        status = "LISTENING" if self.is_listening else "ACTIVE"
        cx, cy = 300, 250
        self.canvas.coords(self.inner_core, cx-pulse1, cy-pulse1, cx+pulse1, cy+pulse1)
        self.canvas.itemconfig(self.inner_core, outline=core_color)
        self.canvas.coords(self.outer_glow, cx-pulse2, cy-pulse2, cx+pulse2, cy+pulse2)
        self.canvas.itemconfig(self.outer_glow, outline=core_color)
        self.canvas.itemconfig(self.status_text, text=status, fill=core_color)
        self.after(20, self.animate)

    def log_msg(self, msg):
        self.console.insert("end", f"{msg}\n")
        self.console.see("end")

    def process_text(self, event=None):
        query = self.text_input.get()
        if query:
            self.text_input.delete(0, "end")
            self.log_msg(f"USER: {query}")
            threading.Thread(target=lambda: self.execute_flow(query), daemon=True).start()

    def execute_flow(self, query):
        engine.speak(f"I heard {query}. Doing it now.")
        perform_action(query)

    def start_voice(self):
        if not self.is_listening:
            self.is_listening = True
            self.mic_btn.configure(fg_color="#00f2ff", text_color="black")
            threading.Thread(target=self.run_voice, daemon=True).start()

    def run_voice(self):
        query = engine.take_command()
        if query != "none":
            self.text_input.insert(0, query.upper())
            self.execute_flow(query)
        else:
            self.log_msg("SYSTEM: Voice not recognized.")
        
        self.is_listening = False
        self.mic_btn.configure(fg_color="#ff00ff", text_color="white")

if __name__ == "__main__":
    engine.play_startup_sound()
    app = AyshuOS()
    app.mainloop()
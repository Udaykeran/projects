import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyttsx3
from pydub import AudioSegment

# Create a class for the application
class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Application")
        
        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Create widgets
        self.create_widgets()

        # Fetch available voices
        self.get_voices()

    def create_widgets(self):
        # Text input label and entry
        self.text_label = tk.Label(self.root, text="Enter text:")
        self.text_label.grid(row=0, column=0, padx=10, pady=10)
        self.text_input = tk.Text(self.root, height=5, width=50)
        self.text_input.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

        # Voice selection label and dropdown
        self.voice_label = tk.Label(self.root, text="Select voice:")
        self.voice_label.grid(row=1, column=0, padx=10, pady=10)
        self.voice_selection = ttk.Combobox(self.root, state="readonly")
        self.voice_selection.grid(row=1, column=1, padx=10, pady=10)

        # Sliders for rate, pitch, and volume
        self.rate_label = tk.Label(self.root, text="Rate:")
        self.rate_label.grid(row=2, column=0, padx=10, pady=10)
        self.rate_slider = tk.Scale(self.root, from_=50, to=200, orient="horizontal")
        self.rate_slider.set(100)  # Default rate
        self.rate_slider.grid(row=2, column=1, padx=10, pady=10)

        self.volume_label = tk.Label(self.root, text="Volume:")
        self.volume_label.grid(row=3, column=0, padx=10, pady=10)
        self.volume_slider = tk.Scale(self.root, from_=0, to=1, resolution=0.1, orient="horizontal")
        self.volume_slider.set(1.0)  # Default volume
        self.volume_slider.grid(row=3, column=1, padx=10, pady=10)

        # Buttons for play, pause, stop, and save
        self.play_button = tk.Button(self.root, text="Play", command=self.play_speech)
        self.play_button.grid(row=4, column=0, padx=10, pady=10)
        
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_speech)
        self.pause_button.grid(row=4, column=1, padx=10, pady=10)
        
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_speech)
        self.stop_button.grid(row=4, column=2, padx=10, pady=10)
        
        self.save_button = tk.Button(self.root, text="Save as MP3", command=self.save_speech)
        self.save_button.grid(row=4, column=3, padx=10, pady=10)
        
    def get_voices(self):
        # Get the available voices and set them in the dropdown
        voices = self.engine.getProperty("voices")
        self.voice_list = []
        for voice in voices:
            self.voice_list.append(voice)
            self.voice_selection["values"] = [v.name for v in self.voice_list]
        # Set the first voice as default selection
        self.voice_selection.current(0)

    def set_voice_properties(self):
        # Set the selected voice, rate, and volume in the engine
        selected_voice = self.voice_list[self.voice_selection.current()]
        self.engine.setProperty("voice", selected_voice.id)
        self.engine.setProperty("rate", self.rate_slider.get())
        self.engine.setProperty("volume", self.volume_slider.get())

    def play_speech(self):
        # Convert the text to speech and play it
        self.set_voice_properties()
        text = self.text_input.get("1.0", tk.END).strip()
        if text:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            messagebox.showwarning("No text", "Please enter some text to convert to speech.")

    def pause_speech(self):
        # Pause the speech playback
        self.engine.stop()

    def stop_speech(self):
        # Stop the speech playback
        self.engine.stop()

    def save_speech(self):
        # Save the generated speech as an MP3 file
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No text", "Please enter some text to convert to speech.")
            return
        
        # Get the save file path
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                 filetypes=[("MP3 files", "*.mp3")])
        if not file_path:
            return
        
        # Convert the text to speech and save it
        self.set_voice_properties()
        self.engine.save_to_file(text, file_path)
        self.engine.runAndWait()
        messagebox.showinfo("Success", f"Speech saved to {file_path}")

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()

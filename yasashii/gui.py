"""Yasashii Anki GUI - Graphical interface for Japanese word lookup and Anki card creation"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from .japanese_word import JapaneseWord
from .anki_client import AnkiClient


class YasashiiApp:
    """Main GUI application for Yasashii Anki"""

    def __init__(self, root):
        self.root = root
        self.root.title("Yasashii Anki")
        self.root.geometry("600x700")
        self.root.minsize(400, 500)

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface components"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)  # Input area
        main_frame.rowconfigure(4, weight=2)  # Results area

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Yasashii Anki",
            font=("Helvetica", 18, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 10), sticky="w")

        # Input label
        input_label = ttk.Label(
            main_frame,
            text="Enter Japanese words (one per line or comma-separated):"
        )
        input_label.grid(row=1, column=0, sticky="w", pady=(0, 5))

        # Input text area
        self.input_text = scrolledtext.ScrolledText(
            main_frame,
            height=8,
            font=("Helvetica", 14),
            wrap=tk.WORD
        )
        self.input_text.grid(row=1, column=0, sticky="nsew", pady=(20, 10))

        # Controls frame (checkbox and button)
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=2, column=0, sticky="ew", pady=10)
        controls_frame.columnconfigure(1, weight=1)

        # Checkbox for adding to Anki
        self.add_to_anki_var = tk.BooleanVar(value=True)
        self.add_to_anki_checkbox = ttk.Checkbutton(
            controls_frame,
            text="Add cards to Anki",
            variable=self.add_to_anki_var
        )
        self.add_to_anki_checkbox.grid(row=0, column=0, sticky="w")

        # Submit button
        self.submit_button = ttk.Button(
            controls_frame,
            text="Submit",
            command=self.on_submit
        )
        self.submit_button.grid(row=0, column=2, sticky="e", padx=(10, 0))

        # Results label
        results_label = ttk.Label(main_frame, text="Results:")
        results_label.grid(row=3, column=0, sticky="w", pady=(10, 5))

        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            main_frame,
            height=15,
            font=("Helvetica", 12),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.results_text.grid(row=4, column=0, sticky="nsew")

        # Configure text tags for styling
        self.results_text.tag_configure("word", font=("Helvetica", 14, "bold"))
        self.results_text.tag_configure("reading", foreground="gray")
        self.results_text.tag_configure("meaning", foreground="#333333")
        self.results_text.tag_configure("success", foreground="green")
        self.results_text.tag_configure("warning", foreground="orange")
        self.results_text.tag_configure("error", foreground="red")

    def on_submit(self):
        """Handle submit button click"""
        # Get input text and parse words
        input_content = self.input_text.get("1.0", tk.END).strip()
        if not input_content:
            return

        # Parse words: split by newlines and commas, strip whitespace
        words = []
        for line in input_content.split("\n"):
            for word in line.split(","):
                word = word.strip()
                if word:
                    words.append(word)

        if not words:
            return

        # Disable submit button during processing
        self.submit_button.config(state=tk.DISABLED)

        # Clear results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.config(state=tk.DISABLED)

        # Process words in background thread
        add_to_anki = self.add_to_anki_var.get()
        thread = threading.Thread(
            target=self.process_words,
            args=(words, add_to_anki),
            daemon=True
        )
        thread.start()

    def process_words(self, words, add_to_anki):
        """Process words and update results (runs in background thread)"""
        client = AnkiClient() if add_to_anki else None

        for word_text in words:
            # Look up word
            word = JapaneseWord(word_text)

            # Update UI from main thread
            self.root.after(0, lambda w=word, wt=word_text: self.display_word_result(w, wt, client))

        # Re-enable submit button when done
        self.root.after(0, lambda: self.submit_button.config(state=tk.NORMAL))

    def display_word_result(self, word, word_text, client):
        """Display a single word result in the results area"""
        self.results_text.config(state=tk.NORMAL)

        if word.meaning:
            # Word header
            readings = ", ".join(word.meaning.get("readings", []))
            if readings:
                self.results_text.insert(tk.END, f"{word_text} ", "word")
                self.results_text.insert(tk.END, f"({readings})\n", "reading")
            else:
                self.results_text.insert(tk.END, f"{word_text}\n", "word")

            # Meanings
            meanings_dict = word.meaning.get("meanings", {})
            sense_number = 1
            for sense_key, glosses in meanings_dict.items():
                glosses_str = ", ".join(glosses)
                pos = sense_key.split(" ", 1)[1] if " " in sense_key else sense_key
                self.results_text.insert(
                    tk.END,
                    f"  {sense_number}. ({pos}) {glosses_str}\n",
                    "meaning"
                )
                sense_number += 1

            # Add to Anki if requested
            if client:
                try:
                    result = client.create_card(word.meaning)
                    deck = result.get("deck_name", "unknown")
                    audio_status = "with audio" if result.get("audio_available") else "without audio"
                    self.results_text.insert(
                        tk.END,
                        f"  -> Added to {deck} {audio_status}\n",
                        "success"
                    )
                except Exception as e:
                    if "duplicate" in str(e).lower():
                        self.results_text.insert(
                            tk.END,
                            f"  -> Already exists in deck\n",
                            "warning"
                        )
                    else:
                        self.results_text.insert(
                            tk.END,
                            f"  -> Error: {e}\n",
                            "error"
                        )
        else:
            self.results_text.insert(tk.END, f"{word_text}\n", "word")
            self.results_text.insert(tk.END, "  -> Not found\n", "error")

        self.results_text.insert(tk.END, "\n")
        self.results_text.config(state=tk.DISABLED)

        # Auto-scroll to bottom
        self.results_text.see(tk.END)


def run_app():
    """Create and run the application"""
    root = tk.Tk()
    app = YasashiiApp(root)
    root.mainloop()

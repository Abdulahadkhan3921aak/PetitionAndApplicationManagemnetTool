import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import scrolledtext
from tkinterweb import HtmlFrame

# Importing the parse_html_to_form function and the template data loader
from html_parser import parse_html_to_form
from template_data import load_templates

# Load templates from JSON or default data
template_data = load_templates()


class HTMLPreviewTool(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("HTML Preview Tool")
        self.geometry("1633x768")

        # Create frames for the layout
        self.html_frame = tk.Frame(self)
        self.options_frame = tk.Frame(self)
        self.preview_frame = tk.Frame(self)

        # Grid layout for the frames
        self.html_frame.grid(row=0, column=0, sticky="nsew")
        self.options_frame.grid(row=0, column=1, sticky="nsew")
        self.preview_frame.grid(row=0, column=2, sticky="nsew")

        # Configure the root window grid to allow expansion
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # HTML Text Panel (Left)
        self.html_code_label = tk.Label(self.html_frame, text="HTML Code")
        self.html_code_label.pack(anchor="nw")

        self.html_code_text = scrolledtext.ScrolledText(
            self.html_frame,
            wrap=tk.WORD,
            width=90,
            height=30,
        )
        self.html_code_text.pack(fill="both", expand=True)
        self.html_code_text.bind("<<Modified>>", self.update_preview)

        # Options Panel (Center)
        self.options_label = tk.Label(
            self.options_frame, text="Pre-designed HTML Chunks"
        )
        self.options_label.pack(anchor="nw", padx=10)

        self.template_vars = {}
        for x in template_data:
            for key in x.keys():
                var = tk.BooleanVar()
                chk = tk.Checkbutton(
                    self.options_frame,
                    text=key,
                    variable=var,
                    command=self.update_preview,
                )
                chk.pack(anchor="w", padx=10)
                self.template_vars[key] = var

        self.add_selected_button = tk.Button(
            self.options_frame, text="Add Selected", command=self.add_selected_templates
        )
        self.add_selected_button.pack(pady=10)

        self.compile_button = tk.Button(
            self.options_frame, text="Compile", command=self.compile_html
        )
        self.compile_button.pack(pady=10)

        # Preview Panel (Right)
        self.preview_label = tk.Label(self.preview_frame, text="Preview")
        self.preview_label.pack(anchor="nw")

        self.preview_html = HtmlFrame(self.preview_frame)
        self.preview_html.pack(fill="both", expand=True, padx=10, pady=10)

    def add_new_chunk(self):
        self.html_code_text.insert(tk.END, "\n")

    def add_selected_templates(self):
        for name, var in self.template_vars.items():
            if var.get():
                # Find the template with the selected name
                for template in template_data:
                    if name in template:
                        self.html_code_text.insert(tk.END, template[name] + "\n")
        self.update_preview()

    def update_preview(self, event=None):
        self.html_code_text.edit_modified(False)
        html_code = self.html_code_text.get("1.0", tk.END)
        self.preview_html.load_html(html_code)

    def compile_html(self):
        html_code = self.html_code_text.get("1.0", tk.END)
        file_name = askstring("Save File", "Enter file name (without extension):")
        parse_html_to_form(html_code, file_name)


if __name__ == "__main__":
    app = HTMLPreviewTool()
    app.mainloop()

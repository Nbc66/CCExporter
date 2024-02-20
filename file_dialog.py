import tkinter as tk
from tkinter import ttk, filedialog
import vdf_to_json
import webbrowser
import sys, os
import compile_vdf

class GUI:
    def __init__(self):
        self.entry1 = None
        self.entry2 = None
        self.format_var = None
        self.result_label = None
        self.format_combobox = None
        self.entry2_button = None
        self.format_label = None
        self.override_var = None
        self.override_checkbox = None
        self.compile_check = None

    def update_combobox_based_on_file_format(self, file_path):
        # Update combobox based on the selected file's format
        if file_path.lower().endswith(".json"):
            self.format_combobox.set("VDF")
        elif file_path.lower().endswith((".txt", ".vdf")):
            self.format_combobox.set("JSON")

    def on_button_click(self):
        input_value1 = self.entry1.get()
        input_value2 = self.entry2.get()
        selected_format = self.format_var.get()
        #self.result_label.config(text=f"Input 1: {input_value1}, Input 2: {input_value2}, Format: {selected_format}")
        if(selected_format == "JSON"):
            output_path = vdf_to_json.cc_txt_to_json_dump(input_value1,input_value2)
        elif(selected_format == "VDF"):
            output_path = vdf_to_json.json_to_vdf_file(input_value1,input_value2)
            #compile into .dat file if we check the box
            if self.compile_check.get():
                cc_data:bytes = None
                dat_filename:str = None
                if input_value2 != "":
                    cc_data = compile_vdf.compile(input_value2)
                    dat_filename = input_value2
                else:
                    cc_data = compile_vdf.compile(input_value1)
                    dat_filename = input_value1
            with open(dat_filename.replace(".json",".dat"),"wb") as fp:
                fp.truncate()
                fp.write(cc_data)
                fp.close()
            webbrowser.open(dat_filename.replace(".json",".dat"))
            
        webbrowser.open(output_path)

        #self.result_label.config(text=f"Input 1: {input_value1}, Input 2: {input_value2}, Format: {selected_format}")

    def open_file_dialog(self, entry_widget: tk.Entry, override: bool = False):
        if override:
            # When override is True, open a file dialog for creating a file of the opposite format or selecting a file
            opposite_format = "VDF" if self.format_var.get() == "JSON" else "JSON"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json" if opposite_format == "VDF" else ".vdf",
                filetypes=[("JSON File", ".json"), ("VDF File", ".txt .vdf")] if opposite_format == "VDF" else [("VDF File", ".txt .vdf"), ("JSON File", ".json")],
                title=f"Select/Create " + ".json" if opposite_format == "JSON" else ".vdf" + " formatted file"
            )
        else:
            # When override is False, open a file dialog based on the current format_var
            if self.format_var.get() == "VDF":
                file_path = filedialog.askopenfilename(filetypes=[("JSON File", ".json")], title="Select JSON formatted file")
            elif self.format_var.get() == "JSON":
                file_path = filedialog.askopenfilename(filetypes=[("VDF File", ".txt .vdf")], title="Select VDF formatted file")

        if file_path and override == False:
            self.update_combobox_based_on_file_format(file_path)

        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

    def on_checkbox_click(self):
        override_output_enabled = self.override_var.get()
        self.entry2.config(state=tk.NORMAL if override_output_enabled else tk.DISABLED)
        self.entry2_button.config(state=tk.NORMAL if override_output_enabled else tk.DISABLED)

    def start_gui(self):
        # Create the main window
        window = tk.Tk()
        window.title("CC to JSON")

        style = ttk.Style()
        style.theme_use('clam')

        if getattr(sys, 'frozen', False):
            # Set a small icon for the window (replace "your_icon.ico" with the path to your icon file)
            window.iconbitmap(os.path.join(sys._MEIPASS,"icon\convert.ico"))
        else:
            window.iconbitmap("icon\convert.ico")

        # Disable window resizing
        window.resizable(width=False, height=False)

        # Remove maximize button
        window.attributes('-topmost', 1)
        window.attributes('-topmost', 0)

        # Create entry widgets for input
        entry1_label = tk.Label(window, text="Input File")
        entry1_label.grid(row=0, column=0, padx=5, pady=5)

        self.entry1 = tk.Entry(window)
        self.entry1.grid(row=0, column=1, padx=5, pady=5)

        entry2_label = tk.Label(window, text="Override File Output")
        entry2_label.grid(row=1, column=0, padx=5, pady=5)

        self.entry2 = tk.Entry(window, state=tk.DISABLED)  # Initially disabled
        self.entry2.grid(row=1, column=1, padx=5, pady=5)

        # Dropdown list (combobox) for file format selection
        self.format_var = tk.StringVar()
        self.format_label = tk.Label(window, text="Convert To:")
        self.format_label.grid(row=2, column=0, padx=5, pady=5)

        self.format_combobox = ttk.Combobox(window, textvariable=self.format_var, values=["JSON", "VDF"])
        self.format_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.format_combobox.set("JSON")  # Set the default selection

        # Checkbox for overriding output
        self.override_var = tk.IntVar()
        self.override_checkbox = tk.Checkbutton(window, text="Override Output", variable=self.override_var,
                                                 command=self.on_checkbox_click)
        self.override_checkbox.grid(row=3, column=0, columnspan=2, pady=5)

        self.compile_check = tk.IntVar()
        self.compile_checkbox = tk.Checkbutton(window, text="Compile captions", variable=self.compile_check)
        self.compile_checkbox.grid(row=3, column=1, columnspan=2, pady=5)

        # Create buttons for opening file dialogs
        entry1_button = tk.Button(window, text="Open File Dialog", command=lambda: self.open_file_dialog(self.entry1))
        entry1_button.grid(row=0, column=2, padx=5, pady=5)

        self.entry2_button = tk.Button(window, text="Open File Dialog",
                                       command=lambda: self.open_file_dialog(self.entry2, override=True))
        self.entry2_button.grid(row=1, column=2, padx=5, pady=5)
        self.entry2_button.config(state=tk.DISABLED)  # Initially disabled

        # Create a button
        button = tk.Button(window, text="Convert", command=self.on_button_click)
        button.grid(row=4, column=0, columnspan=2, pady=10)

        # Create a label to display the result
        self.result_label = tk.Label(window, text="")
        self.result_label.grid(row=5, column=0, columnspan=2)

        # Start the main event loop
        window.mainloop()
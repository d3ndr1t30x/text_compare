import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class TextFileComparerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Comparer")
        self.root.geometry("800x600")

        # Left pane for reference file
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.left_text = tk.Text(self.left_frame, wrap=tk.WORD)
        self.left_text.pack(fill=tk.BOTH, expand=True)
        
        self.upload_left_button = tk.Button(self.left_frame, text="Upload Reference Text File", command=self.upload_left_file)
        self.upload_left_button.pack(pady=5)
        
        # Right pane for file to compare
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.right_text = tk.Text(self.right_frame, wrap=tk.WORD)
        self.right_text.pack(fill=tk.BOTH, expand=True)

        self.upload_right_button = tk.Button(self.right_frame, text="Upload Text File to Compare", command=self.upload_right_file)
        self.upload_right_button.pack(pady=5)

        # Bottom pane for matched lines
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.match_label = tk.Label(self.bottom_frame, text="Matching Lines:")
        self.match_label.pack(anchor=tk.W)

        # Table to display matching lines
        self.match_table = ttk.Treeview(self.bottom_frame, columns=("Line in Reference File", "Line in Comparison File"), show="headings")
        self.match_table.heading("Line in Reference File", text="Reference File Line")
        self.match_table.heading("Line in Comparison File", text="Comparison File Line")
        self.match_table.pack(fill=tk.BOTH, expand=True)

        # Store contents of the files
        self.left_file_lines = set()
        self.right_file_lines = set()

    def upload_left_file(self):
        file_path = filedialog.askopenfilename(title="Select Reference Text File", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as f:
                # Load lines from the reference file, stripping extra whitespace
                self.left_file_lines = {line.strip() for line in f if line.strip()}
                # Display content in the left text pane
                self.left_text.delete(1.0, tk.END)
                self.left_text.insert(tk.END, "\n".join(self.left_file_lines))
            # Clear previous matching results
            self.clear_match_table()

    def upload_right_file(self):
        file_path = filedialog.askopenfilename(title="Select Comparison Text File", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as f:
                # Load lines from the comparison file, stripping extra whitespace
                self.right_file_lines = {line.strip() for line in f if line.strip()}
                # Display content in the right text pane
                self.right_text.delete(1.0, tk.END)
                self.right_text.insert(tk.END, "\n".join(self.right_file_lines))
            # Find matches
            self.find_matches()

    def find_matches(self):
        # Clear previous matching results
        self.clear_match_table()

        # Find intersection of the two sets to identify matching lines
        matching_lines = self.left_file_lines.intersection(self.right_file_lines)

        # Display matching lines in the table
        for line in matching_lines:
            self.match_table.insert("", tk.END, values=(line, line))

        if not matching_lines:
            messagebox.showinfo("No Matches", "No matching lines found between the two files.")

    def clear_match_table(self):
        # Clear the match table
        for row in self.match_table.get_children():
            self.match_table.delete(row)

# Initialize Tkinter
root = tk.Tk()
app = TextFileComparerApp(root)
root.mainloop()

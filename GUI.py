import tkinter as tk
from tkinter import messagebox, Menu, filedialog, scrolledtext
from concurrent.futures import ThreadPoolExecutor
import threading
import urllib.parse
from Crawler import crawl

class CrawlerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Web Crawler")

        # Initialize menu bar
        self.menu_bar = Menu(master)
        master.config(menu=self.menu_bar)

        # File menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Export to Text", command=self.export_to_text)
        self.file_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Create labels and entries for URL and Depth
        self.label_url = tk.Label(master, text="Starting URL:")
        self.label_url.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_url = tk.Entry(master, width=50)
        self.entry_url.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        self.label_depth = tk.Label(master, text="Depth:")
        self.label_depth.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_depth = tk.Entry(master, width=10)
        self.entry_depth.grid(row=1, column=1, padx=5, pady=5)

        # Create Start Crawling button
        self.btn_crawl = tk.Button(master, text="Start Crawling", command=self.start_crawling)
        self.btn_crawl.grid(row=1, column=2, padx=5, pady=5)

        # Create a scrolled text area for output
        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.text_area.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Configure row and column resizing
        for i in range(3):
            master.grid_rowconfigure(i, weight=1)
        for j in range(3):
            master.grid_columnconfigure(j, weight=1)
    def export_to_text(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w') as file:
                lines = self.text_area.get(1.0, tk.END).split('\n')
                for line in lines:
                    file.write(line.strip() + '\n')

    def start_crawling(self):
        start_url = self.entry_url.get()
        depth = int(self.entry_depth.get())

        if not start_url:
            messagebox.showerror("Error", "Please enter a starting URL.")
            return

        if depth <= 0:
            messagebox.showerror("Error", "Please enter a valid depth (greater than 0).")
            return

        self.text_area.delete(1.0, tk.END)  # Clear previous output

        visited = set()
        output_lock = threading.Lock()

        # Extract domain from starting URL
        domain = urllib.parse.urlparse(start_url).netloc

        # Using ThreadPoolExecutor for concurrent crawling
        with ThreadPoolExecutor(max_workers=10) as executor:
            crawl_result = crawl(start_url, domain, depth, visited, output_lock)
            self.text_area.insert(tk.END, crawl_result)

def main():
    root = tk.Tk()
    app = CrawlerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
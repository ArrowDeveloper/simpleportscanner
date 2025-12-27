import socket
import customtkinter as ctk
from concurrent.futures import ThreadPoolExecutor
import queue

class PortScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner")

        self.exec = ThreadPoolExecutor(max_workers=100)
        self.q = queue.Queue()

        self.check_queue()

        ctk.set_appearance_mode("dark")    
        ctk.set_default_color_theme("blue")

        self.GUI()

    def GUI(self):
        Hlabel = ctk.CTkLabel(self.root, text="HOST: ")
        Hlabel.grid(row=0,column=0)

        Plabel = ctk.CTkLabel(self.root, text="RANGE START: ")
        Plabel.grid(row=1,column=0)

        P1label = ctk.CTkLabel(self.root, text="RANGE END: ")
        P1label.grid(row=2,column=0)

        self.HOST = ctk.CTkEntry(self.root)
        self.HOST.grid(row=0,column=1)

        self.port_range_start = ctk.CTkEntry(self.root)
        self.port_range_start.grid(row=1,column=1)

        self.port_range_end = ctk.CTkEntry(self.root)
        self.port_range_end.grid(row=2,column=1) 

        self.result = ctk.CTkTextbox(self.root,width=250)
        self.result.grid(row=4,column=1)

        submit = ctk.CTkButton(self.root, text="Scan", command=self.threads)
        submit.grid(row=3,column=1)

    def Scanner(self, port):
        host = self.HOST.get().strip()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect((host, port))
            self.q.put(f"PORT OPEN AT {host}:{port}")
        except Exception as e:
            pass
        finally:
            s.close()

    def threads(self):
        try:
            port_rs = int(self.port_range_start.get())
            port_re = int(self.port_range_end.get())
        except ValueError:
            self.result.insert("end", "Enter valid port")
            return
        for port in range(port_rs, port_re + 1):
            self.exec.submit(self.Scanner, port)

    def check_queue(self):
        try:
            while True:
                msg = self.q.get_nowait()
                self.result.insert("end", msg + "\n")
                self.result.see("end")
        except queue.Empty:
            pass

        self.root.after(100, self.check_queue)

if __name__ == "__main__":
    root = ctk.CTk()
    app = PortScanner(root)
    root.mainloop()
import customtkinter as ctk
import socket

root = ctk.CTk()
root.title("Port Scanner")
ctk.set_appearance_mode("dark")    
ctk.set_default_color_theme("blue") 

label = ctk.CTkLabel(root, text="Domain:")
label.grid(column=0,row=0)

label1 = ctk.CTkLabel(root, text="Port: ")
label1.grid(column=0,row=1,sticky="e")

domain = ctk.CTkEntry(root)
domain.grid(column=1,row=0)

port = ctk.CTkEntry(root)
port.grid(column=1, row=1)

result = ctk.CTkLabel(root, text=" ")
result.grid(column=1,row=3)

def portscanner():
    domain1 = domain.get().strip()
    try:
        port1 = int(port.get().strip())
    except ValueError:
        result.configure(text="Please enter valid port!")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.connect((domain1, port1))
            result.configure(text=f"Port is open at {domain1}:{port1}")
            s.close()
        except Exception as e:
            result.configure(text="Port is not open")
            s.close()

button = ctk.CTkButton(root, text="Search", command=portscanner)
button.grid(column=1,row=2)

root.mainloop()
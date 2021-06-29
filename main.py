import tkinter as tk
import subprocess
from datetime import datetime


#Creating the user interface window
sharedfolders_app = tk.Tk()
sharedfolders_app.rowconfigure([0,1,2,3,4,5,6,7,8], weight=1)
sharedfolders_app.columnconfigure([0,1], weight=1)
sharedfolders_app.title("Disable Shared Folders Remotely - Performance Testing Team")

label_explanation1 = tk.Label(text="This app will stop the shared C$ and D$ folders informed in the servers list.")
label_explanation1.grid(row=0, column=0, sticky="nsew", columnspan=2)

label_explanation2 = tk.Label(text="You need to provide a list named Servers.txt with the servers")
label_explanation2.grid(row=1, column=0, sticky="nsew", columnspan=2)

label_explanation3 = tk.Label(text="This list must be in the the same folder that contains this program")
label_explanation3.grid(row=2, column=0, sticky="nsew", columnspan=2)

label_explanation3 = tk.Label(text="A message below 'Disable Shared Folders' button will be displayed when completed")
label_explanation3.grid(row=3, column=0, sticky="nsew", columnspan=2)

#label_input= tk.Label(text="Please inform the folders you want to stop sharing with space between them:")
#label_input.grid(row=3, column=0, sticky="nse")

#folders_names_box = tk.Entry(width=50)
#folders_names_box.grid(row=3, column=1)


def disable_shared_folders():
    servers = open('Servers.txt', 'r')
    servers_str = servers.readlines()
    #folders_names = folders_names_box.get()
    #folders_names_list = folders_names.split(" ")
    with open("Log.txt", "w") as program_output:
        now = datetime.now().strftime("%Y/%B/%d %H:%M:%S")
        program_output.write(f"{now}\r\n")
        for server in servers_str:
            if "\n" in server:
                server = server[0:-1]
                program_output.write(f"{server}\r\n")
            net_view_output = subprocess.run(["net", "view", f"\\\\{server}", "/all"], universal_newlines=True, stdout=subprocess.PIPE)
            program_output.write(net_view_output.stdout)
            lines = net_view_output.stdout.splitlines()
            for line in lines:
                if "C$" in line and "share" in line:
                    try:
                        net_share_output = subprocess.run(["net", "share", "C$", f"\\\\{server}", "/delete"], universal_newlines=True, stdout=subprocess.PIPE)
                        #net_share_output = subprocess.run(["net", "view", f"\\\\{server}", "/all"], universal_newlines=True, stdout=subprocess.PIPE)
                        program_output.write(net_share_output.stdout)
                        net_share_output_lines = net_share_output.stdout.splitlines()
                    except:
                        print(f"Error when deleting C$ folder from {server}")
                if "D$" in line and "share" in line:
                    try:
                        net_share_output = subprocess.run(["net", "share", "D$", f"\\\\{server}", "/delete"], universal_newlines = True, stdout = subprocess.PIPE)
                        #net_share_output = subprocess.run(["net", "view", f"\\\\{server}", "/all"], universal_newlines=True, stdout=subprocess.PIPE)
                        program_output.write(net_share_output.stdout)
                        net_share_output_lines = net_share_output.stdout.splitlines()
                    except:
                        print(f"Error when deleting D$ folder from {server}")
    #output = tk.Label(text=f"{folders_names_list} disabled")
    output = tk.Label(text=f"Disabled folders completed, please check Log.txt file")
    output.grid(row=6, column=0, columnspan=2)


button = tk.Button(text="Disable Shared Folders", command=disable_shared_folders)
button.grid(row=5, column=0, columnspan=2)


sharedfolders_app.mainloop()
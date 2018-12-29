import tkinter as tk


class SSHCredentials:
    """ Class responsible for setting SSH credentials """
    __root = None
    __ip = None
    __user = None
    __pwd = None
    __ip_val = None
    __user_val = None
    __pwd_val = None

    @staticmethod
    def prompt_credentials():
        global ssh
        SSHCredentials.__root = tk.Tk()
        SSHCredentials.__root.geometry('300x200')
        SSHCredentials.__root.title('Enter your SSH credentials')
        # Frame for window margin
        parent = tk.Frame(SSHCredentials.__root, padx=10, pady=10)
        parent.pack(fill=tk.BOTH, expand=True)
        # Entries with not shown text
        SSHCredentials.__ip = SSHCredentials.__make_entry(parent, "IP address:", 16)
        SSHCredentials.__user = SSHCredentials.__make_entry(parent, "Username:", 16)
        SSHCredentials.__pwd = SSHCredentials.__make_entry(parent, "Password:", 16, show="*")
        # Button to attempt to login
        b = tk.Button(parent, borderwidth=4, text="Enter", width=10, pady=8, command=SSHCredentials.__submit)
        b.pack(side=tk.BOTTOM)
        SSHCredentials.__ip.focus()
        SSHCredentials.__user.bind('<Return>', SSHCredentials.__enter_sumbit)
        SSHCredentials.__pwd.bind('<Return>', SSHCredentials.__enter_sumbit)
        parent.focus_force()
        parent.mainloop()
        if not SSHCredentials.__ip_val or not SSHCredentials.__user_val or not SSHCredentials.__pwd_val:
            return None
        return SSHCredentials.__ip_val, SSHCredentials.__user_val, SSHCredentials.__pwd_val

    @staticmethod
    def __enter_sumbit(event):
        SSHCredentials.__submit()

    @staticmethod
    def __submit():
        SSHCredentials.__ip_val = SSHCredentials.__ip.get()
        SSHCredentials.__user_val = SSHCredentials.__user.get()
        SSHCredentials.__pwd_val = SSHCredentials.__pwd.get()
        SSHCredentials.__root.destroy()

    @staticmethod
    def __make_entry(parent, caption, width=None, **options):
        tk.Label(parent, text=caption).pack(side=tk.TOP)
        entry = tk.Entry(parent, **options)
        if width:
            entry.config(width=width)
        entry.pack(side=tk.TOP, padx=10, fill=tk.BOTH)
        return entry

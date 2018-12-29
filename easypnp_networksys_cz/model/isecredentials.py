import tkinter as tk


class ISECredentials:
    """ Class responsible for setting ISE credentials """
    __root = None
    __ip = None
    __user = None
    __pwd = None
    __ip_val = None
    __user_val = None
    __pwd_val = None

    @staticmethod
    def prompt_credentials():
        global ise
        ISECredentials.__root = tk.Tk()
        ISECredentials.__root.geometry('300x200')
        ISECredentials.__root.title('Enter your ISE credentials')
        # Frame for window margin
        parent = tk.Frame(ISECredentials.__root, padx=10, pady=10)
        parent.pack(fill=tk.BOTH, expand=True)
        # Entries with not shown text
        ISECredentials.__ip = ISECredentials.__make_entry(parent, "IP address:", 16)
        ISECredentials.__user = ISECredentials.__make_entry(parent, "Username:", 16)
        ISECredentials.__pwd = ISECredentials.__make_entry(parent, "Password:", 16, show="*")
        # Button to attempt to login
        b = tk.Button(parent, borderwidth=4, text="Enter", width=10, pady=8, command=ISECredentials.__submit)
        b.pack(side=tk.BOTTOM)
        ISECredentials.__ip.focus()
        ISECredentials.__user.bind('<Return>', ISECredentials.__enter_sumbit)
        ISECredentials.__pwd.bind('<Return>', ISECredentials.__enter_sumbit)
        parent.focus_force()
        parent.mainloop()
        if not ISECredentials.__ip_val or not ISECredentials.__user_val or not ISECredentials.__pwd_val:
            return None
        return ISECredentials.__ip_val, ISECredentials.__user_val, ISECredentials.__pwd_val

    @staticmethod
    def __enter_sumbit(event):
        ISECredentials.__submit()

    @staticmethod
    def __submit():
        ISECredentials.__ip_val = ISECredentials.__ip.get()
        ISECredentials.__user_val = ISECredentials.__user.get()
        ISECredentials.__pwd_val = ISECredentials.__pwd.get()
        ISECredentials.__root.destroy()

    @staticmethod
    def __make_entry(parent, caption, width=None, **options):
        tk.Label(parent, text=caption).pack(side=tk.TOP)
        entry = tk.Entry(parent, **options)
        if width:
            entry.config(width=width)
        entry.pack(side=tk.TOP, padx=10, fill=tk.BOTH)
        return entry

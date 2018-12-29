import tkinter as tk


class UserCredentials:
    """ Class responsible for setting user credentials """
    __root = None
    __user = None
    __pwd = None
    __user_val = None
    __pwd_val = None

    @staticmethod
    def prompt_credentials():
        global user
        UserCredentials.__root = tk.Tk()
        UserCredentials.__root.geometry('300x160')
        UserCredentials.__root.title('Enter your credentials')
        # Frame for window margin
        parent = tk.Frame(UserCredentials.__root, padx=10, pady=10)
        parent.pack(fill=tk.BOTH, expand=True)
        # Entries with not shown text
        UserCredentials.__user = UserCredentials.__make_entry(parent, "Username:", 16)
        UserCredentials.__pwd = UserCredentials.__make_entry(parent, "Password:", 16, show="*")
        # Button to attempt to login
        b = tk.Button(parent, borderwidth=4, text="Login", width=10, pady=8, command=UserCredentials.__submit)
        b.pack(side=tk.BOTTOM)
        UserCredentials.__user.focus()
        UserCredentials.__pwd.bind('<Return>', UserCredentials.__enter_sumbit)
        parent.focus_force()
        parent.mainloop()
        if not UserCredentials.__user_val or not UserCredentials.__pwd_val:
            return None
        return UserCredentials.__user_val, UserCredentials.__pwd_val

    @staticmethod
    def __enter_sumbit(event):
        UserCredentials.__submit()

    @staticmethod
    def __submit():
        UserCredentials.__user_val = UserCredentials.__user.get()
        UserCredentials.__pwd_val = UserCredentials.__pwd.get()
        UserCredentials.__root.destroy()

    @staticmethod
    def __make_entry(parent, caption, width=None, **options):
        tk.Label(parent, text=caption).pack(side=tk.TOP)
        entry = tk.Entry(parent, **options)
        if width:
            entry.config(width=width)
        entry.pack(side=tk.TOP, padx=10, fill=tk.BOTH)
        return entry

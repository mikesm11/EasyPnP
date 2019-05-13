import tkinter as tk


class UserCredentials:
    """ Class responsible for setting user credentials to controller """
    __root = None
    __user = None
    __pwd = None
    __user_val = None
    __pwd_val = None

    @staticmethod
    def prompt_credentials():
        """ Method to display a dialog box for setting user credentials to controller """
        global user
        # Parameters of the dialog box
        UserCredentials.__root = tk.Tk()
        UserCredentials.__root.geometry('300x160')
        UserCredentials.__root.title('Enter your credentials')
        # Frame for the dialog box margin
        parent = tk.Frame(UserCredentials.__root, padx=10, pady=10)
        parent.pack(fill=tk.BOTH, expand=True)
        # Entries for user credentials
        UserCredentials.__user = UserCredentials.__make_entry(parent, "Username:", 16)
        UserCredentials.__pwd = UserCredentials.__make_entry(parent, "Password:", 16, show="*")
        # Button to attempt to login
        b = tk.Button(parent, borderwidth=4, text="Login", width=10, pady=8, command=UserCredentials.__submit)
        # Customize button size by text
        b.pack(side=tk.BOTTOM)
        # First focus to the label for username (you can write immediately after displaying the dialog box)
        UserCredentials.__user.focus()
        # Then bind to the label for username (you can't login using enter without filling in all labels)
        UserCredentials.__pwd.bind('<Return>', UserCredentials.__ent_submit)
        # Focus and display the above defined dialog box
        parent.focus_force()
        parent.mainloop()
        # Returns sent user credentials
        if not UserCredentials.__user_val or not UserCredentials.__pwd_val:
            return None
        return UserCredentials.__user_val, UserCredentials.__pwd_val

    @staticmethod
    def __ent_submit(event):
        """ Local method to bind function """
        UserCredentials.__submit()

    @staticmethod
    def __submit():
        """ Local method to submit button """
        UserCredentials.__user_val = UserCredentials.__user.get()
        UserCredentials.__pwd_val = UserCredentials.__pwd.get()
        # Close the dialog box
        UserCredentials.__root.destroy()

    @staticmethod
    def __make_entry(parent, caption, width=None, **options):
        """ Local method to create labels """
        tk.Label(parent, text=caption).pack(side=tk.TOP)
        entry = tk.Entry(parent, **options)
        if width:
            entry.config(width=width)
        entry.pack(side=tk.TOP, padx=10, fill=tk.BOTH)
        return entry

import tkinter as tk


class ISECredentials:
    """ Class responsible for setting user credentials to Cisco ISE """
    __root = None
    __ip = None
    __user = None
    __pwd = None
    __ip_val = None
    __user_val = None
    __pwd_val = None

    @staticmethod
    def prompt_credentials():
        """ Method to display a dialog box for setting user credentials to Cisco ISE """
        global ise
        # Parameters of the dialog box
        ISECredentials.__root = tk.Tk()
        ISECredentials.__root.geometry('300x200')
        ISECredentials.__root.title('Enter your ISE credentials')
        # Frame for the dialog box margin
        parent = tk.Frame(ISECredentials.__root, padx=10, pady=10)
        parent.pack(fill=tk.BOTH, expand=True)
        # Entries for user credentials
        ISECredentials.__ip = ISECredentials.__make_entry(parent, "IP address:", 16)
        ISECredentials.__user = ISECredentials.__make_entry(parent, "Username:", 16)
        ISECredentials.__pwd = ISECredentials.__make_entry(parent, "Password:", 16, show="*")
        # Button to attempt to send
        b = tk.Button(parent, borderwidth=4, text="Enter", width=10, pady=8, command=ISECredentials.__submit)
        # Customize button size by text
        b.pack(side=tk.BOTTOM)
        # First focus to the label for IP address (you can write immediately after displaying the dialog box)
        ISECredentials.__ip.focus()
        # Then bind to the label for username and password (you can't send using enter without filling in all labels)
        ISECredentials.__user.bind('<Return>', ISECredentials.__ent_submit)
        ISECredentials.__pwd.bind('<Return>', ISECredentials.__ent_submit)
        # Focus and display the above defined dialog box
        parent.focus_force()
        parent.mainloop()
        # Returns sent user credentials
        if not ISECredentials.__ip_val or not ISECredentials.__user_val or not ISECredentials.__pwd_val:
            return None
        return ISECredentials.__ip_val, ISECredentials.__user_val, ISECredentials.__pwd_val

    @staticmethod
    def __ent_submit(event):
        """ Local method to bind function """
        ISECredentials.__submit()

    @staticmethod
    def __submit():
        """ Local method to submit button """
        ISECredentials.__ip_val = ISECredentials.__ip.get()
        ISECredentials.__user_val = ISECredentials.__user.get()
        ISECredentials.__pwd_val = ISECredentials.__pwd.get()
        # Close the dialog box
        ISECredentials.__root.destroy()

    @staticmethod
    def __make_entry(parent, caption, width=None, **options):
        """ Local method to create labels """
        tk.Label(parent, text=caption).pack(side=tk.TOP)
        entry = tk.Entry(parent, **options)
        if width:
            entry.config(width=width)
        entry.pack(side=tk.TOP, padx=10, fill=tk.BOTH)
        return entry

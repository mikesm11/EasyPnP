import tkinter as tk


class SSHCredentials:
    """ Class responsible for setting SSH credentials to device """
    __root = None
    __ip = None
    __user = None
    __pwd = None
    __ip_val = None
    __user_val = None
    __pwd_val = None

    @staticmethod
    def prompt_credentials():
        """ Method to display a dialog box for setting SSH credentials to device """
        global ssh
        # Parameters of the dialog box
        SSHCredentials.__root = tk.Tk()
        SSHCredentials.__root.geometry('300x200')
        SSHCredentials.__root.title('Enter your SSH credentials')
        # Frame for the dialog box margin
        parent = tk.Frame(SSHCredentials.__root, padx=10, pady=10)
        parent.pack(fill=tk.BOTH, expand=True)
        # Entries for user credentials
        SSHCredentials.__ip = SSHCredentials.__make_entry(parent, "IP address:", 16)
        SSHCredentials.__user = SSHCredentials.__make_entry(parent, "Username:", 16)
        SSHCredentials.__pwd = SSHCredentials.__make_entry(parent, "Password:", 16, show="*")
        # Button to attempt to send
        b = tk.Button(parent, borderwidth=4, text="Enter", width=10, pady=8, command=SSHCredentials.__submit)
        # Customize button size by text
        b.pack(side=tk.BOTTOM)
        # First focus to the label for IP address (you can write immediately after displaying the dialog box)
        SSHCredentials.__ip.focus()
        # Then bind to the label for username and password (you can't send using enter without filling in all labels)
        SSHCredentials.__user.bind('<Return>', SSHCredentials.__ent_submit)
        SSHCredentials.__pwd.bind('<Return>', SSHCredentials.__ent_submit)
        # Focus and display the above defined dialog box
        parent.focus_force()
        parent.mainloop()
        # Returns sent user credentials
        if not SSHCredentials.__ip_val or not SSHCredentials.__user_val or not SSHCredentials.__pwd_val:
            return None
        return SSHCredentials.__ip_val, SSHCredentials.__user_val, SSHCredentials.__pwd_val

    @staticmethod
    def __ent_submit(event):
        """ Local method to bind function """
        SSHCredentials.__submit()

    @staticmethod
    def __submit():
        """ Local method to submit button """
        SSHCredentials.__ip_val = SSHCredentials.__ip.get()
        SSHCredentials.__user_val = SSHCredentials.__user.get()
        SSHCredentials.__pwd_val = SSHCredentials.__pwd.get()
        # Close the dialog box
        SSHCredentials.__root.destroy()

    @staticmethod
    def __make_entry(parent, caption, width=None, **options):
        """ Local method to create labels """
        tk.Label(parent, text=caption).pack(side=tk.TOP)
        entry = tk.Entry(parent, **options)
        if width:
            entry.config(width=width)
        entry.pack(side=tk.TOP, padx=10, fill=tk.BOTH)
        return entry

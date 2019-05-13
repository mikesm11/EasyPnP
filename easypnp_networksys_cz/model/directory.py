from tkinter import filedialog
import tkinter as tk


class Directory:
    """ Class for managing user directory manipulation """
    @staticmethod
    def pick_file_dir(*file_types):
        """ Method for selecting a file """
        # Creates a new instance
        root = tk.Tk()
        root.withdraw()
        # If the parameter doesn't define a file extension, continue with parameter "all"
        if file_types == ():
            file_types = ('all',)
        # Use the parameter to enable the selection of a defined file extension
        supported = Directory.__get_supported_types(file_types)
        # Runs the dialog box
        file_path = filedialog.askopenfile(filetypes=supported)
        # Returns path to the selected file
        if file_path is None:
            return None
        return file_path.name

    @staticmethod
    def __get_supported_types(*types):
        """ Local method for displaying files with defined file extension (using specified parameter) """
        # Creates empty tuple
        out_types = ()
        for t in types[0]:
            # If parameter is "all" , you can select file with any kind of file extension
            if t == 'all':
                out_types = (('all files', '*.*'),) + out_types
                continue
            # Infills the tuple with files with defined file extension
            desc = t + ' files'
            match = '*.' + t
            out_types = ((desc, match),) + out_types
        # If the tuple is empty, you can select file with any kind of file extension
        if out_types == ():
            out_types = (('all files', '*.*'),)
        # Return the tuple with files with defined file extension
        return out_types

from tkinter import filedialog
import tkinter as tk


class Directory:
    """ Class for managing user directory manipulation """
    @staticmethod
    def pick_file_dir(*file_types):
        root = tk.Tk()
        root.withdraw()
        if file_types == ():
            file_types = ('all',)
        # Supported file types
        supported = Directory.__get_supported_types(file_types)
        file_path = filedialog.askopenfile(filetypes=supported)
        if file_path is None:
            return None
        return file_path.name

    @staticmethod
    def __get_supported_types(*types):
        out_types = ()
        for t in types[0]:
            if t == 'all':
                out_types = (('all files', '*.*'),) + out_types
                continue
            desc = t + ' files'
            match = '*.' + t
            out_types = ((desc, match),) + out_types
        if out_types == ():
            out_types = (('all files', '*.*'),)
        return out_types

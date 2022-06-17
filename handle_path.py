import os


class HandlePath:

    def __init__(self, file_path: str, dir_path: str, out_path: str):
        self.file_path = file_path
        self.dir_path = dir_path
        self.out_path = out_path

    def check_dir(self):
        directory_path = self.dir_path
        out_path = self.out_path

        if directory_path and os.path.isdir(directory_path) and os.path.isdir(out_path):
            pass
        elif directory_path and not os.path.isdir(directory_path):
            raise NotADirectoryError(directory_path)
        elif directory_path and not os.path.isdir(out_path):
            raise NotADirectoryError(out_path)

        else:
            return False

    def check_file_path(self):
        file_path = self.file_path

        if file_path and os.path.isfile(file_path):
            pass
        else:
            raise FileNotFoundError(file_path)
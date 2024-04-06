import os


class ContentsReader:
    def __init__(self, root_folder):
        self.root_folder = root_folder

    def read_all_files(self):
        """
        Reads all files in the given root folder and its subfolders,
        returning the contents of these files in a list of strings.
        """
        file_contents = []
        for root, dirs, files in os.walk(self.root_folder):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as fileToRead:
                        contents = fileToRead.read()
                        file_contents.append(contents)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
        return file_contents

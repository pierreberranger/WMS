

class FileIDGenerator:
    def __init__(self, filename: str):
        self.filename = filename
        # initialisation de vos trucs avec les fichiers

    def __next__(self) -> int:
        with open(self.filename, mode='r') as file_content:
            next_id = int(file_content.readlines()[0]) + 1
        with open(self.filename, mode='w') as file_content:
            file_content.write(f"{next_id}")
        return next_id

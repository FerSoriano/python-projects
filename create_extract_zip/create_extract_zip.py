import zipfile
import os
from pathlib import Path
import sys

class Zip():
    def __init__(self, option: str, path: str) -> None:
        """
        option: create or extract \n
        path: Path where is the file / directory
        """
        self.option = option
        self.path = path

    def validar_directorio(self) -> bool:
        """
        Return true if directory.
        """
        if os.path.isdir(self.path):
            self.name = str(Path(self.path)) + '_zip.zip'
            self.files = os.listdir(self.path)
            return True
        else:
            self.name = str(Path(self.path)) + '.zip'
            return False
    
    def crear_extract_zip(self) -> None:
        try:
            if self.option == 'create':
                print("Creating ZIP...")
                if self.validar_directorio():
                    with zipfile.ZipFile(file=self.name, mode='w') as zip_file:
                        for file in self.files:
                            full_name = os.path.join(self.path, file)
                            zip_file.write(full_name)
                else:
                    with zipfile.ZipFile(file=self.name, mode='w') as zip_file:
                        zip_file.write(self.path) 
                print('✅ Done! The ZIP file was created in the same path.')
                    
            elif self.option == 'extract':
                print("Extracting ZIP...")
                with zipfile.ZipFile(file=self.path, mode='r') as zip_file:
                    zip_file.extractall(str(Path(self.path)) + '.zip')
                print('✅ Done! The ZIP file was extracted in the same path.')

            else:
                print("❌ Invalid option. Make sure to select 'extract' or 'create'. Try again.")
            
        except:
            print("❌ File / directory not found. Try again.")
            

if __name__ == "__main__":
    try:
        option = sys.argv[1]
        path = sys.argv[2]
        zip_file = Zip(option=option, path=path)
        zip_file.crear_extract_zip()
    except:
        print("⚠️  Please add the parameters Option and Path:\nOption: create or extract \nPath: where the file / directory is located")

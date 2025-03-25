import os,json

class Config:
    def __init__(self,config_file='config.json'):
        self.config_file = config_file  
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                self.config = json.load(file)
        else:
            raise FileNotFoundError(f"Configuration file {self.config_file} not found.")
        
    def get(self, key):
        return self.config.get(key)
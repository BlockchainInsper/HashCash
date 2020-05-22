import pandas as pd
import uuid
import datetime

class HashReport:

    def __init__(self):
        self.pd = pd
        self.create_df_time()
        self.create_df_difficulty()
        self.create_df_user()
    
    def create_df_user(self):
        data = {'id': [], 'username': [], 'password': []}
        self.df_user = self.pd.DataFrame(data)

    def create_df_time(self):
        data = {'id': [], 'time': [], 'timestamp': []}
        self.df_time = self.pd.DataFrame(data)

    def create_df_difficulty(self):
        data = {'id': [], 'difficulty': [], 'timestamp': []}
        self.df_difficulty = self.pd.DataFrame(data)

    def insert_time(self, time):
        self.df_time = self.df_time.append({
            'id': str(uuid.uuid4()),
            'time': time,
            'timestamp': str(datetime.datetime.utcnow())
        }, ignore_index=True)

    def insert_difficulty(self, difficulty):
        self.df_difficulty = self.df_difficulty.append({
            'id': str(uuid.uuid4()),
            'difficulty': str(difficulty),
            'timestamp': str(datetime.datetime.utcnow())
        }, ignore_index=True)

    def insert_user(self, username, password, salt):
        self.df_user = self.df_user.append({
            'id': str(uuid.uuid4()),
            'username': str(username),
            'password': str(password),
            'salt': str(salt)
        }, ignore_index=True)
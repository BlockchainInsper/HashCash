import pandas as pd
import uuid
import datetime

class HashReport:

    def __init__(self):
        self.pd = pd
        self.create_df_time()
        self.create_df_difficulty()

    def create_df_time(self):
        data = {'id': [], 'time': [], 'timestamp': []}
        self.df_time = self.pd.DataFrame(data)

    def create_df_difficulty(self):
        data = {'id': [], 'difficulty': [], 'timestamp': []}
        self.df_difficulty = self.pd.DataFrame(data)

    def insert_time(self, time):
        self.df_time = self.df_time.append({
            'id': str(uuid.uuid4()),
            'time': str(time),
            'timestamp': str(datetime.datetime.utcnow())
        }, ignore_index=True)

    def insert_difficulty(self, difficulty):
        self.df_difficulty = self.df_difficulty.append({
            'id': str(uuid.uuid4()),
            'difficulty': str(difficulty),
            'timestamp': str(datetime.datetime.utcnow())
        }, ignore_index=True)
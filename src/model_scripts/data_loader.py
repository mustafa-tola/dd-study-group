# modules/data_loader.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import asyncio
from utils import Utils


class DataLoader:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.data = None
        self.X_train = None
        self.X_test = None

    async def load_data(self):
        """Simulate an asynchronous data loading operation."""
        loop = asyncio.get_event_loop()
        self.data = await loop.run_in_executor(None, pd.read_csv, self.csv_path)
        print("Data loaded successfully.")

    async def preprocess_data(self):
        """Preprocess the data (encoding, scaling)."""
        await self.load_data()
        print("Initial Data Preview:")
        print(self.data.head())

        label_encoder = LabelEncoder()
        self.data['Skill_Level'] = label_encoder.fit_transform(self.data['Skill_Level'])
        self.data['Preferred_Group_Size'] = label_encoder.fit_transform(self.data['Preferred_Group_Size'])

        scaler = StandardScaler()
        numeric_features = ['Latitude', 'Longitude']
        self.data[numeric_features] = scaler.fit_transform(self.data[numeric_features])
        
        await Utils.save_scaler(scaler,"../model/scaler.joblib")
        self.data = self.data.drop("UserID", axis=1)
        print("Processed Data Preview:")
        print(self.data.head())

    async def split_data(self):
        """Split data into training and testing sets."""
        await self.preprocess_data()
        self.X_train, self.X_test, _, _ = train_test_split(self.data, [0] * len(self.data), test_size=0.20, random_state=42)
        print("Training Data Preview:")
        print(self.X_train.head())
        return self.X_train, self.X_test
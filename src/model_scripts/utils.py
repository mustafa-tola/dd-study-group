# modules/utils.py

import asyncio
import joblib

class Utils:
    @staticmethod
    async def save_to_csv(X_train, output_path):
        """Save the results asynchronously to a CSV file."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, X_train.to_csv, output_path, ",")
        print(f"Clustered data saved to {output_path}")

    @staticmethod
    async def save_model(model, path):
        joblib.dump(model, path)
    
    @staticmethod
    async def save_scaler(scaler,path):
        joblib.dump(scaler,path)
    
    @staticmethod
    async def load_scaler(path):
        joblib.load(path)
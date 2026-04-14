<<<<<<< HEAD
# Crop Disease Detection Web App

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate`
3. Install: `pip install -r requirements.txt`
4. Download PlantVillage dataset to `dataset/` folder
5. Train model: `python train_model.py`
6. Setup MySQL database (see below)
7. Run: `python app.py`

## Database Setup
```sql
CREATE DATABASE crop_disease_db;
USE crop_disease_db;
CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_filename VARCHAR(255),
    disease VARCHAR(100),
    confidence FLOAT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Dataset
Download PlantVillage dataset from Kaggle: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
Extract to `dataset/plantvillage_dataset/`
=======
# Crop-Disease-Detection
>>>>>>> dd1c27dfc4a0b6dea3a63c4ed2b3c02579c14877

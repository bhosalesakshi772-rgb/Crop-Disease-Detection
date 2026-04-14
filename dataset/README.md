# Dataset Instructions

1. Download PlantVillage Dataset from Kaggle:
   https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset

2. Extract to: `crop-disease-detection/dataset/plantvillage_dataset/color/`

3. Expected structure:
   ```
   dataset/
   └── plantvillage_dataset/
       └── color/
           ├── Apple___Apple_scab/
           ├── Apple___Black_rot/
           ├── ... (38 classes total)
   ```

4. Run training: `python train_model.py`


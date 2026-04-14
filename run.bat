@echo off
echo Setting up Crop Disease Detection App...
echo.

REM Create virtual environment if not exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Create necessary directories
mkdir model 2>nul
mkdir uploads 2>nul
mkdir dataset 2>nul

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Download PlantVillage dataset: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
echo 2. Extract to: dataset/plantvillage_dataset/color/
echo 3. Run: python train_model.py
echo 4. Setup MySQL database (see README.md)
echo 5. Run: python app.py
echo.
pause


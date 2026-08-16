@echo off
chcp 65001 >nul
echo ========================================
echo   СБОРКА МАТЕМАТИЧЕСКОГО ТРЕНАЖЕРА
echo ========================================

:: Устанавливаем нужные пакеты
pip install pyinstaller Pillow

:: Сборка с добавлением папки assets и скрытых импортов Pillow
pyinstaller --onefile --windowed --name MathTrainer ^
    --add-data "assets;assets" ^
    --hidden-import PIL ^
    --hidden-import PIL._imaging ^
    main.py

echo.
echo ========================================
echo   ГОТОВО! Файл MathTrainer.exe в папке dist
echo ========================================
pause
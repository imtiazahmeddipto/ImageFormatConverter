# Image Format Converter

A simple desktop tool to convert images between formats (JPG, PNG, DDS, BMP, TIFF) with an easy-to-use GUI.

## Folder Structure

- dist/ # Final executable is here: app.exe
- app.py # Python source code (optional if running exe)
- app.spec # PyInstaller build file (optional)
- build/ # Temporary PyInstaller folder (can be ignored)

markdown
Copy code

## How to Run

1. Go to the `dist/` folder.
2. Double-click `app.exe` to open the application.
3. Use the GUI to convert images:

   - **Select Images** → choose the images you want to convert  
   - **Select Output Folder** → choose where to save the converted files  
   - **Target Format** → pick the output format (PNG, JPG, BMP, TIFF)  
   - **Delete Original** → check this box if you want to remove the original files after conversion  
   - **Convert** → click to start conversion. The progress bar shows the conversion status

**Note:** No Python installation is required. Just run `app.exe` from the `dist` folder.

## Supported Formats

- PNG
- JPG / JPEG
- BMP
- TIFF
- DDS

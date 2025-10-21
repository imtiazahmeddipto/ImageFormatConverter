import os
from tkinter import Tk, Button, Label, filedialog, StringVar, BooleanVar, Checkbutton, ttk, Text, Scrollbar, END
from PIL import Image
import imageio.v3 as iio

def select_files():
    files = filedialog.askopenfilenames(title="Select images")
    if files:
        global selected_files_list
        selected_files_list = list(files)
        selected_files.set(f"{len(files)} file(s) selected")

def select_output_folder():
    folder = filedialog.askdirectory(title="Select output folder")
    if folder:
        output_folder.set(folder)

def detect_format(file):
    ext = os.path.splitext(file)[1].lower()
    if ext in [".jpg", ".jpeg"]:
        return "jpg"
    elif ext == ".png":
        return "png"
    elif ext == ".dds":
        return "dds"
    elif ext == ".bmp":
        return "bmp"
    elif ext == ".tiff":
        return "tiff"
    else:
        return "unknown"

def log_error(message):
    error_box.insert(END, message + "\n")
    error_box.see(END)

def clear_errors():
    error_box.delete(1.0, END)

def convert_images():
    clear_errors()

    if not selected_files_list:
        log_error("No files selected.")
        return
    if not output_folder.get():
        log_error("Select output folder first.")
        return

    delete_original = delete_bool.get()
    out_dir = output_folder.get()
    target = target_format.get().lower()

    progress["value"] = 0
    step = 100 / len(selected_files_list)

    for i, file in enumerate(selected_files_list):
        try:
            src_format = detect_format(file)
            if src_format == target:
                log_error(f"Skipped (same format): {file}")
                continue

            if src_format == "dds":
                arr = iio.imread(file)
                img = Image.fromarray(arr)
            else:
                img = Image.open(file)

            base = os.path.splitext(os.path.basename(file))[0]
            save_path = os.path.join(out_dir, f"{base}.{target}")

            if target in ["jpg", "jpeg"]:
                img = img.convert("RGB")  # remove alpha for JPG

            img.save(save_path)
            print(f"Converted: {file} → {save_path}")

            if delete_original:
                os.remove(file)

        except Exception as e:
            log_error(f"Error converting {file}: {e}")

        progress["value"] += step
        root.update_idletasks()

    progress["value"] = 100
    log_error("Conversion complete.")

# --- GUI ---
root = Tk()
root.title("Image Format Converter")
root.geometry("500x500")

# Error visualizer
Label(root, text="Error / Log Viewer:").pack(pady=(5, 0))
frame_log = ttk.Frame(root)
frame_log.pack(pady=2, fill="both", expand=False)

scrollbar = Scrollbar(frame_log)
scrollbar.pack(side="right", fill="y")

error_box = Text(frame_log, height=6, width=60, wrap="word", yscrollcommand=scrollbar.set, bg="#f8f8f8")
error_box.pack(padx=5, pady=2)
scrollbar.config(command=error_box.yview)

selected_files_list = []
selected_files = StringVar(value="No files selected")
output_folder = StringVar()
target_format = StringVar(value="png")
delete_bool = BooleanVar(value=False)

Label(root, textvariable=selected_files).pack(pady=3)
Label(root, text="Target Format:").pack()
ttk.OptionMenu(root, target_format, "png", "jpg", "jpeg", "bmp", "tiff").pack()

Button(root, text="Select Images", command=select_files).pack(pady=5)
Button(root, text="Select Output Folder", command=select_output_folder).pack(pady=5)
Checkbutton(root, text="Delete original after conversion", variable=delete_bool).pack()

progress = ttk.Progressbar(root, length=400, mode="determinate")
progress.pack(pady=10)

Button(root, text="Convert", command=convert_images).pack(pady=10)

root.mainloop()

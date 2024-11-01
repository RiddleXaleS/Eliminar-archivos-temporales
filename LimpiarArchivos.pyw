import os
import shutil
import stat
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar

def remove_readonly(func, path, excinfo):
    # Cambia los permisos de solo lectura antes de eliminar el archivo
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clean_temp_folder(folder, status_label, deleted_listbox, failed_listbox, open_folder_button):
    # Intenta limpiar la carpeta específica
    if os.path.exists(folder):
        print(f"Limpando la carpeta: {folder}")
        files_to_remove = os.listdir(folder)
        total_files = len(files_to_remove)
        status_label.config(text=f"Limpieza de: {folder} - Total archivos: {total_files}")

        for index, filename in enumerate(files_to_remove):
            file_path = os.path.join(folder, filename)
            try:
                # Actualizar la etiqueta de estado
                status_label.config(text=f"Eliminando: {filename} ({index + 1}/{total_files})")
                
                # Intenta eliminar el archivo
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Eliminado: {file_path}")
                    deleted_listbox.insert(tk.END, filename)  # Agregar a la lista de eliminados
                # Si es un directorio, eliminarlo
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path, onerror=remove_readonly)
                    print(f"Eliminado directorio: {file_path}")
                    deleted_listbox.insert(tk.END, filename)  # Agregar a la lista de eliminados

            except PermissionError:
                print(f"Acceso denegado: {file_path}. Se omitirá.")
                failed_listbox.insert(tk.END, filename)  # Agregar a la lista de fallidos
            except Exception as e:
                print(f"No se pudo eliminar {file_path}: {e}")
                failed_listbox.insert(tk.END, filename)  # Agregar a la lista de fallidos

        messagebox.showinfo("Limpieza completada", f"La carpeta {folder} ha sido limpiada.")
        status_label.config(text="Limpieza completada.")
        open_folder_button.config(state=tk.NORMAL)  # Activar el botón para abrir la carpeta
    else:
        messagebox.showwarning("Carpeta no encontrada", f"La carpeta no existe: {folder}")
        status_label.config(text="Carpeta no encontrada.")

def clean_all_temp_folders(status_label, deleted_listbox, failed_listbox, open_folder_button):
    # Rutas de las carpetas a limpiar
    temp_folders = [
        r"C:\Users\alexl\AppData\Local\Temp",
        r"C:\Windows\Prefetch",
        r"C:\Windows\Temp"
    ]
    
    for folder in temp_folders:
        clean_temp_folder(folder, status_label, deleted_listbox, failed_listbox, open_folder_button)

def open_folder(folder):
    # Abre la carpeta especificada en el explorador de archivos
    os.startfile(folder)

class TempCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Limpiador de Carpetas Temporales")
        self.root.geometry("600x400")

        # Etiqueta para mostrar el estado de limpieza
        self.status_label = tk.Label(root, text="Selecciona una carpeta para limpiar.", bg='white')
        self.status_label.pack(pady=10)

        # Botones para limpiar cada carpeta
        self.clean_temp_button = tk.Button(root, command=lambda: clean_temp_folder(r"C:\Users\alexl\AppData\Local\Temp", self.status_label, self.deleted_listbox, self.failed_listbox, self.open_folder_button), text="Limpiar Temp", bg='gray', fg='white')
        self.clean_temp_button.pack(pady=10)

        self.clean_prefetch_button = tk.Button(root, command=lambda: clean_temp_folder(r"C:\Windows\Prefetch", self.status_label, self.deleted_listbox, self.failed_listbox, self.open_folder_button), text="Limpiar Prefetch", bg='gray', fg='white')
        self.clean_prefetch_button.pack(pady=10)

        self.clean_windows_temp_button = tk.Button(root, command=lambda: clean_temp_folder(r"C:\Windows\Temp", self.status_label, self.deleted_listbox, self.failed_listbox, self.open_folder_button), text="Limpiar Windows Temp", bg='gray', fg='white')
        self.clean_windows_temp_button.pack(pady=10)

        # Botón para limpiar todas las carpetas, ahora en rojo
        self.clean_all_button = tk.Button(root, command=lambda: clean_all_temp_folders(self.status_label, self.deleted_listbox, self.failed_listbox, self.open_folder_button), text="Limpiar Todas", bg='red', fg='white')
        self.clean_all_button.pack(pady=10)

        # Botón para abrir la carpeta
        self.open_folder_button = tk.Button(root, text="Abrir Temp", command=lambda: open_folder(r"C:\Users\alexl\AppData\Local\Temp"), bg='blue', fg='white')
        self.open_folder_button.pack(pady=10)

        # Botón para abrir la carpeta
        self.open_folder_button = tk.Button(root, text="Abrir Prefetch", command=lambda: open_folder(r"C:\Windows\Prefetch"), bg='blue', fg='white')
        self.open_folder_button.pack(pady=10)

        # Botón para abrir la carpeta
        self.open_folder_button = tk.Button(root, text="Abrir Win Temp", command=lambda: open_folder(r"C:\Windows\Temp"), bg='blue', fg='white')
        self.open_folder_button.pack(pady=10)

        # Marco para listas de eliminados y fallidos
        self.list_frame = tk.Frame(root)
        self.list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Lista de archivos eliminados
        self.deleted_listbox = Listbox(self.list_frame, bg='lightgreen')
        self.deleted_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Scrollbar para la lista de eliminados
        self.deleted_scrollbar = Scrollbar(self.list_frame)
        self.deleted_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.deleted_listbox.config(yscrollcommand=self.deleted_scrollbar.set)
        self.deleted_scrollbar.config(command=self.deleted_listbox.yview)

        # Lista de archivos fallidos
        self.failed_listbox = Listbox(self.list_frame, bg='lightcoral')
        self.failed_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Scrollbar para la lista de fallidos
        self.failed_scrollbar = Scrollbar(self.list_frame)
        self.failed_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.failed_listbox.config(yscrollcommand=self.failed_scrollbar.set)
        self.failed_scrollbar.config(command=self.failed_listbox.yview)

if __name__ == "__main__":
    root = tk.Tk()
    app = TempCleanerApp(root)
    root.mainloop()
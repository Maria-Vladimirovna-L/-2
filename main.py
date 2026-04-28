import tkinter as tk
from tkinter import messagebox, Listbox, END
import requests
import json

FAVORITES_FILE = "favorites.json"
current_user_data = None

def load_favorites():
    try:
        with open(FAVORITES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_favorites(favorites):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=2)

def search_user():
    global current_user_data
    username = entry_search.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым!")
        return

    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        response.raise_for_status()
        user_data = response.json()
        display_user(user_data)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка", f"Пользователь не найден или ошибка сети: {e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось обработать данные: {e}")

def display_user(user_data):
    global current_user_data
    listbox_results.delete(0, END)
    info = f"{user_data['login']} ({user_data.get('name', 'Нет имени')})"
    listbox_results.insert(END, info)
    current_user_data = user_data

def add_to_favorites():
    global current_user_data
    if not current_user_data:
        messagebox.showwarning("Ошибка", "Сначала найдите пользователя!")
        return

    favorites = load_favorites()
    if any(u['login'] == current_user_data['login'] for u in favorites):
        messagebox.showinfo("Информация", "Пользователь уже в избранном!")
        return

    favorites.append(current_user_data)
    save_favorites(favorites)
    messagebox.showinfo("Успех", "Пользователь добавлен в избранное!")


# --- GUI ---
root = tk.Tk()
root.title("GitHub User Finder")
root.geometry("500x400")
root.resizable(False, False)

# Поле ввода и кнопка поиска
frame_search = tk.Frame(root)
frame_search.pack(pady=10)
entry_search = tk.Entry(frame_search, width=40)
entry_search.pack(side=tk.LEFT, padx=5)
btn_search = tk.Button(frame_search, text="Поиск", command=search_user)
btn_search.pack(side=tk.LEFT)

# Список результатов
listbox_results = Listbox(root, width=60, height=10)
listbox_results.pack(pady=10)

# Кнопка избранного
btn_fav = tk.Button(root, text="Добавить в избранное", command=add_to_favorites)
btn_fav.pack(pady=5)

root.mainloop()

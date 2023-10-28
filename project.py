import sqlite3
import tkinter as tk
from tkinter import ttk

# Создание подключения к базе данных
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()

# Создание таблицы employees, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        phone TEXT,
        email TEXT,
        salary INTEGER
    )
''')
conn.commit()

# Создание главного окна приложения
root = tk.Tk()
root.title("Список сотрудников компании")

# Создание и настройка виджета Treeview для отображения записей из БД
tree = ttk.Treeview(root, columns=("fullname", "phone", "email", "salary"), show="headings")
tree.heading("fullname", text="ФИО")
tree.heading("phone", text="Телефон")
tree.heading("email", text="Email")
tree.heading("salary", text="Заработная плата")
tree.pack()

# Функция для обновления отображаемых записей в Treeview
def update_tree():
    # Очистка Treeview
    tree.delete(*tree.get_children())
    
    # Запрос всех записей из БД
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    
    # Добавление записей в Treeview
    for row in rows:
        tree.insert("", tk.END, values=row)

# Функция для добавления нового сотрудника
def add_employee():
    fullname = entry_fullname.get()
    phone = entry_phone.get()
    email = entry_email.get()
    salary = entry_salary.get()
    
    # Вставка новой записи в БД
    cursor.execute("INSERT INTO employees (fullname, phone, email, salary) VALUES (?, ?, ?, ?)", (fullname, phone, email, salary))
    conn.commit()
    
    # Обновление отображаемых записей
    update_tree()

# Функция для изменения выбранного сотрудника
def edit_employee():
    selected_item = tree.selection()[0]
    fullname = entry_fullname.get()
    phone = entry_phone.get()
    email = entry_email.get()
    salary = entry_salary.get()
    
    # Обновление выбранной записи в БД
    cursor.execute("UPDATE employees SET fullname=?, phone=?, email=?, salary=? WHERE id=?", (fullname, phone, email, salary, selected_item))
    conn.commit()

    # Обновление отображаемых записей
    update_tree()

# Функция для удаления выбранного сотрудника
def delete_employee():
    selected_item = tree.selection()[0]

    # Удаление выбранной записи из БД
    cursor.execute("DELETE FROM employees WHERE id=?", (selected_item,))
    conn.commit()

    # Обновление отображаемых записей
    update_tree()

# Функция для поиска сотрудников по ФИО
def search_employee():
    search_query = entry_search.get()

    # Очистка Treeview
    tree.delete(*tree.get_children())

    # Запрос записей из БД, соответствующих поисковому запросу
    cursor.execute("SELECT * FROM employees WHERE fullname LIKE ?", ('%' + search_query + '%',))
    rows = cursor.fetchall()

    # Добавление записей в Treeview
    for row in rows:
        tree.insert("", tk.END, values=row)

# Создание и настройка виджетов для ввода данных
frame_input = ttk.Frame(root)
frame_input.pack()

label_fullname = ttk.Label(frame_input, text="ФИО:")
label_fullname.grid(row=0, column=0, padx=5, pady=5)
entry_fullname = ttk.Entry(frame_input)
entry_fullname.grid(row=0, column=1, padx=5, pady=5)

label_phone = ttk.Label(frame_input, text="Телефон:")
label_phone.grid(row=1, column=0, padx=5, pady=5)
entry_phone = ttk.Entry(frame_input)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

label_email = ttk.Label(frame_input, text="Email:")
label_email.grid(row=2, column=0, padx=5, pady=5)
entry_email = ttk.Entry(frame_input)
entry_email.grid(row=2, column=1, padx=5, pady=5)

label_salary = ttk.Label(frame_input, text="Заработная плата:")
label_salary.grid(row=3, column=0, padx=5, pady=5)
entry_salary = ttk.Entry(frame_input)
entry_salary.grid(row=3, column=1, padx=5, pady=5)

# Создание и настройка кнопок для выполнения действий
frame_buttons = ttk.Frame(root)
frame_buttons.pack()

button_add = ttk.Button(frame_buttons, text="Добавить", command=add_employee)
button_add.grid(row=0, column=0, padx=5, pady=5)

button_edit = ttk.Button(frame_buttons, text="Изменить", command=edit_employee)
button_edit.grid(row=0, column=1, padx=5, pady=5)

button_delete = ttk.Button(frame_buttons, text="Удалить", command=delete_employee)
button_delete.grid(row=0, column=2, padx=5, pady=5)

# Создание и настройка виджетов для поиска сотрудников
frame_search = ttk.Frame(root)
frame_search.pack()

label_search = ttk.Label(frame_search, text="Поиск по ФИО:")
label_search.grid(row=0, column=0, padx=5, pady=5)
entry_search = ttk.Entry(frame_search)
entry_search.grid(row=0, column=1, padx=5, pady=5)

button_search = ttk.Button(frame_search, text="Найти", command=search_employee)
button_search.grid(row=0, column=2, padx=5, pady=5)

# Обновление отображаемых записей при запуске приложения
update_tree()

# Запуск главного цикла приложения
root.mainloop()

# Закрытие подключения к базе данных при выходе из приложения
conn.close()
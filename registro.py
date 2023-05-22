import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Crear la conexión a la base de datos
conn = sqlite3.connect('registro_asistencia.db')
c = conn.cursor()

# Crear la tabla "Docente" si no existe
c.execute('''CREATE TABLE IF NOT EXISTS Docente (
                codigo INTEGER PRIMARY KEY,
                nombre TEXT,
                curso TEXT,
                contraseña TEXT
            )''')

# Crear la tabla "RegistroAsistencia" si no existe
c.execute('''CREATE TABLE IF NOT EXISTS RegistroAsistencia (
                codigo INTEGER,
                contraseña TEXT,
                fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (codigo, contraseña) REFERENCES Docente(codigo, contraseña)
            )''')

# Función para agregar un nuevo docente
def agregar_docente():
    def agregar():
        codigo = int(entry_codigo.get())
        nombre = entry_nombre.get()
        curso = entry_curso.get()
        contraseña = entry_contraseña.get()

        # Insertar los datos del docente en la tabla "Docente"
        c.execute("INSERT INTO Docente VALUES (?, ?, ?, ?)", (codigo, nombre, curso, contraseña))
        conn.commit()
        messagebox.showinfo('Éxito', 'Docente agregado correctamente.')
        window_agregar.destroy()

    # Crear ventana para agregar docente
    window_agregar = Toplevel(root)
    window_agregar.title('Agregar Docente')

    label_codigo = Label(window_agregar, text='Código:')
    label_codigo.pack()
    entry_codigo = Entry(window_agregar)
    entry_codigo.pack()

    label_nombre = Label(window_agregar, text='Nombre:')
    label_nombre.pack()
    entry_nombre = Entry(window_agregar)
    entry_nombre.pack()

    label_curso = Label(window_agregar, text='Curso:')
    label_curso.pack()
    entry_curso = Entry(window_agregar)
    entry_curso.pack()

    label_contraseña = Label(window_agregar, text='Contraseña:')
    label_contraseña.pack()
    entry_contraseña = Entry(window_agregar, show='*')
    entry_contraseña.pack()

    btn_agregar = Button(window_agregar, text='Agregar', command=agregar)
    btn_agregar.pack()

# Función para registrar la asistencia
def registrar_asistencia():
    def registrar():
        codigo = int(entry_codigo.get())
        contraseña = entry_contraseña.get()
        # Verificar si el código y la contraseña coinciden con un docente existente
        c.execute("SELECT COUNT(*) FROM Docente WHERE codigo = ? AND contraseña = ?", (codigo, contraseña))
        if c.fetchone()[0] == 0:
            messagebox.showerror('Error', 'Código o contraseña incorrectos.')
            return
        # Insertar el registro de asistencia en la tabla "RegistroAsistencia"
        c.execute("INSERT INTO RegistroAsistencia (codigo, contraseña) VALUES (?, ?)", (codigo, contraseña))
        conn.commit()
        messagebox.showinfo('Éxito', 'Asistencia registrada correctamente.')
        window_registrar.destroy()

    # Crear ventana para registrar asistencia
    window_registrar = Toplevel(root)
    window_registrar.title('Registrar Asistencia')

    label_codigo = Label(window_registrar, text='Código:')
    label_codigo.pack()
    entry_codigo = Entry(window_registrar)
    entry_codigo.pack()

    label_contraseña = Label(window_registrar, text='Contraseña:')
    label_contraseña.pack()
    entry_contraseña = Entry(window_registrar, show='*')
    entry_contraseña.pack()

    btn_registrar = Button(window_registrar, text='Registrar', command=registrar)
    btn_registrar.pack()

# Función para mostrar todos los docentes
def mostrar_docentes():
    c.execute("SELECT * FROM Docente")
    docentes = c.fetchall()

    # Crear ventana para mostrar docentes
    window_mostrar = Toplevel(root)
    window_mostrar.title('Docentes')

    # Crear el Treeview
    tree = ttk.Treeview(window_mostrar, columns=('codigo', 'nombre', 'curso', 'contraseña'), show='headings')
    tree.heading('codigo', text='Código')
    tree.heading('nombre', text='Nombre')
    tree.heading('curso', text='Curso')
    tree.heading('contraseña', text='Contraseña')
    tree.pack()

    # Insertar los datos en el Treeview
    for docente in docentes:
        tree.insert('', 'end', values=docente)

# Función para eliminar un docente
def eliminar_docente():
    def eliminar():
        codigo = int(entry_codigo.get())
        contraseña = entry_contraseña.get()

        # Eliminar el docente de la tabla "Docente"
        c.execute("DELETE FROM Docente WHERE codigo = ? AND contraseña = ?", (codigo, contraseña))
        conn.commit()
        messagebox.showinfo('Éxito', 'Docente eliminado correctamente.')
        window_eliminar.destroy()

    # Crear ventana para eliminar docente
    window_eliminar = Toplevel(root)
    window_eliminar.title('Eliminar Docente')

    label_codigo = Label(window_eliminar, text='Código:')
    label_codigo.pack()
    entry_codigo = Entry(window_eliminar)
    entry_codigo.pack()

    label_contraseña = Label(window_eliminar, text='Contraseña:')
    label_contraseña.pack()
    entry_contraseña = Entry(window_eliminar, show='*')
    entry_contraseña.pack()

    btn_eliminar = Button(window_eliminar, text='Eliminar', command=eliminar)
    btn_eliminar.pack()

# Función para mostrar las asistencias
def mostrar_asistencias():
    def buscar_asistencias():
        codigo = int(entry_codigo.get())

        # Buscar las asistencias del docente en la tabla "RegistroAsistencia"
        c.execute("SELECT * FROM RegistroAsistencia WHERE codigo = ?", (codigo,))
        asistencias = c.fetchall()

        # Crear ventana para mostrar asistencias
        window_asistencias = Toplevel(root)
        window_asistencias.title('Asistencias')

        # Crear el Treeview
        tree = ttk.Treeview(window_asistencias, columns=('codigo', 'contraseña', 'fecha_hora'), show='headings')
        tree.heading('codigo', text='Código')
        tree.heading('contraseña', text='Contraseña')
        tree.heading('fecha_hora', text='Fecha y Hora')
        tree.pack()

        # Insertar los datos en el Treeview
        for asistencia in asistencias:
            tree.insert('', 'end', values=asistencia)

    # Crear ventana para buscar asistencias
    window_buscar = Toplevel(root)
    window_buscar.title('Buscar Asistencias')

    label_codigo = Label(window_buscar, text='Código:')
    label_codigo.pack()
    entry_codigo = Entry(window_buscar)
    entry_codigo.pack()

    btn_buscar = Button(window_buscar, text='Buscar', command=buscar_asistencias)
    btn_buscar.pack()

# Crear la interfaz gráfica
root = Tk()
root.title('Registro de Asistencia')

btn_agregar_docente = Button(root, text='Agregar Docente', command=agregar_docente)
btn_agregar_docente.pack()

btn_registrar_asistencia = Button(root, text='Registrar Asistencia', command=registrar_asistencia)
btn_registrar_asistencia.pack()

btn_mostrar_docentes = Button(root, text='Mostrar Docentes', command=mostrar_docentes)
btn_mostrar_docentes.pack()

btn_eliminar_docente = Button(root, text='Eliminar Docente', command=eliminar_docente)
btn_eliminar_docente.pack()

btn_mostrar_asistencias = Button(root, text='Mostrar Asistencias', command=mostrar_asistencias)
btn_mostrar_asistencias.pack()

root.mainloop()

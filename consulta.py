import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as conn
from tkinter import font as tkfont
from datetime import datetime
from os import system
system("cls")

class ConsultaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Médico - Consultas")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f8ff')
        
        try:
            self.conexao = conn.connect(
                host="localhost",
                user="root",
                password="M@taturu.1981",
                database="consultorio_medical"
            )
            self.cursor = self.conexao.cursor()
            self.carregar_pacientes()
            self.carregar_medicos()
        except Exception as e:
            messagebox.showerror("Erro", f"Conexão falhou: {str(e)}")
            self.root.destroy()
            return

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f8ff')
        self.style.configure('TLabel', background='#f0f8ff', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))
        self.style.configure('Accent.TButton', foreground='white', background='#4a6ea9')
        
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight='bold')
        self.status_options = ['Agendada', 'Confirmada', 'Cancelada', 'Realizada', 'Paciente faltou']
        self.create_widgets()

    def carregar_pacientes(self):
        try:
            self.cursor.execute("SELECT ID, Nome FROM Paciente")
            self.pacientes = {f"{id} - {nome}": id for id, nome in self.cursor.fetchall()}
            self.pacientes_lista = list(self.pacientes.keys())
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar pacientes: {str(e)}")
            self.pacientes = {}
            self.pacientes_lista = []

    def carregar_medicos(self):
        try:
            self.cursor.execute("SELECT ID, Nome FROM Medico")
            self.medicos = {f"{id} - {nome}": id for id, nome in self.cursor.fetchall()}
            self.medicos_lista = list(self.medicos.keys())
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar médicos: {str(e)}")
            self.medicos = {}
            self.medicos_lista = []

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Gerenciamento de Consultas", font=self.title_font)
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        search_frame = ttk.LabelFrame(main_frame, text=" Buscar Consultas ", padding=10)
        search_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)
        
        ttk.Label(search_frame, text="Tipo:").grid(row=0, column=0, padx=5)
        self.search_type = ttk.Combobox(search_frame, values=["ID", "Paciente", "Médico", "Data"], state="readonly")
        self.search_type.current(0)
        self.search_type.grid(row=0, column=1, padx=5, sticky="w")
        
        ttk.Label(search_frame, text="Valor:").grid(row=0, column=2, padx=5)
        self.search_value = ttk.Entry(search_frame, width=15)
        self.search_value.grid(row=0, column=3, padx=5, sticky="w")
        
        ttk.Button(search_frame, text="Buscar", command=self.buscar_por_tipo, style='Accent.TButton').grid(row=0, column=4, padx=5)

        form_frame = ttk.LabelFrame(main_frame, text=" Dados da Consulta ", padding=15)
        form_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=10)

        campos = [
            ("ID:", "id_entry", True),
            ("Data*:", "data_entry", False),
            ("Hora*:", "hora_entry", False),
            ("Status*:", "status_combobox", False),
            ("Paciente*:", "paciente_combobox", False),
            ("Médico*:", "medico_combobox", False),
            ("Observação:", "observacao_text", False)
        ]
        
        for i, (text, attr, readonly) in enumerate(campos):
            ttk.Label(form_frame, text=text).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            
            if attr == "observacao_text":
                entry = tk.Text(form_frame, height=4, width=30)
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            elif attr.endswith("combobox"):
                if "status" in attr:
                    values = self.status_options
                elif "paciente" in attr:
                    values = self.pacientes_lista
                else:  # médico
                    values = self.medicos_lista
                entry = ttk.Combobox(form_frame, values=values, state="readonly")
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            else:
                entry = ttk.Entry(form_frame)
                if readonly:
                    entry.config(state='readonly')
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            
            setattr(self, attr, entry)

        # Configurar valores padrão
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.status_combobox.set('Agendada')

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Novo", command=self.nova_consulta).grid(row=0, column=0, padx=5)
        self.salvar_btn = ttk.Button(button_frame, text="Salvar", command=self.salvar_consulta, state=tk.DISABLED)
        self.salvar_btn.grid(row=0, column=1, padx=5)
        self.atualizar_btn = ttk.Button(button_frame, text="Atualizar", command=self.atualizar_consulta, state=tk.DISABLED)
        self.atualizar_btn.grid(row=0, column=2, padx=5)
        self.deletar_btn = ttk.Button(button_frame, text="Deletar", command=self.deletar_consulta, state=tk.DISABLED)
        self.deletar_btn.grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.limpar_campos).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(main_frame, 
                               columns=("ID", "Data", "Hora", "Status", "Paciente", "Médico", "Observacao"), 
                               show="headings", height=12)
        self.tree.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=10)
        
        colunas = [
            ("ID", 50),
            ("Data", 100),
            ("Hora", 80),
            ("Status", 120),
            ("Paciente", 200),
            ("Médico", 200),
            ("Observacao", 200)
        ]
        
        for col, width in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="w")
        
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_consulta)
        self.carregar_consultas()

    def buscar_por_tipo(self):
        tipo = self.search_type.get()
        valor_busca = self.search_value.get()
        
        if not valor_busca:
            messagebox.showwarning("Aviso", "Digite um valor para buscar")
            return

        try:
            if tipo == "ID":
                self.cursor.execute("SELECT * FROM Consulta WHERE ID = %s", (valor_busca,))
            elif tipo == "Paciente":
                self.cursor.execute("""SELECT c.* FROM Consulta c
                                      JOIN Paciente p ON c.Paciente_ID = p.ID
                                      WHERE p.Nome LIKE %s""", (f"%{valor_busca}%",))
            elif tipo == "Médico":
                self.cursor.execute("""SELECT c.* FROM Consulta c
                                      JOIN Medico m ON c.Medico_ID = m.ID
                                      WHERE m.Nome LIKE %s""", (f"%{valor_busca}%",))
            else:  # Data
                try:
                    data_busca = datetime.strptime(valor_busca, '%d/%m/%Y').date()
                    self.cursor.execute("SELECT * FROM Consulta WHERE Data = %s", (data_busca,))
                except ValueError:
                    messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
                    return
            
            resultado = self.cursor.fetchone()
            
            if resultado:
                self.limpar_campos()
                self.id_entry.config(state='normal')
                self.id_entry.insert(0, resultado[0])
                self.id_entry.config(state='readonly')
                self.data_entry.delete(0, tk.END)
                self.data_entry.insert(0, resultado[1].strftime('%d/%m/%Y'))
                self.hora_entry.delete(0, tk.END)
                self.hora_entry.insert(0, resultado[2].strftime('%H:%M'))
                self.status_combobox.set(resultado[3])
                
                # Carregar paciente
                self.cursor.execute("SELECT CONCAT(ID, ' - ', Nome) FROM Paciente WHERE ID = %s", (resultado[5],))
                paciente = self.cursor.fetchone()[0]
                self.paciente_combobox.set(paciente)
                
                # Carregar médico
                self.cursor.execute("SELECT CONCAT(ID, ' - ', Nome) FROM Medico WHERE ID = %s", (resultado[6],))
                medico = self.cursor.fetchone()[0]
                self.medico_combobox.set(medico)
                
                self.observacao_text.delete('1.0', tk.END)
                self.observacao_text.insert('1.0', resultado[4] if resultado[4] else "")
                
                self.atualizar_btn.config(state=tk.NORMAL)
                self.deletar_btn.config(state=tk.NORMAL)
                
                self.carregar_consultas(f"WHERE c.ID = {resultado[0]}")
            else:
                messagebox.showinfo("Informação", "Nenhuma consulta encontrada")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar: {str(e)}")

    def carregar_consultas(self, where_clause=""):
        self.tree.delete(*self.tree.get_children())
        try:
            query = f"""SELECT c.ID, c.Data, c.Hora, c.Status, 
                       CONCAT(p.ID, ' - ', p.Nome) AS Paciente,
                       CONCAT(m.ID, ' - ', m.Nome) AS Medico,
                       c.Observacao
                       FROM Consulta c
                       JOIN Paciente p ON c.Paciente_ID = p.ID
                       JOIN Medico m ON c.Medico_ID = m.ID
                       {where_clause} 
                       ORDER BY c.Data, c.Hora"""
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                # Formatar data e hora
                formatted_row = list(row)
                formatted_row[1] = row[1].strftime('%d/%m/%Y')
                formatted_row[2] = row[2].strftime('%H:%M')
                self.tree.insert("", "end", values=formatted_row)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar: {str(e)}")

    def selecionar_consulta(self, event):
        item = self.tree.focus()
        if item:
            dados = self.tree.item(item)['values']
            self.limpar_campos()
            self.id_entry.config(state='normal')
            self.id_entry.insert(0, dados[0])
            self.id_entry.config(state='readonly')
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, dados[1])
            self.hora_entry.delete(0, tk.END)
            self.hora_entry.insert(0, dados[2])
            self.status_combobox.set(dados[3])
            self.paciente_combobox.set(dados[4])
            self.medico_combobox.set(dados[5])
            self.observacao_text.delete('1.0', tk.END)
            if len(dados) > 6 and dados[6]:
                self.observacao_text.insert('1.0', dados[6])
            self.atualizar_btn.config(state=tk.NORMAL)
            self.deletar_btn.config(state=tk.NORMAL)

    def nova_consulta(self):
        self.limpar_campos()
        self.salvar_btn.config(state=tk.NORMAL)
        self.data_entry.focus()
        # Configurar valores padrão
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.status_combobox.set('Agendada')

    def limpar_campos(self):
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state='readonly')
        self.data_entry.delete(0, tk.END)
        self.hora_entry.delete(0, tk.END)
        self.status_combobox.set('')
        self.paciente_combobox.set('')
        self.medico_combobox.set('')
        self.observacao_text.delete('1.0', tk.END)
        self.salvar_btn.config(state=tk.DISABLED)
        self.atualizar_btn.config(state=tk.DISABLED)
        self.deletar_btn.config(state=tk.DISABLED)
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def validar_campos(self):
        # Validar data
        try:
            data = datetime.strptime(self.data_entry.get(), '%d/%m/%Y').date()
            if data < datetime.now().date():
                messagebox.showerror("Erro", "Data não pode ser no passado!")
                self.data_entry.focus()
                return False
        except ValueError:
            messagebox.showerror("Erro", "Data inválida! Use o formato DD/MM/AAAA")
            self.data_entry.focus()
            return False
        
        # Validar hora
        try:
            datetime.strptime(self.hora_entry.get(), '%H:%M').time()
        except ValueError:
            messagebox.showerror("Erro", "Formato de hora inválido! Use HH:MM")
            self.hora_entry.focus()
            return False
        
        if not self.status_combobox.get():
            messagebox.showerror("Erro", "Selecione um status!")
            self.status_combobox.focus()
            return False
            
        if not self.paciente_combobox.get():
            messagebox.showerror("Erro", "Selecione um paciente!")
            self.paciente_combobox.focus()
            return False
            
        if not self.medico_combobox.get():
            messagebox.showerror("Erro", "Selecione um médico!")
            self.medico_combobox.focus()
            return False
        
        return True

    def salvar_consulta(self):
        if not self.validar_campos():
            return

        try:
            paciente_id = self.pacientes[self.paciente_combobox.get()]
            medico_id = self.medicos[self.medico_combobox.get()]
            data = datetime.strptime(self.data_entry.get(), '%d/%m/%Y').date()
            hora = datetime.strptime(self.hora_entry.get(), '%H:%M').time()
            
            query = """INSERT INTO Consulta 
                      (Data, Hora, Status, Observacao, Paciente_ID, Medico_ID) 
                      VALUES (%s, %s, %s, %s, %s, %s)"""
            valores = (
                data,
                hora,
                self.status_combobox.get(),
                self.observacao_text.get('1.0', tk.END).strip() or None,
                paciente_id,
                medico_id
            )
            
            self.cursor.execute(query, valores)
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Consulta cadastrada com sucesso!")
            self.limpar_campos()
            self.carregar_consultas()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {str(e)}")

    def atualizar_consulta(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione uma consulta para atualizar")
            return
        
        if not self.validar_campos():
            return

        try:
            paciente_id = self.pacientes[self.paciente_combobox.get()]
            medico_id = self.medicos[self.medico_combobox.get()]
            data = datetime.strptime(self.data_entry.get(), '%d/%m/%Y').date()
            hora = datetime.strptime(self.hora_entry.get(), '%H:%M').time()
            
            query = """UPDATE Consulta SET 
                      Data = %s,
                      Hora = %s,
                      Status = %s,
                      Observacao = %s,
                      Paciente_ID = %s,
                      Medico_ID = %s
                      WHERE ID = %s"""
            valores = (
                data,
                hora,
                self.status_combobox.get(),
                self.observacao_text.get('1.0', tk.END).strip() or None,
                paciente_id,
                medico_id,
                self.id_entry.get()
            )
            
            self.cursor.execute(query, valores)
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Consulta atualizada com sucesso!")
            self.carregar_consultas()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {str(e)}")

    def deletar_consulta(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione uma consulta para deletar")
            return

        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar esta consulta?"):
            return

        try:
            self.cursor.execute("DELETE FROM Consulta WHERE ID = %s", (self.id_entry.get(),))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Consulta deletada com sucesso!")
            self.limpar_campos()
            self.carregar_consultas()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao deletar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConsultaApp(root)
    root.mainloop()
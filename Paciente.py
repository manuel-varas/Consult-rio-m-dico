import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as conn
from tkinter import font as tkfont
from os import system
from datetime import datetime
system("cls")

class PacienteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Médico - Pacientes")
        self.root.geometry("1200x900")
        self.root.configure(bg='#f0f8ff')
        
        try:
            self.conexao = conn.connect(
                host="localhost",
                user="root",
                password="M@taturu.1981",
                database="consultorio_medical"
            )
            self.cursor = self.conexao.cursor()
            self.carregar_convenios()
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
        self.create_widgets()

    def carregar_convenios(self):
        try:
            self.cursor.execute("SELECT ID, Nome FROM Convenio")
            self.convenios = {nome: id for id, nome in self.cursor.fetchall()}
            self.convenios_nomes = list(self.convenios.keys())
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar convênios: {str(e)}")
            self.convenios = {}
            self.convenios_nomes = []

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Gerenciamento de Pacientes", font=self.title_font)
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        search_frame = ttk.LabelFrame(main_frame, text=" Buscar Pacientes ", padding=10)
        search_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)
        
        ttk.Label(search_frame, text="Tipo:").grid(row=0, column=0, padx=5)
        self.search_type = ttk.Combobox(search_frame, values=["ID", "Nome", "CPF"], state="readonly")
        self.search_type.current(0)
        self.search_type.grid(row=0, column=1, padx=5, sticky="w")
        
        ttk.Label(search_frame, text="Valor:").grid(row=0, column=2, padx=5)
        self.search_value = ttk.Entry(search_frame, width=15)
        self.search_value.grid(row=0, column=3, padx=5, sticky="w")
        
        ttk.Button(search_frame, text="Buscar", command=self.buscar_por_tipo, style='Accent.TButton').grid(row=0, column=4, padx=5)

        form_frame = ttk.LabelFrame(main_frame, text=" Dados do Paciente ", padding=15)
        form_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=10)

        campos = [
            ("ID:", "id_entry", True),
            ("Nome*:", "nome_entry", False),
            ("Email:", "email_entry", False),
            ("Telefone:", "telefone_entry", False),
            ("CPF:", "cpf_entry", False),
            ("Data Nasc.:", "data_nasc_entry", False),
            ("Convênio:", "convenio_combobox", False),
            ("Endereço ID:", "endereco_id_entry", False)
        ]
        
        for i, (text, attr, readonly) in enumerate(campos):
            ttk.Label(form_frame, text=text).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            
            if attr == "convenio_combobox":
                entry = ttk.Combobox(form_frame, values=self.convenios_nomes, state="readonly")
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            else:
                entry = ttk.Entry(form_frame)
                if readonly:
                    entry.config(state='readonly')
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            
            setattr(self, attr, entry)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Novo", command=self.novo_paciente).grid(row=0, column=0, padx=5)
        self.salvar_btn = ttk.Button(button_frame, text="Salvar", command=self.salvar_paciente, state=tk.DISABLED)
        self.salvar_btn.grid(row=0, column=1, padx=5)
        self.atualizar_btn = ttk.Button(button_frame, text="Atualizar", command=self.atualizar_paciente, state=tk.DISABLED)
        self.atualizar_btn.grid(row=0, column=2, padx=5)
        self.deletar_btn = ttk.Button(button_frame, text="Deletar", command=self.deletar_paciente, state=tk.DISABLED)
        self.deletar_btn.grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.limpar_campos).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(main_frame, 
                               columns=("ID", "Nome", "Email", "Telefone", "CPF", "Data_Nasc", "Convenio", "Endereco_ID"), 
                               show="headings", height=12)
        self.tree.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=10)
        
        colunas = [
            ("ID", 50),
            ("Nome", 150),
            ("Email", 150),
            ("Telefone", 100),
            ("CPF", 100),
            ("Data_Nasc", 100),
            ("Convenio", 100),
            ("Endereco_ID", 80)
        ]
        
        for col, width in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="w")
        
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_paciente)
        self.carregar_pacientes()

    def buscar_por_tipo(self):
        tipo = self.search_type.get()
        valor_busca = self.search_value.get()
        
        if not valor_busca:
            messagebox.showwarning("Aviso", "Digite um valor para buscar")
            return

        try:
            if tipo == "ID":
                self.cursor.execute("SELECT * FROM Paciente WHERE ID = %s", (valor_busca,))
            elif tipo == "Nome":
                self.cursor.execute("SELECT * FROM Paciente WHERE Nome LIKE %s", (f"%{valor_busca}%",))
            else:  # CPF
                self.cursor.execute("SELECT * FROM Paciente WHERE CPF = %s", (valor_busca,))
            
            resultado = self.cursor.fetchone()
            
            if resultado:
                self.limpar_campos()
                self.id_entry.config(state='normal')
                self.id_entry.insert(0, resultado[0])
                self.id_entry.config(state='readonly')
                self.nome_entry.insert(0, resultado[1])
                self.email_entry.insert(0, resultado[2] if resultado[2] else "")
                self.telefone_entry.insert(0, resultado[3] if resultado[3] else "")
                self.cpf_entry.insert(0, resultado[4] if resultado[4] else "")
                
                # Formatar data
                if resultado[5]:
                    data_formatada = resultado[5].strftime('%d/%m/%Y')
                    self.data_nasc_entry.insert(0, data_formatada)
                
                # Definir convênio
                if resultado[6]:
                    self.cursor.execute("SELECT Nome FROM Convenio WHERE ID = %s", (resultado[6],))
                    convenio_nome = self.cursor.fetchone()[0]
                    self.convenio_combobox.set(convenio_nome)
                
                self.endereco_id_entry.insert(0, resultado[7] if resultado[7] else "")
                
                self.atualizar_btn.config(state=tk.NORMAL)
                self.deletar_btn.config(state=tk.NORMAL)
                
                self.carregar_pacientes(f"WHERE ID = {resultado[0]}")
            else:
                messagebox.showinfo("Informação", "Nenhum paciente encontrado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar: {str(e)}")

    def carregar_pacientes(self, where_clause=""):
        self.tree.delete(*self.tree.get_children())
        try:
            query = f"""SELECT p.ID, p.Nome, p.Email, p.Telefone, p.CPF, p.Data_Nascimento, 
                       c.Nome, p.Endereco_ID 
                       FROM Paciente p
                       LEFT JOIN Convenio c ON p.Convenio_ID = c.ID
                       {where_clause} 
                       ORDER BY p.ID"""
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                # Formatar data
                if row[5]:
                    data_formatada = row[5].strftime('%d/%m/%Y')
                    row = list(row)
                    row[5] = data_formatada
                
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar: {str(e)}")

    def selecionar_paciente(self, event):
        item = self.tree.focus()
        if item:
            dados = self.tree.item(item)['values']
            self.limpar_campos()
            self.id_entry.config(state='normal')
            self.id_entry.insert(0, dados[0])
            self.id_entry.config(state='readonly')
            self.nome_entry.insert(0, dados[1])
            self.email_entry.insert(0, dados[2] if len(dados) > 2 and dados[2] else "")
            self.telefone_entry.insert(0, dados[3] if len(dados) > 3 and dados[3] else "")
            self.cpf_entry.insert(0, dados[4] if len(dados) > 4 and dados[4] else "")
            
            if len(dados) > 5 and dados[5]:
                self.data_nasc_entry.insert(0, dados[5])
            
            if len(dados) > 6 and dados[6]:
                self.convenio_combobox.set(dados[6])
            
            self.endereco_id_entry.insert(0, dados[7] if len(dados) > 7 and dados[7] else "")
            self.atualizar_btn.config(state=tk.NORMAL)
            self.deletar_btn.config(state=tk.NORMAL)

    def novo_paciente(self):
        self.limpar_campos()
        self.salvar_btn.config(state=tk.NORMAL)
        self.nome_entry.focus()

    def limpar_campos(self):
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state='readonly')
        self.nome_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.cpf_entry.delete(0, tk.END)
        self.data_nasc_entry.delete(0, tk.END)
        self.convenio_combobox.set('')
        self.endereco_id_entry.delete(0, tk.END)
        self.salvar_btn.config(state=tk.DISABLED)
        self.atualizar_btn.config(state=tk.DISABLED)
        self.deletar_btn.config(state=tk.DISABLED)
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def validar_campos(self):
        if not self.nome_entry.get().strip():
            messagebox.showerror("Erro", "O campo Nome é obrigatório!")
            self.nome_entry.focus()
            return False
        
        # Validação básica de CPF (apenas formato)
        cpf = self.cpf_entry.get()
        if cpf and len(cpf) not in (11, 14):  # 11 dígitos ou 14 com formatação
            messagebox.showerror("Erro", "CPF inválido! Deve ter 11 dígitos (com ou sem formatação)")
            self.cpf_entry.focus()
            return False
        
        # Validação de data
        data_nasc = self.data_nasc_entry.get()
        if data_nasc:
            try:
                datetime.strptime(data_nasc, '%d/%m/%Y')
            except ValueError:
                messagebox.showerror("Erro", "Data de nascimento inválida! Use o formato DD/MM/AAAA")
                self.data_nasc_entry.focus()
                return False
        
        return True

    def salvar_paciente(self):
        if not self.validar_campos():
            return

        try:
            # Formatar data
            data_nasc = None
            if self.data_nasc_entry.get():
                data_nasc = datetime.strptime(self.data_nasc_entry.get(), '%d/%m/%Y').date()
            
            # Obter ID do convênio
            convenio_id = None
            convenio_nome = self.convenio_combobox.get()
            if convenio_nome:
                convenio_id = self.convenios.get(convenio_nome)
            
            query = """INSERT INTO Paciente 
                      (Nome, Email, Telefone, CPF, Data_Nascimento, Convenio_ID, Endereco_ID) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            valores = (
                self.nome_entry.get(),
                self.email_entry.get() or None,
                self.telefone_entry.get() or None,
                self.cpf_entry.get() or None,
                data_nasc,
                convenio_id,
                self.endereco_id_entry.get() or None
            )
            
            self.cursor.execute(query, valores)
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_pacientes()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {str(e)}")

    def atualizar_paciente(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione um paciente para atualizar")
            return
        
        if not self.validar_campos():
            return

        try:
            # Formatar data
            data_nasc = None
            if self.data_nasc_entry.get():
                data_nasc = datetime.strptime(self.data_nasc_entry.get(), '%d/%m/%Y').date()
            
            # Obter ID do convênio
            convenio_id = None
            convenio_nome = self.convenio_combobox.get()
            if convenio_nome:
                convenio_id = self.convenios.get(convenio_nome)
            
            query = """UPDATE Paciente SET 
                      Nome = %s,
                      Email = %s,
                      Telefone = %s,
                      CPF = %s,
                      Data_Nascimento = %s,
                      Convenio_ID = %s,
                      Endereco_ID = %s
                      WHERE ID = %s"""
            valores = (
                self.nome_entry.get(),
                self.email_entry.get() or None,
                self.telefone_entry.get() or None,
                self.cpf_entry.get() or None,
                data_nasc,
                convenio_id,
                self.endereco_id_entry.get() or None,
                self.id_entry.get()
            )
            
            self.cursor.execute(query, valores)
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso!")
            self.carregar_pacientes()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {str(e)}")

    def deletar_paciente(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione um paciente para deletar")
            return

        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar este paciente?"):
            return

        try:
            self.cursor.execute("DELETE FROM Paciente WHERE ID = %s", (self.id_entry.get(),))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Paciente deletado com sucesso!")
            self.limpar_campos()
            self.carregar_pacientes()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao deletar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PacienteApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as conn
from tkinter import font as tkfont
from os import system
system("cls")

class MedicoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Médico - Médicos")
        self.root.geometry("1100x800")
        self.root.configure(bg='#f0f8ff')
        
        try:
            self.conexao = conn.connect(
                host="localhost",
                user="root",
                password="M@taturu.1981",
                database="consultorio_medical"
            )
            self.cursor = self.conexao.cursor()
            self.verificar_estrutura_tabela()
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

    def verificar_estrutura_tabela(self):
        try:
            self.cursor.execute("SHOW COLUMNS FROM Medico LIKE 'Nome'")
            if not self.cursor.fetchone():
                self.cursor.execute("ALTER TABLE Medico ADD COLUMN Nome VARCHAR(100) AFTER ID")
                self.conexao.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao verificar estrutura da tabela: {str(e)}")

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Gerenciamento de Médicos", font=self.title_font)
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        search_frame = ttk.LabelFrame(main_frame, text=" Buscar Médicos ", padding=10)
        search_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)
        
        ttk.Label(search_frame, text="Tipo:").grid(row=0, column=0, padx=5)
        self.search_type = ttk.Combobox(search_frame, values=["Médico", "CRM"], state="readonly")
        self.search_type.current(0)
        self.search_type.grid(row=0, column=1, padx=5, sticky="w")
        
        ttk.Label(search_frame, text="ID/CRM:").grid(row=0, column=2, padx=5)
        self.search_id = ttk.Entry(search_frame, width=15)
        self.search_id.grid(row=0, column=3, padx=5, sticky="w")
        
        ttk.Button(search_frame, text="Buscar", command=self.buscar_por_tipo, style='Accent.TButton').grid(row=0, column=4, padx=5)

        form_frame = ttk.LabelFrame(main_frame, text=" Dados do Médico ", padding=15)
        form_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=10)

        campos = [
            ("ID:", "id_entry", True),
            ("Nome:", "nome_entry", False),
            ("CRM:", "crm_entry", False),
            ("Especialidade:", "especialidade_entry", False),
            ("Endereço ID:", "endereco_id_entry", False)
        ]
        
        for i, (text, attr, readonly) in enumerate(campos):
            ttk.Label(form_frame, text=text).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(form_frame)
            if readonly:
                entry.config(state='readonly')
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            setattr(self, attr, entry)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Novo", command=self.novo_medico).grid(row=0, column=0, padx=5)
        self.salvar_btn = ttk.Button(button_frame, text="Salvar", command=self.salvar_medico, state=tk.DISABLED)
        self.salvar_btn.grid(row=0, column=1, padx=5)
        self.atualizar_btn = ttk.Button(button_frame, text="Atualizar", command=self.atualizar_medico, state=tk.DISABLED)
        self.atualizar_btn.grid(row=0, column=2, padx=5)
        self.deletar_btn = ttk.Button(button_frame, text="Deletar", command=self.deletar_medico, state=tk.DISABLED)
        self.deletar_btn.grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.limpar_campos).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(main_frame, 
                               columns=("ID", "Nome", "CRM", "Especialidade", "Endereco_ID"), 
                               show="headings", height=12)
        self.tree.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=10)
        
        for col in ("ID", "Nome", "CRM", "Especialidade", "Endereco_ID"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="w")
        
        self.tree.column("Nome", width=150)
        self.tree.column("Especialidade", width=200)
        
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_medico)
        self.carregar_medicos()

    def buscar_por_tipo(self):
        tipo = self.search_type.get()
        valor_busca = self.search_id.get()
        
        if not valor_busca:
            messagebox.showwarning("Aviso", "Digite um valor para buscar")
            return

        try:
            if tipo == "Médico":
                self.cursor.execute("SELECT * FROM Medico WHERE ID = %s", (valor_busca,))
            else:
                self.cursor.execute("SELECT * FROM Medico WHERE CRM = %s", (valor_busca,))
            
            resultado = self.cursor.fetchone()
            
            if resultado:
                self.limpar_campos()
                self.id_entry.config(state='normal')
                self.id_entry.insert(0, resultado[0])
                self.id_entry.config(state='readonly')
                self.nome_entry.insert(0, resultado[1])
                self.crm_entry.insert(0, resultado[2])
                self.especialidade_entry.insert(0, resultado[3])
                self.endereco_id_entry.insert(0, resultado[4] if resultado[4] else "")
                
                self.atualizar_btn.config(state=tk.NORMAL)
                self.deletar_btn.config(state=tk.NORMAL)
                
                self.carregar_medicos(f"WHERE ID = {resultado[0]}")
            else:
                messagebox.showinfo("Informação", "Nenhum médico encontrado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar: {str(e)}")

    def carregar_medicos(self, where_clause=""):
        self.tree.delete(*self.tree.get_children())
        try:
            query = f"SELECT ID, Nome, CRM, Especialidade, Endereco_ID FROM Medico {where_clause} ORDER BY ID"
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar: {str(e)}")

    def selecionar_medico(self, event):
        item = self.tree.focus()
        if item:
            dados = self.tree.item(item)['values']
            self.limpar_campos()
            self.id_entry.config(state='normal')
            self.id_entry.insert(0, dados[0])
            self.id_entry.config(state='readonly')
            self.nome_entry.insert(0, dados[1])
            self.crm_entry.insert(0, dados[2])
            self.especialidade_entry.insert(0, dados[3])
            self.endereco_id_entry.insert(0, dados[4] if dados[4] else "")
            self.atualizar_btn.config(state=tk.NORMAL)
            self.deletar_btn.config(state=tk.NORMAL)

    def novo_medico(self):
        self.limpar_campos()
        self.salvar_btn.config(state=tk.NORMAL)
        self.nome_entry.focus()

    def limpar_campos(self):
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state='readonly')
        self.nome_entry.delete(0, tk.END)
        self.crm_entry.delete(0, tk.END)
        self.especialidade_entry.delete(0, tk.END)
        self.endereco_id_entry.delete(0, tk.END)
        self.salvar_btn.config(state=tk.DISABLED)
        self.atualizar_btn.config(state=tk.DISABLED)
        self.deletar_btn.config(state=tk.DISABLED)
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def validar_campos(self):
        campos_obrigatorios = [
            (self.nome_entry, "Nome"),
            (self.crm_entry, "CRM"),
            (self.especialidade_entry, "Especialidade")
        ]
        
        for campo, nome in campos_obrigatorios:
            if not campo.get().strip():
                messagebox.showerror("Erro", f"O campo {nome} é obrigatório!")
                campo.focus()
                return False
        
        return True

    def salvar_medico(self):
        if not self.validar_campos():
            return

        try:
            query = """INSERT INTO Medico 
                      (Nome, CRM, Especialidade, Endereco_ID) 
                      VALUES (%s, %s, %s, %s)"""
            valores = (
                self.nome_entry.get(),
                self.crm_entry.get(),
                self.especialidade_entry.get(),
                self.endereco_id_entry.get() or None
            )
            
            self.cursor.execute(query, valores)
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Médico cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_medicos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {str(e)}")

    def atualizar_medico(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione um médico para atualizar")
            return
        
        if not self.validar_campos():
            return

        try:
            query = """UPDATE Medico SET 
                      Nome = %s,
                      CRM = %s,
                      Especialidade = %s,
                      Endereco_ID = %s
                      WHERE ID = %s"""
            valores = (
                self.nome_entry.get(),
                self.crm_entry.get(),
                self.especialidade_entry.get(),
                self.endereco_id_entry.get() or None,
                self.id_entry.get()
            )
            
            self.cursor.execute(query, valores)
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Médico atualizado com sucesso!")
            self.carregar_medicos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {str(e)}")

    def deletar_medico(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione um médico para deletar")
            return

        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar este médico?"):
            return

        try:
            self.cursor.execute("DELETE FROM Medico WHERE ID = %s", (self.id_entry.get(),))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Médico deletado com sucesso!")
            self.limpar_campos()
            self.carregar_medicos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao deletar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicoApp(root)
    root.mainloop()
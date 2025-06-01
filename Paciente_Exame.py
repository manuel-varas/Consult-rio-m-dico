import tkinter as tk
from tkinter import ttk, messagebox, font
import mysql.connector
from datetime import datetime
from os import system
system("cls")

class SistemaPacienteExame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Exames de Pacientes")
        self.root.geometry("1350x750")
        self.root.configure(bg='#f0f8ff')
        self.conectar_banco_dados()
        self.configurar_interface()
        self.carregar_dados_referencia()
        self.criar_componentes()
        self.carregar_todos_relacionamentos()

    def conectar_banco_dados(self):
        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="M@taturu.1981",
                database="consultorio_medical"
            )
            self.cursor = self.conexao.cursor(dictionary=True)
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados:\n{str(e)}")
            self.root.destroy()

    def configurar_interface(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f8ff')
        self.style.configure('TLabel', background='#f0f8ff', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))
        self.style.configure('Accent.TButton', foreground='white', background='#4a6ea9')
        self.fonte_titulo = font.Font(family='Helvetica', size=16, weight='bold')

    def carregar_dados_referencia(self):
        try:
            # Carregar pacientes com tratamento para valores nulos
            self.cursor.execute("SELECT ID, Nome, COALESCE(CPF, 'Não informado') AS CPF FROM Paciente ORDER BY Nome")
            self.pacientes = self.cursor.fetchall()
            self.lista_pacientes = [f"{p['ID']} - {p['Nome']} (CPF: {p['CPF']})" for p in self.pacientes]
            
            # Carregar exames com tratamento para valores nulos
            self.cursor.execute("SELECT ID, Nome, COALESCE(Descricao, 'Sem descrição') AS Descricao FROM Exame ORDER BY Nome")
            self.exames = self.cursor.fetchall()
            self.lista_exames = [f"{e['ID']} - {e['Nome']} ({e['Descricao']})" for e in self.exames]
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erro no Banco de Dados", f"Falha ao carregar dados:\n{str(err)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado:\n{str(e)}")

    def criar_componentes(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="Gerenciamento de Exames de Pacientes", font=self.fonte_titulo)
        title.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Área de busca
        self.criar_area_busca(main_frame)
        
        # Formulário
        self.criar_formulario(main_frame)
        
        # Botões
        self.criar_botoes(main_frame)
        
        # Tabela de resultados
        self.criar_tabela_resultados(main_frame)

    def criar_area_busca(self, parent):
        search_frame = ttk.LabelFrame(parent, text=" Buscar Relacionamentos ", padding=10)
        search_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)
        
        ttk.Label(search_frame, text="Buscar por:").grid(row=0, column=0, padx=5)
        self.search_type = ttk.Combobox(search_frame, values=["Paciente", "Exame"], state="readonly")
        self.search_type.current(0)
        self.search_type.grid(row=0, column=1, padx=5, sticky="w")
        
        ttk.Label(search_frame, text="Termo:").grid(row=0, column=2, padx=5)
        self.search_term = ttk.Entry(search_frame, width=25)
        self.search_term.grid(row=0, column=3, padx=5, sticky="w")
        
        ttk.Button(search_frame, text="Buscar", command=self.buscar_relacionamentos, style='Accent.TButton').grid(row=0, column=4, padx=5)
        ttk.Button(search_frame, text="Limpar", command=self.limpar_busca).grid(row=0, column=5, padx=5)

    def criar_formulario(self, parent):
        form_frame = ttk.LabelFrame(parent, text=" Dados do Relacionamento ", padding=15)
        form_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=10)
        
        # Campo Paciente
        ttk.Label(form_frame, text="Paciente*:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.paciente_combo = ttk.Combobox(form_frame, values=self.lista_pacientes, state="readonly")
        self.paciente_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Campo Exame
        ttk.Label(form_frame, text="Exame*:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.exame_combo = ttk.Combobox(form_frame, values=self.lista_exames, state="readonly")
        self.exame_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    def criar_botoes(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        # Botão Novo
        self.novo_btn = ttk.Button(btn_frame, text="Novo", command=self.novo_relacionamento)
        self.novo_btn.grid(row=0, column=0, padx=5)
        
        # Botão Salvar
        self.salvar_btn = ttk.Button(btn_frame, text="Salvar", command=self.salvar_relacionamento, state=tk.DISABLED)
        self.salvar_btn.grid(row=0, column=1, padx=5)
        
        # Botão Excluir
        self.excluir_btn = ttk.Button(btn_frame, text="Excluir", command=self.excluir_relacionamento, state=tk.DISABLED)
        self.excluir_btn.grid(row=0, column=2, padx=5)
        
        # Botão Limpar
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_formulario).grid(row=0, column=3, padx=5)

    def criar_tabela_resultados(self, parent):
        columns = ("Paciente", "Exame")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=15, selectmode="browse")
        
        # Configurar colunas
        col_widths = [400, 400]
        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="w")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Posicionamento
        self.tree.grid(row=4, column=0, columnspan=4, sticky="nsew")
        scrollbar.grid(row=4, column=4, sticky="ns")
        
        # Evento de seleção
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_relacionamento)

    def buscar_relacionamentos(self):
        tipo = self.search_type.get()
        termo = self.search_term.get().strip()
        
        if not termo and tipo != "Exame":
            messagebox.showwarning("Aviso", "Digite um termo para busca")
            return
        
        try:
            condicoes = ""
            if tipo == "Paciente": 
                condicoes = f"WHERE pac.Nome LIKE '%{termo}%' OR pac.CPF LIKE '%{termo}%'"
            elif tipo == "Exame": 
                condicoes = f"WHERE ex.Nome LIKE '%{termo}%' OR ex.Descricao LIKE '%{termo}%'"
            
            self.carregar_relacionamentos(condicoes)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na busca:\n{str(e)}")

    def limpar_busca(self):
        self.search_type.current(0)
        self.search_term.delete(0, tk.END)
        self.carregar_relacionamentos()

    def carregar_relacionamentos(self, condicoes=""):
        self.tree.delete(*self.tree.get_children())
        try:
            query = f"""SELECT 
                      CONCAT(pac.ID, ' - ', pac.Nome, ' (CPF: ', COALESCE(pac.CPF, 'Não informado'), ')') AS Paciente,
                      CONCAT(ex.ID, ' - ', ex.Nome, ' (', COALESCE(ex.Descricao, 'Sem descrição'), ')') AS Exame
                      FROM Paciente_Exame pe
                      JOIN Paciente pac ON pe.Paciente_ID = pac.ID
                      JOIN Exame ex ON pe.Exame_ID = ex.ID
                      {condicoes} 
                      ORDER BY pac.Nome, ex.Nome"""
            
            self.cursor.execute(query)
            for relacionamento in self.cursor.fetchall():
                self.tree.insert("", "end", values=(
                    relacionamento['Paciente'],
                    relacionamento['Exame']
                ))
        except mysql.connector.Error as err:
            messagebox.showerror("Erro no Banco de Dados", f"Falha ao carregar relacionamentos:\n{str(err)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado:\n{str(e)}")

    def selecionar_relacionamento(self, event):
        item = self.tree.focus()
        if not item:
            return
            
        dados = self.tree.item(item)['values']
        self.limpar_formulario()
        
        try:
            self.paciente_combo.set(dados[0])
            self.exame_combo.set(dados[1])
            self.excluir_btn.config(state=tk.NORMAL)
            self.salvar_btn.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao selecionar relacionamento:\n{str(e)}")

    def novo_relacionamento(self):
        self.limpar_formulario()
        self.salvar_btn.config(state=tk.NORMAL)
        self.excluir_btn.config(state=tk.DISABLED)
        self.paciente_combo.focus()

    def limpar_formulario(self):
        self.paciente_combo.set('')
        self.exame_combo.set('')
        self.salvar_btn.config(state=tk.DISABLED)
        self.excluir_btn.config(state=tk.DISABLED)
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def validar_campos(self):
        if not self.paciente_combo.get():
            messagebox.showerror("Erro", "Selecione um paciente!")
            self.paciente_combo.focus()
            return False
            
        if not self.exame_combo.get():
            messagebox.showerror("Erro", "Selecione um exame!")
            self.exame_combo.focus()
            return False
        
        return True

    def salvar_relacionamento(self):
        if not self.validar_campos():
            return
            
        try:
            paciente_id = int(self.paciente_combo.get().split(' - ')[0])
            exame_id = int(self.exame_combo.get().split(' - ')[0])
            
            # Verificar se o relacionamento já existe
            self.cursor.execute("SELECT * FROM Paciente_Exame WHERE Paciente_ID = %s AND Exame_ID = %s", 
                              (paciente_id, exame_id))
            if self.cursor.fetchone():
                messagebox.showwarning("Aviso", "Este relacionamento já existe!")
                return
            
            # Inserir novo relacionamento
            self.cursor.execute("INSERT INTO Paciente_Exame (Paciente_ID, Exame_ID) VALUES (%s, %s)", 
                              (paciente_id, exame_id))
            self.conexao.commit()
            
            messagebox.showinfo("Sucesso", "Relacionamento registrado com sucesso!")
            self.limpar_formulario()
            self.carregar_relacionamentos()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erro no Banco de Dados", f"Falha ao salvar relacionamento:\n{str(err)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado ao salvar:\n{str(e)}")

    def excluir_relacionamento(self):
        if not self.paciente_combo.get() or not self.exame_combo.get():
            messagebox.showerror("Erro", "Selecione um relacionamento para excluir")
            return
            
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este relacionamento?"):
            return
            
        try:
            paciente_id = int(self.paciente_combo.get().split(' - ')[0])
            exame_id = int(self.exame_combo.get().split(' - ')[0])
            
            self.cursor.execute("DELETE FROM Paciente_Exame WHERE Paciente_ID = %s AND Exame_ID = %s", 
                              (paciente_id, exame_id))
            self.conexao.commit()
            
            messagebox.showinfo("Sucesso", "Relacionamento excluído com sucesso!")
            self.limpar_formulario()
            self.carregar_relacionamentos()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erro no Banco de Dados", f"Falha ao excluir relacionamento:\n{str(err)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado ao excluir:\n{str(e)}")

    def carregar_todos_relacionamentos(self):
        self.carregar_relacionamentos()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaPacienteExame(root)
    root.mainloop()
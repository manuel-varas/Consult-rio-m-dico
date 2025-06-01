import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as conn
from tkinter import font as tkfont
import requests
from os import system
system("cls")

class EnderecoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Médico - Endereços")
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
            
            # Verificar e corrigir a estrutura da tabela
            self.verificar_estrutura_tabela()
            
            self.cursor.execute("SHOW COLUMNS FROM Endereco")
            colunas = [coluna[0] for coluna in self.cursor.fetchall()]
            self.id_column = colunas[0]
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
            # Verificar se a coluna Bairro existe
            self.cursor.execute("SHOW COLUMNS FROM Endereco LIKE 'Bairro'")
            if not self.cursor.fetchone():
                # Adicionar a coluna Bairro se não existir
                self.cursor.execute("ALTER TABLE Endereco ADD COLUMN Bairro VARCHAR(100) AFTER Complemento")
            
            # Verificar a ordem das colunas CEP e Bairro
            self.cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Endereco' ORDER BY ORDINAL_POSITION")
            colunas = [col[0] for col in self.cursor.fetchall()]
            
            # Se CEP estiver antes de Bairro, corrigir a ordem
            if 'CEP' in colunas and 'Bairro' in colunas and colunas.index('CEP') < colunas.index('Bairro'):
                self.cursor.execute("ALTER TABLE Endereco MODIFY COLUMN Bairro VARCHAR(100) AFTER Complemento")
                self.cursor.execute("ALTER TABLE Endereco MODIFY COLUMN CEP VARCHAR(10) AFTER Bairro")
            
            self.conexao.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao verificar estrutura da tabela: {str(e)}")

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Gerenciamento de Endereços", font=self.title_font)
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        search_frame = ttk.LabelFrame(main_frame, text=" Buscar Endereços ", padding=10)
        search_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)
        
        ttk.Label(search_frame, text="Tipo:").grid(row=0, column=0, padx=5)
        self.search_type = ttk.Combobox(search_frame, values=["Endereço", "Paciente", "Médico", "Consultório"], state="readonly")
        self.search_type.current(0)
        self.search_type.grid(row=0, column=1, padx=5, sticky="w")
        
        ttk.Label(search_frame, text="ID:").grid(row=0, column=2, padx=5)
        self.search_id = ttk.Entry(search_frame, width=15)
        self.search_id.grid(row=0, column=3, padx=5, sticky="w")
        
        ttk.Button(search_frame, text="Buscar", command=self.buscar_por_tipo, style='Accent.TButton').grid(row=0, column=4, padx=5)

        form_frame = ttk.LabelFrame(main_frame, text=" Dados do Endereço ", padding=15)
        form_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=10)

        campos = [
            ("ID:", "id_entry", True),
            ("Logradouro:", "logradouro_entry", False),
            ("Número:", "numero_entry", False),
            ("Complemento:", "complemento_entry", False),
            ("Bairro:", "bairro_entry", False),
            ("CEP:", "cep_entry", False),
            ("Cidade:", "cidade_entry", False),
            ("Estado:", "estado_entry", False)
        ]
        
        for i, (text, attr, readonly) in enumerate(campos):
            ttk.Label(form_frame, text=text).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(form_frame)
            if readonly:
                entry.config(state='readonly')
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            setattr(self, attr, entry)
        
        self.cep_entry.bind("<FocusOut>", self.buscar_cep)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Novo", command=self.novo_endereco).grid(row=0, column=0, padx=5)
        self.salvar_btn = ttk.Button(button_frame, text="Salvar", command=self.salvar_endereco, state=tk.DISABLED)
        self.salvar_btn.grid(row=0, column=1, padx=5)
        self.atualizar_btn = ttk.Button(button_frame, text="Atualizar", command=self.atualizar_endereco, state=tk.DISABLED)
        self.atualizar_btn.grid(row=0, column=2, padx=5)
        self.deletar_btn = ttk.Button(button_frame, text="Deletar", command=self.deletar_endereco, state=tk.DISABLED)
        self.deletar_btn.grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.limpar_campos).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(main_frame, 
                               columns=("ID", "Logradouro", "Número", "Complemento", "Bairro", "CEP", "Cidade", "Estado", "Tipo", "ID Relacionado"), 
                               show="headings", height=12)
        self.tree.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=10)
        
        for col in ("ID", "Logradouro", "Número", "Complemento", "Bairro", "CEP", "Cidade", "Estado", "Tipo", "ID Relacionado"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor="w")
        
        self.tree.column("Logradouro", width=150)
        self.tree.column("Complemento", width=100)
        self.tree.column("Bairro", width=120)
        self.tree.column("Cidade", width=120)
        self.tree.column("Tipo", width=100)
        
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_endereco)
        self.carregar_enderecos()

    def buscar_por_tipo(self):
        tipo = self.search_type.get()
        id_busca = self.search_id.get()
        
        if not id_busca:
            messagebox.showwarning("Aviso", "Digite um ID para buscar")
            return

        try:
            if tipo == "Endereço":
                self.cursor.execute(f"SELECT e.*, 'Endereço' as tipo, NULL as id_relacionado FROM Endereco e WHERE {self.id_column} = %s", (id_busca,))
            elif tipo == "Paciente":
                self.cursor.execute("""
                    SELECT e.*, 'Paciente' as tipo, p.id as id_relacionado 
                    FROM Endereco e
                    JOIN Paciente p ON e.id = p.Endereco_ID 
                    WHERE p.id = %s
                """, (id_busca,))
            elif tipo == "Médico":
                self.cursor.execute("""
                    SELECT e.*, 'Médico' as tipo, m.id as id_relacionado 
                    FROM Endereco e
                    JOIN Medico m ON e.id = m.Endereco_ID 
                    WHERE m.id = %s
                """, (id_busca,))
            elif tipo == "Consultório":
                self.cursor.execute("""
                    SELECT e.*, 'Consultório' as tipo, c.id as id_relacionado 
                    FROM Endereco e
                    JOIN Consultorio c ON e.id = c.Endereco_ID 
                    WHERE c.id = %s
                """, (id_busca,))
            
            resultado = self.cursor.fetchone()
            
            if resultado:
                self.limpar_campos()
                self.id_entry.config(state='normal')
                self.id_entry.insert(0, resultado[0])
                self.id_entry.config(state='readonly')
                self.logradouro_entry.insert(0, resultado[1])
                self.numero_entry.insert(0, resultado[2])
                self.complemento_entry.insert(0, resultado[3] if resultado[3] else "")
                self.bairro_entry.insert(0, resultado[4] if len(resultado) > 4 else "")
                self.cep_entry.insert(0, resultado[5] if len(resultado) > 5 else "")
                self.cidade_entry.insert(0, resultado[6] if len(resultado) > 6 else "")
                self.estado_entry.insert(0, resultado[7] if len(resultado) > 7 else "")
                
                self.atualizar_btn.config(state=tk.NORMAL)
                self.deletar_btn.config(state=tk.NORMAL)
                
                self.carregar_enderecos(f"WHERE e.id = {resultado[0]}")
            else:
                messagebox.showinfo("Informação", f"Nenhum endereço encontrado para este {tipo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar: {str(e)}")

    def buscar_cep(self, event):
        cep = self.cep_entry.get().replace("-", "").strip()
        if len(cep) != 8 or not cep.isdigit():
            return

        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            data = response.json()
            
            if 'erro' not in data:
                self.logradouro_entry.delete(0, tk.END)
                self.logradouro_entry.insert(0, data.get('logradouro', ''))
                
                self.bairro_entry.delete(0, tk.END)
                self.bairro_entry.insert(0, data.get('bairro', ''))
                
                self.cidade_entry.delete(0, tk.END)
                self.cidade_entry.insert(0, data.get('localidade', ''))
                
                self.estado_entry.delete(0, tk.END)
                self.estado_entry.insert(0, data.get('uf', ''))
                
                self.numero_entry.focus()
        except Exception as e:
            messagebox.showwarning("Aviso", f"Não foi possível consultar o CEP: {str(e)}")

    def carregar_enderecos(self, where_clause=""):
        self.tree.delete(*self.tree.get_children())
        try:
            query = f"""
                SELECT 
                    e.id, e.Logradouro, e.Numero, e.Complemento, e.Bairro, e.CEP, e.Cidade, e.Estado,
                    CASE 
                        WHEN p.id IS NOT NULL THEN 'Paciente'
                        WHEN m.id IS NOT NULL THEN 'Médico'
                        WHEN c.id IS NOT NULL THEN 'Consultório'
                        ELSE 'Endereço'
                    END as tipo,
                    COALESCE(p.id, m.id, c.id) as id_relacionado
                FROM Endereco e
                LEFT JOIN Paciente p ON e.id = p.Endereco_ID
                LEFT JOIN Medico m ON e.id = m.Endereco_ID
                LEFT JOIN Consultorio c ON e.id = c.Endereco_ID
                {where_clause}
                ORDER BY e.id
            """
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar: {str(e)}")

    def selecionar_endereco(self, event):
        item = self.tree.focus()
        if item:
            dados = self.tree.item(item)['values']
            self.limpar_campos()
            self.id_entry.config(state='normal')
            self.id_entry.insert(0, dados[0])
            self.id_entry.config(state='readonly')
            self.logradouro_entry.insert(0, dados[1])
            self.numero_entry.insert(0, dados[2])
            self.complemento_entry.insert(0, dados[3] if dados[3] else "")
            self.bairro_entry.insert(0, dados[4])
            self.cep_entry.insert(0, dados[5])
            self.cidade_entry.insert(0, dados[6])
            self.estado_entry.insert(0, dados[7])
            self.atualizar_btn.config(state=tk.NORMAL)
            self.deletar_btn.config(state=tk.NORMAL)

    def novo_endereco(self):
        self.limpar_campos()
        self.salvar_btn.config(state=tk.NORMAL)
        self.logradouro_entry.focus()

    def limpar_campos(self):
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state='readonly')
        self.logradouro_entry.delete(0, tk.END)
        self.numero_entry.delete(0, tk.END)
        self.complemento_entry.delete(0, tk.END)
        self.bairro_entry.delete(0, tk.END)
        self.cep_entry.delete(0, tk.END)
        self.cidade_entry.delete(0, tk.END)
        self.estado_entry.delete(0, tk.END)
        self.salvar_btn.config(state=tk.DISABLED)
        self.atualizar_btn.config(state=tk.DISABLED)
        self.deletar_btn.config(state=tk.DISABLED)
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def validar_campos(self):
        campos_obrigatorios = [
            (self.logradouro_entry, "Logradouro"),
            (self.numero_entry, "Número"),
            (self.bairro_entry, "Bairro"),
            (self.cep_entry, "CEP"),
            (self.cidade_entry, "Cidade"),
            (self.estado_entry, "Estado")
        ]
        
        for campo, nome in campos_obrigatorios:
            if not campo.get().strip():
                messagebox.showerror("Erro", f"O campo {nome} é obrigatório!")
                campo.focus()
                return False
        
        if len(self.estado_entry.get()) != 2:
            messagebox.showerror("Erro", "O Estado deve ter exatamente 2 caracteres!")
            self.estado_entry.focus()
            return False
        
        return True

    def salvar_endereco(self):
        if not self.validar_campos():
            return

        try:
            query = """INSERT INTO Endereco 
                      (Logradouro, Numero, Complemento, Bairro, CEP, Cidade, Estado) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            valores = (
                self.logradouro_entry.get(),
                self.numero_entry.get(),
                self.complemento_entry.get() or None,
                self.bairro_entry.get(),
                self.cep_entry.get(),
                self.cidade_entry.get(),
                self.estado_entry.get().upper()
            )
            
            self.cursor.execute(query, valores)
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Endereço cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_enderecos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {str(e)}")

    def atualizar_endereco(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione um endereço para atualizar")
            return
        
        if not self.validar_campos():
            return

        try:
            query = f"""UPDATE Endereco SET 
                      Logradouro = %s,
                      Numero = %s,
                      Complemento = %s,
                      Bairro = %s,
                      CEP = %s,
                      Cidade = %s,
                      Estado = %s
                      WHERE {self.id_column} = %s"""
            valores = (
                self.logradouro_entry.get(),
                self.numero_entry.get(),
                self.complemento_entry.get() or None,
                self.bairro_entry.get(),
                self.cep_entry.get(),
                self.cidade_entry.get(),
                self.estado_entry.get().upper(),
                self.id_entry.get()
            )
            
            self.cursor.execute(query, valores)
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Endereço atualizado com sucesso!")
            self.carregar_enderecos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {str(e)}")

    def deletar_endereco(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione um endereço para deletar")
            return

        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar este endereço?"):
            return

        try:
            self.cursor.execute(f"DELETE FROM Endereco WHERE {self.id_column} = %s", (self.id_entry.get(),))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Endereço deletado com sucesso!")
            self.limpar_campos()
            self.carregar_enderecos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao deletar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnderecoApp(root)
    root.mainloop()
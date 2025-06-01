import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as conn
from tkinter import font as tkfont
from datetime import datetime
from os import system
system("cls")

class ExameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Médico - Exames")
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

        title_label = ttk.Label(main_frame, text="Gerenciamento de Exames", font=self.title_font)
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        search_frame = ttk.LabelFrame(main_frame, text=" Buscar Exames ", padding=10)
        search_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)
        
        ttk.Label(search_frame, text="Tipo:").grid(row=0, column=0, padx=5)
        self.search_type = ttk.Combobox(search_frame, values=["ID", "Tipo de Exame", "Paciente"], state="readonly")
        self.search_type.current(0)
        self.search_type.grid(row=0, column=1, padx=5, sticky="w")
        
        ttk.Label(search_frame, text="Valor:").grid(row=0, column=2, padx=5)
        self.search_value = ttk.Entry(search_frame, width=15)
        self.search_value.grid(row=0, column=3, padx=5, sticky="w")
        
        ttk.Button(search_frame, text="Buscar", command=self.buscar_por_tipo, style='Accent.TButton').grid(row=0, column=4, padx=5)

        form_frame = ttk.LabelFrame(main_frame, text=" Dados do Exame ", padding=15)
        form_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=10)

        campos = [
            ("ID:", "id_entry", True),
            ("Tipo de Exame*:", "tipo_exame_entry", False),
            ("Descrição:", "descricao_text", False),
            ("Valor Base*:", "valor_base_entry", False),
            ("Tempo Solicitado* (min):", "tempo_solicitado_entry", False),
            ("Paciente*:", "paciente_combobox", False),
            ("Médico*:", "medico_combobox", False),
            ("Data Solicitação*:", "data_solicitacao_entry", False)
        ]
        
        for i, (text, attr, readonly) in enumerate(campos):
            ttk.Label(form_frame, text=text).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            
            if attr == "descricao_text":
                entry = tk.Text(form_frame, height=4, width=30)
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            elif attr.endswith("combobox"):
                if "paciente" in attr:
                    values = self.pacientes_lista
                else:
                    values = self.medicos_lista
                entry = ttk.Combobox(form_frame, values=values, state="readonly")
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            else:
                entry = ttk.Entry(form_frame)
                if readonly:
                    entry.config(state='readonly')
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            
            setattr(self, attr, entry)

        # Configurar data atual como padrão
        self.data_solicitacao_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Novo", command=self.novo_exame).grid(row=0, column=0, padx=5)
        self.salvar_btn = ttk.Button(button_frame, text="Salvar", command=self.salvar_exame, state=tk.DISABLED)
        self.salvar_btn.grid(row=0, column=1, padx=5)
        self.atualizar_btn = ttk.Button(button_frame, text="Atualizar", command=self.atualizar_exame, state=tk.DISABLED)
        self.atualizar_btn.grid(row=0, column=2, padx=5)
        self.deletar_btn = ttk.Button(button_frame, text="Deletar", command=self.deletar_exame, state=tk.DISABLED)
        self.deletar_btn.grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.limpar_campos).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(main_frame, 
                               columns=("ID", "Tipo_Exame", "Paciente", "Medico", "Valor_Base", "Data_Solicitacao"), 
                               show="headings", height=12)
        self.tree.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=10)
        
        colunas = [
            ("ID", 50),
            ("Tipo_Exame", 150),
            ("Paciente", 200),
            ("Medico", 200),
            ("Valor_Base", 100),
            ("Data_Solicitacao", 120)
        ]
        
        for col, width in colunas:
            self.tree.heading(col, text=col.replace('_', ' '))
            self.tree.column(col, width=width, anchor="w")
        
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_exame)
        self.carregar_exames()

    def buscar_por_tipo(self):
        tipo = self.search_type.get()
        valor_busca = self.search_value.get()
        
        if not valor_busca:
            messagebox.showwarning("Aviso", "Digite um valor para buscar")
            return

        try:
            if tipo == "ID":
                self.cursor.execute("SELECT * FROM Exame WHERE ID = %s", (valor_busca,))
            elif tipo == "Tipo de Exame":
                self.cursor.execute("SELECT * FROM Exame WHERE TP_Exame LIKE %s", (f"%{valor_busca}%",))
            else:  # Paciente
                self.cursor.execute("""SELECT e.* FROM Exame e
                                      JOIN Paciente p ON e.Paciente_ID = p.ID
                                      WHERE p.Nome LIKE %s""", (f"%{valor_busca}%",))
            
            resultado = self.cursor.fetchone()
            
            if resultado:
                self.limpar_campos()
                self.id_entry.config(state='normal')
                self.id_entry.insert(0, resultado[0])
                self.id_entry.config(state='readonly')
                self.tipo_exame_entry.insert(0, resultado[1])
                self.descricao_text.delete('1.0', tk.END)
                self.descricao_text.insert('1.0', resultado[2] if resultado[2] else "")
                self.valor_base_entry.insert(0, f"{resultado[3]:.2f}")
                self.tempo_solicitado_entry.insert(0, resultado[4])
                
                # Carregar paciente
                self.cursor.execute("SELECT CONCAT(ID, ' - ', Nome) FROM Paciente WHERE ID = %s", (resultado[5],))
                paciente = self.cursor.fetchone()[0]
                self.paciente_combobox.set(paciente)
                
                # Carregar médico
                self.cursor.execute("SELECT CONCAT(ID, ' - ', Nome) FROM Medico WHERE ID = %s", (resultado[6],))
                medico = self.cursor.fetchone()[0]
                self.medico_combobox.set(medico)
                
                # Formatar data
                if resultado[7]:
                    data_formatada = resultado[7].strftime('%d/%m/%Y')
                    self.data_solicitacao_entry.delete(0, tk.END)
                    self.data_solicitacao_entry.insert(0, data_formatada)
                
                self.atualizar_btn.config(state=tk.NORMAL)
                self.deletar_btn.config(state=tk.NORMAL)
                
                self.carregar_exames(f"WHERE e.ID = {resultado[0]}")
            else:
                messagebox.showinfo("Informação", "Nenhum exame encontrado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar: {str(e)}")

    def carregar_exames(self, where_clause=""):
        self.tree.delete(*self.tree.get_children())
        try:
            query = f"""SELECT e.ID, e.TP_Exame, 
                        CONCAT(p.ID, ' - ', p.Nome) AS Paciente,
                        CONCAT(m.ID, ' - ', m.Nome) AS Medico,
                        e.Valor_Base, e.Data_Solicitacao
                        FROM Exame e
                        JOIN Paciente p ON e.Paciente_ID = p.ID
                        JOIN Medico m ON e.Medico_ID = m.ID
                        {where_clause} 
                        ORDER BY e.ID"""
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                # Formatar valor base e data
                formatted_row = list(row)
                formatted_row[4] = f"{row[4]:.2f}"
                formatted_row[5] = row[5].strftime('%d/%m/%Y')
                self.tree.insert("", "end", values=formatted_row)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar: {str(e)}")

    def selecionar_exame(self, event):
        item = self.tree.focus()
        if item:
            dados = self.tree.item(item)['values']
            self.limpar_campos()
            self.id_entry.config(state='normal')
            self.id_entry.insert(0, dados[0])
            self.id_entry.config(state='readonly')
            self.tipo_exame_entry.insert(0, dados[1])
            self.paciente_combobox.set(dados[2])
            self.medico_combobox.set(dados[3])
            self.valor_base_entry.insert(0, dados[4])
            self.data_solicitacao_entry.delete(0, tk.END)
            self.data_solicitacao_entry.insert(0, dados[5])
            self.atualizar_btn.config(state=tk.NORMAL)
            self.deletar_btn.config(state=tk.NORMAL)

    def novo_exame(self):
        self.limpar_campos()
        self.salvar_btn.config(state=tk.NORMAL)
        self.tipo_exame_entry.focus()
        # Configurar data atual como padrão
        self.data_solicitacao_entry.delete(0, tk.END)
        self.data_solicitacao_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

    def limpar_campos(self):
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state='readonly')
        self.tipo_exame_entry.delete(0, tk.END)
        self.descricao_text.delete('1.0', tk.END)
        self.valor_base_entry.delete(0, tk.END)
        self.tempo_solicitado_entry.delete(0, tk.END)
        self.paciente_combobox.set('')
        self.medico_combobox.set('')
        self.data_solicitacao_entry.delete(0, tk.END)
        self.salvar_btn.config(state=tk.DISABLED)
        self.atualizar_btn.config(state=tk.DISABLED)
        self.deletar_btn.config(state=tk.DISABLED)
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def validar_campos(self):
        if not self.tipo_exame_entry.get().strip():
            messagebox.showerror("Erro", "O campo Tipo de Exame é obrigatório!")
            self.tipo_exame_entry.focus()
            return False
        
        try:
            valor = float(self.valor_base_entry.get())
            if valor <= 0:
                messagebox.showerror("Erro", "O valor base deve ser maior que zero!")
                self.valor_base_entry.focus()
                return False
        except ValueError:
            messagebox.showerror("Erro", "Valor base inválido! Deve ser um número.")
            self.valor_base_entry.focus()
            return False
        
        try:
            tempo = int(self.tempo_solicitado_entry.get())
            if tempo <= 0:
                messagebox.showerror("Erro", "O tempo solicitado deve ser maior que zero!")
                self.tempo_solicitado_entry.focus()
                return False
        except ValueError:
            messagebox.showerror("Erro", "Tempo solicitado inválido! Deve ser um número inteiro.")
            self.tempo_solicitado_entry.focus()
            return False
        
        if not self.paciente_combobox.get():
            messagebox.showerror("Erro", "Selecione um paciente!")
            self.paciente_combobox.focus()
            return False
            
        if not self.medico_combobox.get():
            messagebox.showerror("Erro", "Selecione um médico!")
            self.medico_combobox.focus()
            return False
            
        try:
            datetime.strptime(self.data_solicitacao_entry.get(), '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Erro", "Data de solicitação inválida! Use o formato DD/MM/AAAA")
            self.data_solicitacao_entry.focus()
            return False
        
        return True

    def salvar_exame(self):
        if not self.validar_campos():
            return

        try:
            paciente_id = self.pacientes[self.paciente_combobox.get()]
            medico_id = self.medicos[self.medico_combobox.get()]
            data_solicitacao = datetime.strptime(self.data_solicitacao_entry.get(), '%d/%m/%Y').date()
            
            query = """INSERT INTO Exame 
                      (TP_Exame, Descricao, Valor_Base, Tempo_Solicitado, Paciente_ID, Medico_ID, Data_Solicitacao) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            valores = (
                self.tipo_exame_entry.get(),
                self.descricao_text.get('1.0', tk.END).strip() or None,
                float(self.valor_base_entry.get()),
                int(self.tempo_solicitado_entry.get()),
                paciente_id,
                medico_id,
                data_solicitacao
            )
            
            self.cursor.execute(query, valores)
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Exame cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_exames()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {str(e)}")

    def atualizar_exame(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione um exame para atualizar")
            return
        
        if not self.validar_campos():
            return

        try:
            paciente_id = self.pacientes[self.paciente_combobox.get()]
            medico_id = self.medicos[self.medico_combobox.get()]
            data_solicitacao = datetime.strptime(self.data_solicitacao_entry.get(), '%d/%m/%Y').date()
            
            query = """UPDATE Exame SET 
                      TP_Exame = %s,
                      Descricao = %s,
                      Valor_Base = %s,
                      Tempo_Solicitado = %s,
                      Paciente_ID = %s,
                      Medico_ID = %s,
                      Data_Solicitacao = %s
                      WHERE ID = %s"""
            valores = (
                self.tipo_exame_entry.get(),
                self.descricao_text.get('1.0', tk.END).strip() or None,
                float(self.valor_base_entry.get()),
                int(self.tempo_solicitado_entry.get()),
                paciente_id,
                medico_id,
                data_solicitacao,
                self.id_entry.get()
            )
            
            self.cursor.execute(query, valores)
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Exame atualizado com sucesso!")
            self.carregar_exames()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {str(e)}")

    def deletar_exame(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione um exame para deletar")
            return

        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar este exame?"):
            return

        try:
            self.cursor.execute("DELETE FROM Exame WHERE ID = %s", (self.id_entry.get(),))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Exame deletado com sucesso!")
            self.limpar_campos()
            self.carregar_exames()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao deletar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExameApp(root)
    root.mainloop()
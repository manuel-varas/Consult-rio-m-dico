import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as conn
from tkinter import font as tkfont
from os import system
system("cls")
class ConvenioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Médico - Convênios")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f8ff')
        
        try:
            self.conexao = conn.connect(
                host="localhost",
                user="root",
                password="M@taturu.1981",
                database="consultorio_medical"
            )
            self.cursor = self.conexao.cursor()
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

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Gerenciamento de Convênios", font=self.title_font)
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        search_frame = ttk.LabelFrame(main_frame, text=" Buscar Convênio ", padding=10)
        search_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)
        
        ttk.Label(search_frame, text="ID:").grid(row=0, column=0, padx=5)
        self.search_id = ttk.Entry(search_frame, width=15)
        self.search_id.grid(row=0, column=1, padx=5, sticky="w")
        
        ttk.Button(search_frame, text="Buscar", command=self.buscar_convenio, style='Accent.TButton').grid(row=0, column=2, padx=5)

        form_frame = ttk.LabelFrame(main_frame, text=" Dados do Convênio ", padding=15)
        form_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=10)

        campos = [
            ("ID:", "id_entry", True),
            ("Nome:", "nome_entry", False),
            ("CNPJ:", "cnpj_entry", False),
            ("Registro ANS:", "ans_entry", False)
        ]
        
        for i, (text, attr, readonly) in enumerate(campos):
            ttk.Label(form_frame, text=text).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(form_frame)
            if readonly:
                entry.config(state='readonly')
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            setattr(self, attr, entry)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Novo", command=self.novo_convenio).grid(row=0, column=0, padx=5)
        self.salvar_btn = ttk.Button(button_frame, text="Salvar", command=self.salvar_convenio, state=tk.DISABLED)
        self.salvar_btn.grid(row=0, column=1, padx=5)
        self.atualizar_btn = ttk.Button(button_frame, text="Atualizar", command=self.atualizar_convenio, state=tk.DISABLED)
        self.atualizar_btn.grid(row=0, column=2, padx=5)
        self.deletar_btn = ttk.Button(button_frame, text="Deletar", command=self.deletar_convenio, state=tk.DISABLED)
        self.deletar_btn.grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.limpar_campos).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(main_frame, 
                               columns=("ID", "Nome", "CNPJ", "Registro ANS"), 
                               show="headings", height=12)
        self.tree.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=10)
        
        for col in ("ID", "Nome", "CNPJ", "Registro ANS"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="w")
        
        self.tree.column("Nome", width=200)
        self.tree.column("CNPJ", width=150)
        
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_convenio)
        self.carregar_convenios()

    def buscar_convenio(self):
        id_convenio = self.search_id.get()
        if not id_convenio:
            messagebox.showwarning("Aviso", "Digite um ID para buscar")
            return

        try:
            self.cursor.execute("SELECT * FROM Convenio WHERE ID = %s", (id_convenio,))
            convenio = self.cursor.fetchone()
            
            if convenio:
                self.limpar_campos()
                self.id_entry.config(state='normal')
                self.id_entry.insert(0, convenio[0])
                self.id_entry.config(state='readonly')
                self.nome_entry.insert(0, convenio[1])
                self.cnpj_entry.insert(0, convenio[2])
                self.ans_entry.insert(0, convenio[3])
                
                self.atualizar_btn.config(state=tk.NORMAL)
                self.deletar_btn.config(state=tk.NORMAL)
            else:
                messagebox.showinfo("Informação", "Nenhum convênio encontrado com este ID")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar: {str(e)}")

    def carregar_convenios(self):
        self.tree.delete(*self.tree.get_children())
        try:
            self.cursor.execute("SELECT * FROM Convenio ORDER BY ID")
            for row in self.cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar: {str(e)}")

    def selecionar_convenio(self, event):
        item = self.tree.focus()
        if item:
            dados = self.tree.item(item)['values']
            self.limpar_campos()
            self.id_entry.config(state='normal')
            self.id_entry.insert(0, dados[0])
            self.id_entry.config(state='readonly')
            self.nome_entry.insert(0, dados[1])
            self.cnpj_entry.insert(0, dados[2])
            self.ans_entry.insert(0, dados[3])
            self.atualizar_btn.config(state=tk.NORMAL)
            self.deletar_btn.config(state=tk.NORMAL)

    def novo_convenio(self):
        self.limpar_campos()
        self.salvar_btn.config(state=tk.NORMAL)
        self.nome_entry.focus()

    def limpar_campos(self):
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state='readonly')
        self.nome_entry.delete(0, tk.END)
        self.cnpj_entry.delete(0, tk.END)
        self.ans_entry.delete(0, tk.END)
        self.salvar_btn.config(state=tk.DISABLED)
        self.atualizar_btn.config(state=tk.DISABLED)
        self.deletar_btn.config(state=tk.DISABLED)
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def validar_campos(self):
        if not self.nome_entry.get():
            messagebox.showerror("Erro", "Nome é obrigatório!")
            self.nome_entry.focus()
            return False
        
        if not self.cnpj_entry.get():
            messagebox.showerror("Erro", "CNPJ é obrigatório!")
            self.cnpj_entry.focus()
            return False
            
        if not self.ans_entry.get():
            messagebox.showerror("Erro", "Registro ANS é obrigatório!")
            self.ans_entry.focus()
            return False
            
        return True

    def formatar_cnpj(self, cnpj):
        cnpj = ''.join(filter(str.isdigit, cnpj))
        if len(cnpj) != 14:
            return cnpj
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

    def salvar_convenio(self):
        if not self.validar_campos():
            return

        try:
            cnpj_formatado = self.formatar_cnpj(self.cnpj_entry.get())
            
            query = """INSERT INTO Convenio 
                      (Nome, CNPJ, REG_ANS) 
                      VALUES (%s, %s, %s)"""
            valores = (
                self.nome_entry.get(),
                cnpj_formatado,
                self.ans_entry.get()
            )
            
            self.cursor.execute(query, valores)
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Convênio cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_convenios()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {str(e)}")

    def atualizar_convenio(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione um convênio para atualizar")
            return
        
        if not self.validar_campos():
            return

        try:
            cnpj_formatado = self.formatar_cnpj(self.cnpj_entry.get())
            
            query = """UPDATE Convenio SET 
                      Nome = %s,
                      CNPJ = %s,
                      REG_ANS = %s
                      WHERE ID = %s"""
            valores = (
                self.nome_entry.get(),
                cnpj_formatado,
                self.ans_entry.get(),
                self.id_entry.get()
            )
            
            self.cursor.execute(query, valores)
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Convênio atualizado com sucesso!")
            self.carregar_convenios()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {str(e)}")

    def deletar_convenio(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione um convênio para deletar")
            return

        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar este convênio?"):
            return

        try:
            self.cursor.execute("DELETE FROM Convenio WHERE ID = %s", (self.id_entry.get(),))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Convênio deletado com sucesso!")
            self.limpar_campos()
            self.carregar_convenios()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao deletar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConvenioApp(root)
    root.mainloop()
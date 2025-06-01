import tkinter as tk
from tkinter import ttk, messagebox, font
import mysql.connector
from datetime import datetime
from os import system
system("cls")

class SistemaPagamentos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Pagamentos")
        self.root.geometry("1350x750")
        self.root.configure(bg='#f0f8ff')
        self.conectar_banco_dados()
        self.configurar_interface()
        self.carregar_dados_referencia()
        self.criar_componentes()
        self.carregar_todos_pagamentos()

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
        self.opcoes_status = ['Pendente', 'Pago', 'Cancelado', 'Estornado']
        self.formas_pagamento = ['Dinheiro', 'Cartão Débito', 'Cartão Crédito', 'PIX', 'Transferência']

    def carregar_dados_referencia(self):
        try:
            self.cursor.execute("SELECT ID, Nome, CPF FROM Paciente ORDER BY Nome")
            self.pacientes = self.cursor.fetchall()
            self.lista_pacientes = [f"{p['ID']} - {p['Nome']} (CPF: {p['CPF']})" for p in self.pacientes]
            
            self.cursor.execute("SELECT ID, Data, Hora FROM Consulta ORDER BY Data DESC")
            self.consultas = self.cursor.fetchall()
            self.lista_consultas = [f"{c['ID']} - {c['Data']} {c['Hora']}" for c in self.consultas]
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados:\n{str(e)}")

    def criar_componentes(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        title = ttk.Label(main_frame, text="Gerenciamento de Pagamentos", font=self.fonte_titulo)
        title.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        self.criar_area_busca(main_frame)
        self.criar_formulario(main_frame)
        self.criar_botoes(main_frame)
        self.criar_tabela_resultados(main_frame)

    def criar_area_busca(self, parent):
        search_frame = ttk.LabelFrame(parent, text=" Buscar Pagamentos ", padding=10)
        search_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)
        ttk.Label(search_frame, text="Buscar por:").grid(row=0, column=0, padx=5)
        self.search_type = ttk.Combobox(search_frame, values=["ID", "Paciente", "Consulta", "Status", "Data"], state="readonly")
        self.search_type.current(0)
        self.search_type.grid(row=0, column=1, padx=5, sticky="w")
        ttk.Label(search_frame, text="Termo:").grid(row=0, column=2, padx=5)
        self.search_term = ttk.Entry(search_frame, width=25)
        self.search_term.grid(row=0, column=3, padx=5, sticky="w")
        ttk.Button(search_frame, text="Buscar", command=self.buscar_pagamentos, style='Accent.TButton').grid(row=0, column=4, padx=5)
        ttk.Button(search_frame, text="Limpar", command=self.limpar_busca).grid(row=0, column=5, padx=5)

    def criar_formulario(self, parent):
        form_frame = ttk.LabelFrame(parent, text=" Dados do Pagamento ", padding=15)
        form_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=10)
        campos = [
            ("ID:", "id_entry", True),
            ("Valor*:", "valor_entry", False),
            ("Data*:", "data_entry", False),
            ("Status*:", "status_combo", False),
            ("Forma Pagto*:", "forma_pagto_combo", False),
            ("Consulta*:", "consulta_combo", False),
            ("Paciente*:", "paciente_combo", False)
        ]
        for row, (label, field, readonly) in enumerate(campos):
            ttk.Label(form_frame, text=label).grid(row=row, column=0, sticky="e", padx=5, pady=5)
            if "combo" in field:
                values = self.opcoes_status if field == "status_combo" else self.formas_pagamento if field == "forma_pagto_combo" else self.lista_consultas if field == "consulta_combo" else self.lista_pacientes
                widget = ttk.Combobox(form_frame, values=values, state="readonly")
                widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            else:
                widget = ttk.Entry(form_frame)
                if readonly: widget.config(state='readonly')
                widget.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            setattr(self, field, widget)
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.status_combo.set('Pendente')
        self.forma_pagto_combo.set('Dinheiro')

    def criar_botoes(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        botoes = [
            ("Novo", self.novo_pagamento, 0),
            ("Salvar", self.salvar_pagamento, 1),
            ("Atualizar", self.atualizar_pagamento, 2),
            ("Cancelar", self.cancelar_pagamento, 3),
            ("Limpar", self.limpar_formulario, 4),
            ("Relatório", self.gerar_relatorio, 5)
        ]
        for text, command, col in botoes:
            btn = ttk.Button(btn_frame, text=text, command=command)
            if text in ["Salvar", "Atualizar", "Cancelar"]:
                btn.config(state=tk.DISABLED)
                setattr(self, f"{text.lower()}_btn", btn)
            btn.grid(row=0, column=col, padx=5)

    def criar_tabela_resultados(self, parent):
        columns = ("ID", "Valor", "Data", "Status", "Forma Pagto", "Consulta", "Paciente")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=15, selectmode="browse")
        col_widths = [50, 80, 100, 100, 120, 150, 250]
        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="w")
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=4, column=0, columnspan=4, sticky="nsew")
        scrollbar.grid(row=4, column=4, sticky="ns")
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_pagamento)

    def buscar_pagamentos(self):
        tipo = self.search_type.get()
        termo = self.search_term.get().strip()
        if not termo and tipo != "Status":
            messagebox.showwarning("Aviso", "Digite um termo para busca")
            return
        try:
            condicoes = ""
            if tipo == "ID": condicoes = f"WHERE p.ID = {termo}"
            elif tipo == "Paciente": condicoes = f"WHERE pac.Nome LIKE '%{termo}%' OR pac.CPF LIKE '%{termo}%'"
            elif tipo == "Consulta": condicoes = f"WHERE p.Consulta_ID = {termo.split(' - ')[0]}"
            elif tipo == "Status": condicoes = f"WHERE p.Status_Pgto = '{termo if termo else self.opcoes_status[0]}'"
            elif tipo == "Data":
                try:
                    data = datetime.strptime(termo, '%d/%m/%Y').date()
                    condicoes = f"WHERE p.Data = '{data}'"
                except ValueError:
                    messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
                    return
            self.carregar_pagamentos(condicoes)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na busca:\n{str(e)}")

    def limpar_busca(self):
        self.search_type.current(0)
        self.search_term.delete(0, tk.END)
        self.carregar_pagamentos()

    def carregar_pagamentos(self, condicoes=""):
        self.tree.delete(*self.tree.get_children())
        try:
            query = f"""SELECT p.ID, p.Valor, DATE_FORMAT(p.Data, '%d/%m/%Y') AS Data, p.Status_Pgto, 
                      p.Forma_Pgto, CONCAT('Consulta #', p.Consulta_ID) AS Consulta,
                      CONCAT(pac.ID, ' - ', pac.Nome, ' (CPF: ', pac.CPF, ')') AS Paciente
                      FROM Pagamento p
                      JOIN Paciente pac ON p.Paciente_ID = pac.ID
                      {condicoes} ORDER BY p.Data DESC"""
            self.cursor.execute(query)
            for pagamento in self.cursor.fetchall():
                self.tree.insert("", "end", values=(
                    pagamento['ID'],
                    f"R$ {pagamento['Valor']:.2f}",
                    pagamento['Data'],
                    pagamento['Status_Pgto'],
                    pagamento['Forma_Pgto'],
                    pagamento['Consulta'],
                    pagamento['Paciente']
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar pagamentos:\n{str(e)}")

    def selecionar_pagamento(self, event):
        item = self.tree.focus()
        if not item: return
        dados = self.tree.item(item)['values']
        self.limpar_formulario()
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, dados[0])
        self.id_entry.config(state='readonly')
        self.valor_entry.delete(0, tk.END)
        self.valor_entry.insert(0, dados[1].replace('R$ ', ''))
        self.data_entry.delete(0, tk.END)
        self.data_entry.insert(0, dados[2])
        self.status_combo.set(dados[3])
        self.forma_pagto_combo.set(dados[4])
        consulta = next((c for c in self.lista_consultas if c.startswith(dados[5].split('#')[1])), "")
        paciente = next((p for p in self.lista_pacientes if p.split(' - ')[0] == str(dados[6].split(' - ')[0])), "")
        self.consulta_combo.set(consulta)
        self.paciente_combo.set(paciente)
        self.atualizar_btn.config(state=tk.NORMAL)
        self.cancelar_btn.config(state=tk.NORMAL)
        self.salvar_btn.config(state=tk.DISABLED)

    def novo_pagamento(self):
        self.limpar_formulario()
        self.salvar_btn.config(state=tk.NORMAL)
        self.atualizar_btn.config(state=tk.DISABLED)
        self.cancelar_btn.config(state=tk.DISABLED)
        self.data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        self.status_combo.set('Pendente')
        self.forma_pagto_combo.set('Dinheiro')
        self.valor_entry.focus()

    def limpar_formulario(self):
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state='readonly')
        self.valor_entry.delete(0, tk.END)
        self.data_entry.delete(0, tk.END)
        self.status_combo.set('')
        self.forma_pagto_combo.set('')
        self.consulta_combo.set('')
        self.paciente_combo.set('')
        self.salvar_btn.config(state=tk.DISABLED)
        self.atualizar_btn.config(state=tk.DISABLED)
        self.cancelar_btn.config(state=tk.DISABLED)
        for item in self.tree.selection(): self.tree.selection_remove(item)

    def validar_campos(self):
        try:
            valor = float(self.valor_entry.get())
            if valor <= 0:
                messagebox.showerror("Erro", "Valor deve ser maior que zero!")
                self.valor_entry.focus()
                return False
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido! Use números com ponto decimal")
            self.valor_entry.focus()
            return False
        
        try:
            datetime.strptime(self.data_entry.get(), '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
            self.data_entry.focus()
            return False
        
        if not self.status_combo.get():
            messagebox.showerror("Erro", "Selecione um status!")
            self.status_combo.focus()
            return False
            
        if not self.forma_pagto_combo.get():
            messagebox.showerror("Erro", "Selecione uma forma de pagamento!")
            self.forma_pagto_combo.focus()
            return False
            
        if not self.consulta_combo.get():
            messagebox.showerror("Erro", "Selecione uma consulta!")
            self.consulta_combo.focus()
            return False
            
        if not self.paciente_combo.get():
            messagebox.showerror("Erro", "Selecione um paciente!")
            self.paciente_combo.focus()
            return False
        
        return True

    def salvar_pagamento(self):
        if not self.validar_campos(): return
        try:
            consulta_id = int(self.consulta_combo.get().split(' - ')[0])
            paciente_id = int(self.paciente_combo.get().split(' - ')[0])
            valor = float(self.valor_entry.get())
            data = datetime.strptime(self.data_entry.get(), '%d/%m/%Y').date()
            status = self.status_combo.get()
            forma_pgto = self.forma_pagto_combo.get()
            
            self.cursor.execute("INSERT INTO Pagamento (Valor, Data, Status_Pgto, Forma_Pgto, Consulta_ID, Paciente_ID) VALUES (%s, %s, %s, %s, %s, %s)", 
                              (valor, data, status, forma_pgto, consulta_id, paciente_id))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Pagamento registrado com sucesso!")
            self.limpar_formulario()
            self.carregar_pagamentos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar pagamento:\n{str(e)}")

    def atualizar_pagamento(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione um pagamento para editar")
            return
        if not self.validar_campos(): return
        try:
            pagamento_id = int(self.id_entry.get())
            consulta_id = int(self.consulta_combo.get().split(' - ')[0])
            paciente_id = int(self.paciente_combo.get().split(' - ')[0])
            valor = float(self.valor_entry.get())
            data = datetime.strptime(self.data_entry.get(), '%d/%m/%Y').date()
            status = self.status_combo.get()
            forma_pgto = self.forma_pagto_combo.get()
            
            self.cursor.execute("UPDATE Pagamento SET Valor = %s, Data = %s, Status_Pgto = %s, Forma_Pgto = %s, Consulta_ID = %s, Paciente_ID = %s WHERE ID = %s", 
                              (valor, data, status, forma_pgto, consulta_id, paciente_id, pagamento_id))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Pagamento atualizado com sucesso!")
            self.carregar_pagamentos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar pagamento:\n{str(e)}")

    def cancelar_pagamento(self):
        if not self.id_entry.get():
            messagebox.showerror("Erro", "Selecione um pagamento para cancelar")
            return
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja cancelar este pagamento?"): return
        try:
            pagamento_id = int(self.id_entry.get())
            self.cursor.execute("DELETE FROM Pagamento WHERE ID = %s", (pagamento_id,))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Pagamento cancelado com sucesso!")
            self.limpar_formulario()
            self.carregar_pagamentos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cancelar pagamento:\n{str(e)}")

    def gerar_relatorio(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um pagamento para gerar relatório")
            return
        dados = self.tree.item(item)['values']
        relatorio = tk.Toplevel(self.root)
        relatorio.title(f"Recibo de Pagamento #{dados[0]}")
        relatorio.geometry("600x400")
        texto = f"RECIBO DE PAGAMENTO\n{'='*30}\n\nCódigo: #{dados[0]}\nValor: {dados[1]}\nData: {dados[2]}\nStatus: {dados[3]}\nForma: {dados[4]}\n\nConsulta: {dados[5]}\nPaciente: {dados[6]}\n\n{'='*30}\nAssinatura: ________________________"
        text_widget = tk.Text(relatorio, wrap=tk.WORD, font=('Courier', 10))
        text_widget.insert('1.0', texto)
        text_widget.config(state='disabled')
        text_widget.pack(expand=True, fill='both', padx=10, pady=10)
        btn_fechar = ttk.Button(relatorio, text="Fechar", command=relatorio.destroy)
        btn_fechar.pack(pady=10)

    def carregar_todos_pagamentos(self):
        self.carregar_pagamentos()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaPagamentos(root)
    root.mainloop()
# 🏥 Sistema de Gerenciamento para Consultório Médico ⚕️

Este repositório contém o "Projeto Integrador Transdisciplinar em Banco de Dados I"[cite: 1], desenvolvido por Manuel Marcelo R. Varas (RGM: 40817270) [cite: 1] para o curso Técnico Superior em Banco de Dados da Cruzeiro do Sul Virtual[cite: 1]. O projeto foca na Situação-Problema 2[cite: 2], que consiste na criação de um sistema de banco de dados robusto e eficiente para um consultório médico[cite: 2].

O sistema visa otimizar a gestão de informações cruciais como pacientes 🧍, médicos 👨‍⚕️👩‍⚕️, consultas 🗓️, agendamentos ⏱️, exames 🔬, convênios 🤝 e aspectos financeiros 💰[cite: 3], garantindo a segurança 🔒 e eficiência ✅ no manuseio dos dados[cite: 3]. Adicionalmente, foram desenvolvidas interfaces gráficas em Python com Tkinter para proporcionar uma interação amigável e funcional com o banco de dados[cite: 4].

## ✨ Objetivos Principais ✨

* **Centralizar Informações:** Consolidar todos os dados do consultório em um único local 📂, facilitando o acesso e a gestão[cite: 6].
* **Proteção de Dados:** Implementar medidas para proteger os dados contra perdas 🛡️, incluindo a concepção de backups automatizados[cite: 7]. (Nota: A implementação de backup AWS S3 é um conceito do projeto[cite: 16]; os scripts fornecidos focam na aplicação e banco de dados local).
* **Agilizar Processos:** Otimizar rotinas administrativas como agendamentos 🚀, gerenciamento de prontuários (implícito) e faturamento 🧾[cite: 8].
* **Conformidade com LGPD:** Assegurar a privacidade e segurança das informações dos pacientes 👤, em alinhamento com a Lei Geral de Proteção de Dados[cite: 9].
* **Interface Intuitiva:** Oferecer uma interface de usuário clara e prática 🖱️ para facilitar a interação com o sistema[cite: 10].

## ⚙️ Funcionalidades Implementadas (Interfaces Gráficas) 🖥️

O sistema é modular, com interfaces dedicadas para o gerenciamento de diferentes entidades:

* **Gerenciamento de Agenda (`Agenda.py`):**
    * Cadastro ➕, busca 🔍, atualização 🔄 e exclusão 🗑️ de horários na agenda dos médicos.
    * Campos para data 📅, hora de início e fim ⏳, dia da semana 🗓️, status (Agendado, Confirmado, etc.), médico 👨‍⚕️ e observações 📝.
    * Validação de datas (não permitir datas passadas) e horários (hora fim maior que hora início).
* **Gerenciamento de Consultas (`Consulta.py`):**
    * Registro ➕, busca 🔍, atualização 🔄 e remoção 🗑️ de consultas.
    * Campos para data 📅, hora ⏳, status, paciente 🧍, médico 👨‍⚕️ e observações 📝.
    * Validação de datas e obrigatoriedade de campos.
* **Gerenciamento de Consultórios (`Consultorio.py`):**
    * CRUD (Create, Read, Update, Delete) para informações dos consultórios 🏢.
    * Campos para nome e ID do endereço associado 📍.
* **Gerenciamento de Convênios (`Convenio.py`):**
    * Administração de convênios médicos 🤝.
    * Campos para nome, CNPJ (com formatação) e registro ANS.
    * Validação de campos obrigatórios.
* **Gerenciamento de Endereços (`Endereco.py`):**
    * Cadastro ➕, busca 🔍, atualização 🔄 e exclusão 🗑️ de endereços 🗺️.
    * Integração com a API ViaCEP 📮 para busca automática de endereço a partir do CEP.
    * Campos para logradouro, número, complemento, bairro, CEP, cidade e estado.
    * Verifica e corrige a estrutura da tabela `Endereco` para incluir o campo `Bairro`, se necessário.
* **Gerenciamento de Exames (`Exame.py`):**
    * Registro ➕ e acompanhamento 👀 de exames solicitados 🧪.
    * Campos para tipo de exame, descrição 📝, valor base 💰, tempo solicitado ⏳, paciente 🧍, médico 👨‍⚕️ e data de solicitação 📅.
    * Validação de valores numéricos e datas.

## 🛠️ Tecnologias Utilizadas 💻

* **Banco de Dados:** MySQL 🐬.
    * Modelagem Relacional[cite: 12].
    * Normalização de Tabelas (até 3FN)[cite: 13, 20].
    * Criação de Constraints (Chaves Primárias 🔑 e Estrangeiras 🔗)[cite: 14].
* **Linguagem de Programação:** Python 🐍.
    * **Interface Gráfica:** Tkinter[cite: 18, 30].
    * **Conexão com Banco de Dados:** `mysql-connector-python`[cite: 18, 31].
    * **Requisições HTTP:** `requests` (para a API ViaCEP no `Endereco.py`).
* **Modelagem Conceitual:** BrModelo (para o Diagrama Entidade-Relacionamento - DER)[cite: 25].

## 🗂️ Estrutura do Banco de Dados (`consultorio_medico.sql`) 📊

O banco de dados `consultorio_medical` é composto pelas seguintes tabelas principais[cite: 36]:

* `Endereco` 📍
* `Convenio` 🤝
* `Medico` 👨‍⚕️👩‍⚕️ (inclui campo `Nome` adicionado via `UPDATE` no script SQL)
* `Consultorio` 🏢
* `Paciente` 🧍
* `Exame` 🧪
* `Agenda` 🗓️
* `Consulta` ⏱️
* `Pagamento` 💰
* Tabelas de relacionamento (NN): `Paciente_Exame`, `Medico_Exame`, `Medico_Clinica`, `Medico_Paciente`.

O script SQL fornecido (`consultorio_medico.sql`) cria o schema, as tabelas, insere dados de exemplo e realiza algumas atualizações e exclusões demonstrativas[cite: 26, 34].

## ⚙️ Configuração e Execução ▶️

1.  **Pré-requisitos:**
    * Python 3.x.
    * Servidor MySQL instalado e em execução.
    * As seguintes bibliotecas Python: `mysql-connector-python`, `requests`.
        ```bash
        pip install mysql-connector-python requests
        ```

2.  **Configuração do Banco de Dados:**
    * Crie um banco de dados no MySQL chamado `consultorio_medical`.
    * Execute o script `consultorio_medico.sql` para criar as tabelas e popular com dados iniciais.
        ```bash
        mysql -u seu_usuario -p consultorio_medical < consultorio_medico.sql
        ```
    * **Importante:** Verifique e, se necessário, altere a senha de conexão com o banco de dados MySQL dentro de cada arquivo Python (`.py`)[cite: 32, 33]. A senha padrão utilizada no código é `"M@taturu.1981"`[cite: 33].
        Procure pela linha:
        ```python
        password="M@taturu.1981",
        ```
        em arquivos como `Agenda.py`, `Consulta.py`, etc., e ajuste conforme suas credenciais do MySQL.

3.  **Executar as Aplicações:**
    Navegue até o diretório do projeto e execute os módulos individualmente:
    ```bash
    python Agenda.py
    python Consulta.py
    # e assim por diante para os outros módulos.
    ```

## 📂 Estrutura do Projeto 🌳

* `Agenda.py`: Interface para gerenciamento da agenda médica 🗓️.
* `conexao.py`: Script simples para testar a conexão com o banco de dados (não utilizado pelas interfaces principais) 🔗.
* `Consulta.py`: Interface para gerenciamento de consultas ⏱️.
* `Consultorio.py`: Interface para gerenciamento de consultórios 🏢.
* `consultorio_DIAGRAMA.drawio.png`: Diagrama Entidade-Relacionamento do banco de dados 📊[cite: 25, 48].
* `consultorio_medico.sql`: Script SQL para criação e população do banco de dados 💾[cite: 26, 34, 48].
* `Convenio.py`: Interface para gerenciamento de convênios 🤝.
* `Descrição detalhada Projeto.pdf`: Documento descritivo do projeto 📄.
* `Endereco.py`: Interface para gerenciamento de endereços 🗺️.
* `Exame.py`: Interface para gerenciamento de exames 🧪.
    *(Os arquivos Python listados também são referenciados como Anexo 3 nos documentos do projeto)*[cite: 34, 48].

## 🚀 Melhorias Futuras Sugeridas (Conforme Documentação do Projeto) 💡

* Integração com um front-end web 🌐/mobile 📱[cite: 40].
* Implementação de triggers para auditoria 📝[cite: 41].
* Possível migração para Amazon Aurora para escalabilidade ☁️[cite: 42].
* Aprimoramento contínuo das interfaces Python ✨[cite: 43].

## 🎉 Conclusão do Projeto (Original) ✅

Este projeto demonstrou a aplicação prática dos conhecimentos em banco de dados para resolver um problema real[cite: 45], contribuindo para a organização ⚙️, segurança 🔒 e eficiência ✅ da gestão de informações em um consultório médico[cite: 46]. A adição das interfaces em Python agregou valor significativo, evidenciando a importância da integração entre banco de dados e a camada de apresentação 🖥️[cite: 47].

---

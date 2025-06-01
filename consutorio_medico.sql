
CREATE DATABASE IF NOT EXISTS consultorio_medical;
USE consultorio_medical;


CREATE TABLE Endereco (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Logradouro VARCHAR(100) NOT NULL,
    Numero VARCHAR(10) NOT NULL,
    Complemento VARCHAR(50),
    CEP VARCHAR(10) NOT NULL,
    Cidade VARCHAR(50) NOT NULL,
    Estado VARCHAR(2) NOT NULL
);

CREATE TABLE Convenio (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    CNPJ VARCHAR(18) UNIQUE NOT NULL,
    REG_ANS VARCHAR(20) NOT NULL
);

CREATE TABLE Medico (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    CRM VARCHAR(20) UNIQUE NOT NULL,
    Especialidade VARCHAR(50) NOT NULL,
    Endereco_ID INT,
    FOREIGN KEY (Endereco_ID) REFERENCES Endereco(ID)
);

CREATE TABLE Consultorio (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Endereco_ID INT,
    FOREIGN KEY (Endereco_ID) REFERENCES Endereco(ID)
);

CREATE TABLE Paciente (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Email VARCHAR(100),
    Telefone VARCHAR(20),
    CPF VARCHAR(14) UNIQUE,
    Data_Nascimento DATE,
    Convenio_ID INT,
    Endereco_ID INT,
    FOREIGN KEY (Convenio_ID) REFERENCES Convenio(ID),
    FOREIGN KEY (Endereco_ID) REFERENCES Endereco(ID)
);

CREATE TABLE Exame (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    TP_Exame VARCHAR(50) NOT NULL,
    Descricao TEXT,
    Valor_Base DECIMAL(10,2) NOT NULL,
    Tempo_Solicitado INT NOT NULL
);

CREATE TABLE Agenda (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Data DATE NOT NULL,
    Hora_inicio TIME NOT NULL,
    Hora_fim TIME NOT NULL,
    Dia_semana VARCHAR(20),
    Status VARCHAR(20) NOT NULL,
    Observacao TEXT,
    Medico_ID INT NOT NULL,
    FOREIGN KEY (Medico_ID) REFERENCES Medico(ID)
);

CREATE TABLE Consulta (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Data DATE NOT NULL,
    Hora TIME NOT NULL,
    Status VARCHAR(20) NOT NULL,
    Observacao TEXT,
    Paciente_ID INT NOT NULL,
    Medico_ID INT NOT NULL,
    FOREIGN KEY (Paciente_ID) REFERENCES Paciente(ID),
    FOREIGN KEY (Medico_ID) REFERENCES Medico(ID)
);

CREATE TABLE Pagamento (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Valor DECIMAL(10,2) NOT NULL,
    Data DATE NOT NULL,
    Status_Pgto VARCHAR(20) NOT NULL,
    Forma_Pgto VARCHAR(20) NOT NULL,
    Consulta_ID INT NOT NULL,
    Paciente_ID INT NOT NULL,
    FOREIGN KEY (Consulta_ID) REFERENCES Consulta(ID),
    FOREIGN KEY (Paciente_ID) REFERENCES Paciente(ID)
);


CREATE TABLE Paciente_Exame (
    Paciente_ID INT NOT NULL,
    Exame_ID INT NOT NULL,
    PRIMARY KEY (Paciente_ID, Exame_ID),
    FOREIGN KEY (Paciente_ID) REFERENCES Paciente(ID),
    FOREIGN KEY (Exame_ID) REFERENCES Exame(ID)
);

CREATE TABLE Medico_Exame (
    Medico_ID INT NOT NULL,
    Exame_ID INT NOT NULL,
    PRIMARY KEY (Medico_ID, Exame_ID),
    FOREIGN KEY (Medico_ID) REFERENCES Medico(ID),
    FOREIGN KEY (Exame_ID) REFERENCES Exame(ID)
);

CREATE TABLE Medico_Clinica (
    Medico_ID INT NOT NULL,
    Consultorio_ID INT NOT NULL,
    PRIMARY KEY (Medico_ID, Consultorio_ID),
    FOREIGN KEY (Medico_ID) REFERENCES Medico(ID),
    FOREIGN KEY (Consultorio_ID) REFERENCES Consultorio(ID)
);

CREATE TABLE Medico_Paciente (
    Medico_ID INT NOT NULL,
    Paciente_ID INT NOT NULL,
    PRIMARY KEY (Medico_ID, Paciente_ID),
    FOREIGN KEY (Medico_ID) REFERENCES Medico(ID),
    FOREIGN KEY (Paciente_ID) REFERENCES Paciente(ID)
);


INSERT INTO Endereco (Logradouro, Numero, Complemento, CEP, Cidade, Estado) VALUES
('Rua das Flores', '123', 'Apto 101', '01234-567', 'São Paulo', 'SP'),
('Avenida Brasil', '456', 'Sala 202', '04567-890', 'São Paulo', 'SP'),
('Rua das Palmeiras', '789', '', '07890-123', 'Rio de Janeiro', 'RJ'),
('Avenida Paulista', '1000', 'Conjunto 303', '01310-100', 'São Paulo', 'SP'),
('Rua dos Pinheiros', '200', 'Casa 2', '05422-000', 'São Paulo', 'SP');

INSERT INTO Convenio (Nome, CNPJ, REG_ANS) VALUES
('Amil Saúde', '12.345.678/0001-99', '123456'),
('Bradesco Saúde', '98.765.432/0001-11', '654321'),
('SulAmérica', '45.678.912/0001-34', '789123'),
('Unimed', '32.165.498/0001-76', '321654'),
('NotreDame Intermédica', '65.432.198/0001-87', '654987');

INSERT INTO Medico (CRM, Especialidade, Endereco_ID) VALUES
('CRM/SP 123456', 'Cardiologia', 1),
('CRM/SP 654321', 'Pediatria', 2),
('CRM/RJ 789123', 'Ortopedia', 3),
('CRM/SP 321654', 'Dermatologia', 4),
('CRM/SP 987654', 'Neurologia', 5);

INSERT INTO Consultorio (Nome, Endereco_ID) VALUES
('Clínica Cardiológica', 1),
('Pediatria Infantil', 2),
('Ortopedia e Traumatologia', 3),
('Dermatologia Avançada', 4),
('Neurologia e Neurocirurgia', 5);

INSERT INTO Paciente (Nome, Email, Telefone, CPF, Data_Nascimento, Convenio_ID, Endereco_ID) VALUES
('João Silva', 'joao@email.com', '(11) 9999-8888', '123.456.789-00', '1980-05-15', 1, 1),
('Maria Souza', 'maria@email.com', '(11) 9999-7777', '987.654.321-00', '1985-08-20', 2, 2),
('Carlos Oliveira', 'carlos@email.com', '(21) 9999-6666', '456.789.123-00', '1975-03-10', 3, 3),
('Ana Santos', 'ana@email.com', '(11) 9999-5555', '321.654.987-00', '1990-11-25', 4, 4),
('Pedro Costa', 'pedro@email.com', '(11) 9999-4444', '654.321.987-00', '1970-07-30', 5, 5);

INSERT INTO Exame (TP_Exame, Descricao, Valor_Base, Tempo_Solicitado) VALUES
('Hemograma', 'Análise de células sanguíneas', 120.00, 1),
('Glicemia', 'Medição de açúcar no sangue', 80.00, 1),
('Colesterol', 'Perfil lipídico completo', 150.00, 1),
('Raio-X', 'Imagem de raio-X da área solicitada', 200.00, 2),
('Eletrocardiograma', 'Registro da atividade elétrica do coração', 250.00, 1);

INSERT INTO Agenda (Data, Hora_inicio, Hora_fim, Dia_semana, Status, Observacao, Medico_ID) VALUES
('2023-06-01', '08:00:00', '12:00:00', 'Segunda', 'Livre', 'Atendimento normal', 1),
('2023-06-01', '14:00:00', '18:00:00', 'Segunda', 'Livre', 'Atendimento normal', 2),
('2023-06-02', '09:00:00', '13:00:00', 'Terça', 'Livre', 'Atendimento normal', 3),
('2023-06-02', '15:00:00', '19:00:00', 'Terça', 'Livre', 'Atendimento normal', 4),
('2023-06-03', '10:00:00', '14:00:00', 'Quarta', 'Livre', 'Atendimento normal', 5);

INSERT INTO Consulta (Data, Hora, Status, Observacao, Paciente_ID, Medico_ID) VALUES
('2023-06-01', '09:00:00', 'Agendado', 'Consulta de rotina', 1, 1),
('2023-06-01', '15:00:00', 'Agendado', 'Acompanhamento', 2, 2),
('2023-06-02', '10:00:00', 'Agendado', 'Retorno', 3, 3),
('2023-06-02', '16:00:00', 'Cancelado', 'Paciente desmarcou', 4, 4),
('2023-06-03', '11:00:00', 'Realizado', 'Exame físico completo', 5, 5);

INSERT INTO Pagamento (Valor, Data, Status_Pgto, Forma_Pgto, Consulta_ID, Paciente_ID) VALUES
(250.00, '2023-06-01', 'Pago', 'Cartão', 1, 1),
(200.00, '2023-06-01', 'Pago', 'Dinheiro', 2, 2),
(180.00, '2023-06-02', 'Cancelado', 'Boleto', 3, 3),
(300.00, '2023-06-02', 'Pendente', 'Cartão', 4, 4),
(280.00, '2023-06-03', 'Pago', 'PIX', 5, 5);


INSERT INTO Paciente_Exame (Paciente_ID, Exame_ID) VALUES
(1, 1),
(1, 5),
(2, 2),
(3, 3),
(4, 4);

INSERT INTO Medico_Exame (Medico_ID, Exame_ID) VALUES
(1, 5),
(2, 1),
(3, 4),
(4, 1),
(5, 5);

INSERT INTO Medico_Clinica (Medico_ID, Consultorio_ID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

INSERT INTO Medico_Paciente (Medico_ID, Paciente_ID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);


UPDATE Paciente SET Telefone = '(11) 9888-7777' WHERE ID = 1;
UPDATE Consulta SET Status = 'Realizado' WHERE ID = 1;
UPDATE Exame SET Valor_Base = 130.00 WHERE ID = 1;
UPDATE Pagamento SET Status_Pgto = 'Pago' WHERE ID = 4;
UPDATE Agenda SET Status = 'Ocupado' WHERE ID = 1;


DELETE FROM Paciente_Exame WHERE Paciente_ID = 1 AND Exame_ID = 1;
DELETE FROM Medico_Paciente WHERE Medico_ID = 1 AND Paciente_ID = 1;
DELETE FROM Pagamento WHERE ID = 3;
DELETE FROM Pagamento WHERE Consulta_ID = 4;
DELETE FROM Consulta WHERE ID = 4;
DELETE FROM Agenda WHERE ID = 5;


UPDATE Medico SET Nome = 'Dr. Carlos Silva' WHERE CRM = 'CRM/SP 123456';
UPDATE Medico SET Nome = 'Dra. Ana Oliveira' WHERE CRM = 'CRM/SP 654321';
UPDATE Medico SET Nome = 'Dr. Marcos Souza' WHERE CRM = 'CRM/RJ 789123';
UPDATE Medico SET Nome = 'Dra. Juliana Costa' WHERE CRM = 'CRM/SP 321654';
UPDATE Medico SET Nome = 'Dr. Roberto Almeida' WHERE CRM = 'CRM/SP 987654';
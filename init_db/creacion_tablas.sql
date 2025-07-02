
CREATE TABLE Partido_Politico (
ID INT PRIMARY KEY AUTO_INCREMENT,
Nombre VARCHAR(100) NOT NULL,
Dir_Sede VARCHAR(200)
);

CREATE TABLE Evento_Electoral (
ID INT PRIMARY KEY,
Tipo VARCHAR(50) NOT NULL,
Fecha DATE NOT NULL
);

CREATE TABLE Partido_Politico (
ID INT PRIMARY KEY,
Dir_Sede VARCHAR(200)
);

CREATE TABLE Comisaria (
ID INT PRIMARY KEY,
Direccion VARCHAR(200),
ID_Departamento INT,
FOREIGN KEY (ID_Departamento) REFERENCES Departamento(ID)
);

CREATE TABLE Zona (
ID INT PRIMARY KEY,
Nombre VARCHAR(100) NOT NULL,
Tipo VARCHAR(50),
ID_Departamento INT,
FOREIGN KEY (ID_Departamento) REFERENCES Departamento(ID)
);

CREATE TABLE Establecimiento (
ID INT PRIMARY KEY,
Nombre VARCHAR(100) NOT NULL,
Direccion VARCHAR(200),
Tipo VARCHAR(50),
ID_Zona INT,
FOREIGN KEY (ID_Zona) REFERENCES Zona(ID)
);

CREATE TABLE Circuito (
ID INT PRIMARY KEY,
Accesible BOOLEAN,
Serie VARCHAR(20),
Desde INT,
Hasta INT,
ID_Establecimiento INT,
FOREIGN KEY (ID_Establecimiento) REFERENCES Establecimiento(ID)
);

CREATE TABLE Mesa (
ID INT PRIMARY KEY,
Total_Votos_Emitidos INT DEFAULT 0,
ID_Circuito INT,
FOREIGN KEY (ID_Circuito) REFERENCES Circuito(ID)
);

CREATE TABLE Lista (
Numero INT PRIMARY KEY,
ID_Departamento INT,
ID_Partido INT,
ID_Evento_Electoral INT,
FOREIGN KEY (ID_Departamento) REFERENCES Departamento(ID),
FOREIGN KEY (ID_Partido) REFERENCES Partido_Politico(ID),
FOREIGN KEY (ID_Evento_Electoral) REFERENCES Evento_Electoral(ID)
);

CREATE TABLE Ciudadano (
CI VARCHAR(20) PRIMARY KEY,
CC VARCHAR(20),
Nombre VARCHAR(100) NOT NULL,
Apellido VARCHAR(100) NOT NULL,
F_Nacimiento DATE,
Numero_Lista INT,
FOREIGN KEY (Numero_Lista) REFERENCES Lista(Numero)
);

CREATE TABLE Votante (
CI VARCHAR(20) PRIMARY KEY,
Habilitado BOOLEAN DEFAULT TRUE,
Voto BOOLEAN DEFAULT FALSE,
Token_Inicial VARCHAR(100)
FOREIGN KEY (CI) REFERENCES Ciudadano(CI)
);

CREATE TABLE Candidato (
CI VARCHAR(20) PRIMARY KEY,
Organo VARCHAR(100),
Cargo VARCHAR(100),
Lugar_En_Lista INT,
ID_Partido INT NOT NULL,
FOREIGN KEY (CI) REFERENCES Ciudadano(CI),
FOREIGN KEY (ID_Partido) REFERENCES Partido_Politico(ID)
);

CREATE TABLE Empleado_Publico (
CI VARCHAR(20) PRIMARY KEY,
Organismo_De_Trabajo VARCHAR(150),
Rol_En_Mesa VARCHAR(50),
ID_Mesa INT,
FOREIGN KEY (CI) REFERENCES Ciudadano(CI),
FOREIGN KEY (ID_Mesa) REFERENCES Mesa(ID)
);

CREATE TABLE Policia (
CI VARCHAR(20) PRIMARY KEY,
ID_Establecimiento INT,
ID_Comisaria INT,
FOREIGN KEY (CI) REFERENCES Ciudadano(CI),
FOREIGN KEY (ID_Establecimiento) REFERENCES Establecimiento(ID),
FOREIGN KEY (ID_Comisaria) REFERENCES Comisaria(ID)
);

CREATE TABLE Autoridad (
ID_Partido INT,
CI_Autoridad VARCHAR(20),
PRIMARY KEY (ID_Partido, CI_Autoridad),
FOREIGN KEY (ID_Partido) REFERENCES Partido_Politico(ID),
FOREIGN KEY (CI_Autoridad) REFERENCES Ciudadano(CI)
);

CREATE TABLE Admin (
  CI VARCHAR(20) PRIMARY KEY,
  Usuario VARCHAR(50) UNIQUE NOT NULL,
  Password_Hash VARCHAR(255) NOT NULL,
  FOREIGN KEY (CI) REFERENCES Ciudadano(CI)
);


CREATE TABLE Voto (
ID_Voto INT PRIMARY KEY,
En_Blanco BOOLEAN DEFAULT FALSE,
Anulado BOOLEAN DEFAULT FALSE,
Observado BOOLEAN DEFAULT FALSE,
Fecha_Hora DATETIME,
Numero_Lista INT,
ID_Circuito INT NOT NULL,
FOREIGN KEY (Numero_Lista) REFERENCES Lista(Numero),
FOREIGN KEY (ID_Circuito) REFERENCES Circuito(ID)
);

CREATE TABLE Votante_Participa_Evento (
CI_Votante VARCHAR(20),
ID_Evento_Electoral INT,
PRIMARY KEY (CI_Votante, ID_Evento_Electoral),
FOREIGN KEY (CI_Votante) REFERENCES Votante(CI),
FOREIGN KEY (ID_Evento_Electoral) REFERENCES Evento_Electoral(ID)
);

CREATE TABLE Participa_En (
ID_EventoElectoral INT,
ID_Partido INT,
PRIMARY KEY (ID_EventoElectoral, ID_Partido),
FOREIGN KEY (ID_EventoElectoral) REFERENCES Evento_Electoral(ID),
FOREIGN KEY (ID_Partido) REFERENCES Partido_Politico(ID)
);


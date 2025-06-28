import logo from './logo.svg';
import './App.css';

import React, { useEffect, useState } from "react";

const App = () => {
  const [mensaje, setMensaje] = useState("Cargando...");
  const [dbStatus, setDbStatus] = useState("Verificando...");

  useEffect(() => {
    fetch("http://localhost:5000/")
      .then((res) => res.text())
      .then((data) => setMensaje(data))
      .catch(() => setMensaje("Error al conectar con el backend."));

    fetch("http://localhost:5000/dbcheck")
      .then((res) => res.text())
      .then((data) => setDbStatus(data))
      .catch(() => setDbStatus("Error al verificar la base de datos."));
  }, []);

  return (
    <div>
      <h1>Backend:</h1>
      <p>{mensaje}</p>

      <h2>Estado de la base de datos:</h2>
      <p>{dbStatus}</p>
    </div>
  );
};

export default App;


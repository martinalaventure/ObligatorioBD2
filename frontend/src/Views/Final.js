// src/Views/Final.jsx
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../Styles/Final.css';

const Final = () => {
  const navigate = useNavigate();

  useEffect(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("serie");
    localStorage.removeItem("circuito");
    localStorage.removeItem("observado");
  }, []);

  const handleVolver = () => {
    navigate('/login/votante');
  };

  return (
    <div className="final-container">
      <h2>¡Gracias por votar!</h2>
      <p>Tu voto ha sido registrado con éxito.</p>
      <button onClick={handleVolver} className="volver-button">
        Volver al login
      </button>
    </div>
  );
};

export default Final;

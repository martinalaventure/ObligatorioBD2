/*
Acá es para hacer las card que queramos, es para tener una base nomas
Lo llamamos desde la view que vaya a implementarlo y le pasamos los parametros que queramos ahí
Hay que cambiar las cosas de game, lo saqué de una practica de parcial de desarrollo :)
*/

import React from "react";
import { useNavigate } from "react-router-dom";
import "../Styles/Card.css";

export default function Card({ id, title, children }) {
  const navigate = useNavigate();

  const handleDetailsClick = () => {
    navigate(`/listas/${id}`);
  };

  return (
    <div className="card">
      <div className="content-contenedor">
        <div className="card-title">
          <h2>{title}</h2>
        </div>
        <div className="little-description">
          {children}
        </div>
        <button className="detail-btn" onClick={handleDetailsClick}>
          Detalles
        </button>
      </div>
    </div>
  );
}

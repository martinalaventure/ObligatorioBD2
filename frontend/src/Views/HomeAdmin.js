import React from "react";
import { Link, Navigate } from "react-router-dom";
import "../Styles/HomeAdmin.css";
import LogoutButton from "../Components/LogoutButton";

const HomeAdmin = () => {
  return (
    <div className="home-admin-container">
      <LogoutButton />
      <div className="home-admin-buttons">
        <Link to="/resultados/oficiales" className="admin-btn">
          Ver Resultados Oficiales
        </Link>

        <Link to="/escrutinio/nacional" className="admin-btn">
          Ver Escrutinio Nacional
        </Link>

        <a
          href="http://localhost:5000/auditoria/reporte"
          className="admin-btn"
          download
        >
          Descargar Auditoría
        </a>
      </div>
    </div>
  );
};

export default HomeAdmin;

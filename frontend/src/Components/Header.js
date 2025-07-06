import React from "react";
import { useLocation } from "react-router-dom";
import "../Styles/App.css";

const Header = () => {
  const location = useLocation();

  const getPageTitle = () => {
    const path = location.pathname;

    if (path === "/presidente") return "Página Principal";
    if (path === "/listas") return "Elegir Opción A Votar";
    if (path.startsWith("/listas/")) return "Votar";
    if (path === "/home/admin") return "Home Administrador";
    if (path === "/login/votante") return null;
  };

  return (
    <header className="App-header">
      <h1>{getPageTitle()}</h1>
    </header>
  );
};

export default Header;

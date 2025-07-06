import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../Styles/LogoutButton.css';

const LogoutButton = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('presidente_ci');
    navigate('/');
  };

  return (
    <button onClick={handleLogout} className="logout-button">
      Cerrar sesión
    </button>
  );
};

export default LogoutButton;

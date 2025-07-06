import React from 'react';
import { Navigate } from 'react-router-dom';

const RutaProtegida = ({ children }) => {
  const token = localStorage.getItem('token');
  console.log("Token en RutaProtegida:", token);

  if (!token) {
    return <Navigate to="/" replace />;
  }

  return children;
};

export default RutaProtegida;

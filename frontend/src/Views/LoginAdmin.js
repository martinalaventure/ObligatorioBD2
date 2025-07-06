import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../Styles/LoginAdmin.css';

const LoginAdmin = () => {
  const [usuario, setUsuario] = useState('');
  const [contrasena, setContrasena] = useState('');
  const [mensaje, setMensaje] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/login/admin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ usuario, contrasena })
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('adminToken', data.token);
        navigate('/resultadosElecciones');
      } else {
        setMensaje(data.error || 'Usuario o contraseña incorrectos');
      }
    } catch (error) {
      setMensaje('No se pudo conectar con el servidor.');
    }
  };

  return (
    <div id="admin-login-container">
      <h2 className="admin-login-title">Login Administrador</h2>
      <form onSubmit={handleLogin} className="admin-login-form">
        <div className="form-group">
          <label htmlFor="usuario">Usuario:</label>
          <input
            id="usuario"
            type="text"
            value={usuario}
            onChange={(e) => setUsuario(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="contrasena">Contraseña:</label>
          <input
            id="contrasena"
            type="password"
            value={contrasena}
            onChange={(e) => setContrasena(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="admin-login-button">Iniciar sesión</button>

        <div className="extra-login-buttons-admin">
            <button className="alt-login-button-admin" onClick={() => navigate('/login/votante')}>
            Iniciar sesión como votante
            </button>
            <button className="alt-login-button-admin" onClick={() => navigate('/login/presidente')}>
            Iniciar sesión como presidente de mesa
            </button>
        </div>

        {mensaje && <p className="admin-login-message">{mensaje}</p>}
      </form>
    </div>
  );
};

export default LoginAdmin;

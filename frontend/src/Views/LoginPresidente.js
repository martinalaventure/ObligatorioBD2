import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../Styles/LoginPresidente.css';

const LoginPresidente = () => {
  const [usuario, setUsuario] = useState('');
  const [contrasena, setContrasena] = useState('');
  const [mensaje, setMensaje] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/login/presidente', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ usuario, contrasena })
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('presidente_ci', data.ci);
        navigate('/presidente');
      } else {
        setMensaje(data.error || 'Usuario o contraseña incorrectos');
      }
    } catch (error) {
      setMensaje('No se pudo conectar con el servidor.');
    }
  };

  return (
    <div id="presidente-login-container">
      <h2 className="presidente-login-title">Login presidente</h2>
      <form onSubmit={handleLogin} className="presidente-login-form">
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
        <button type="submit" className="presidente-login-button">Iniciar sesión</button>

        <div className="extra-login-buttons-presidente">
            <button className="alt-login-button-presidente" onClick={() => navigate('/login/votante')}>
            Iniciar sesión como votante
            </button>
            <button className="alt-login-button-presidente" onClick={() => navigate('/login/admin')}>
            Iniciar sesión como admin
            </button>
        </div>

        {mensaje && <p className="presidente-login-message">{mensaje}</p>}
      </form>
    </div>
  );
};

export default LoginPresidente;
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../Styles/LoginVotante.css'; 

const LoginVotante = () => {
  const [cc, setCc] = useState('');
  const [circuito, setCircuito] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/login/votante', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          cc,
          circuito_id: circuito
        })
      });

      const data = await response.json();


      if (response.ok) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('circuito', data.circuito);
        localStorage.setItem('serie', data.serie);
        localStorage.setItem('observado', data.observado);
        setUserData(data.serie);
        navigate('/listas');
      } else {
        setMensaje(data.error || 'Error desconocido');
        setUserData(null);
      }
    } catch (error) {
      console.error('Error al conectar con el backend:', error);
      setMensaje('No se pudo conectar con el servidor.');
      setUserData(null);
    }
  };

  return (
  <div id="login-container">
    <h2 className="login-title">Login Votante</h2>
    <form onSubmit={handleLogin} className="login-form">
      <div className="form-group">
        <label htmlFor="cc">Credencial Cívica:</label>
        <input
          id="cc"
          type="text"
          value={cc}
          onChange={(e) => setCc(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="circuito">ID del Circuito:</label>
        <input
          id="circuito"
          type="text"
          value={circuito}
          onChange={(e) => setCircuito(e.target.value)}
          required
        />
      </div>
      <button type="submit" className="login-button">Iniciar sesión</button>
    </form>

    <div className="extra-login-buttons">
        <button className="alt-login-button" onClick={() => navigate('/login/admin')}>
          Iniciar sesión como admin
        </button>
        <button className="alt-login-button" onClick={() => navigate('/login/presidente')}>
          Iniciar sesión como presidente de mesa
        </button>
      </div>

    {mensaje && <p className="login-message">{mensaje}</p>}

  </div>
  );
}


export default LoginVotante;

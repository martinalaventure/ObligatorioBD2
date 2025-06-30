import React, { useState } from 'react';

const LoginVotante = () => {
  const [serie, setSerie] = useState('');
  const [cc, setCc] = useState('');
  const [circuito, setCircuito] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [userData, setUserData] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:5000/login/votante', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          serie,
          cc,
          circuito_id: circuito
        })
      });

      const data = await response.json();

      if (response.ok) {
        setMensaje(data.message);
        setUserData(data.user_data);
        localStorage.setItem('token', data.token);
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
    <div style={{ padding: '2rem', maxWidth: '400px', margin: 'auto' }}>
      <h2>Login Votante</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Serie:</label>
          <input
            type="text"
            value={serie}
            onChange={(e) => setSerie(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Credencial Cívica:</label>
          <input
            type="text"
            value={cc}
            onChange={(e) => setCc(e.target.value)}
            required
          />
        </div>
        <div>
          <label>ID del Circuito:</label>
          <input
            type="text"
            value={circuito}
            onChange={(e) => setCircuito(e.target.value)}
            required
          />
        </div>
        <button type="submit">Iniciar sesión</button>
      </form>

      {mensaje && <p>{mensaje}</p>}

      {userData && (
        <div>
          <h4>Datos del votante:</h4>
          <p>CI: {userData.ci}</p>
          <p>Nombre: {userData.nombre}</p>
        </div>
      )}
    </div>
  );
};

export default LoginVotante;

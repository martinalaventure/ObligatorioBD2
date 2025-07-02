import React, { useEffect, useState } from 'react';
import '../Styles/Presidente.css'; 

const HomePresidente = () => {
  const [votos, setVotos] = useState([]);

  useEffect(() => {
    const ci = localStorage.getItem('presidente_ci');
    if (!ci) return;

    fetch('http://localhost:5000/presidente', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ci })
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.votos) {
          setVotos(data.votos);
        } else {
          alert(data.error);
        }
      })
      .catch((err) => {
        console.error(err);
        alert('Error al cargar los datos');
      });
  }, []);

  return (
    <div>
      <h2>Resumen de votos del circuito</h2>
      <table>
        <thead>
          <tr>
            <th>Lista</th>
            <th>Partido</th>
            <th>Cantidad</th>
            <th>Porcentaje</th>
          </tr>
        </thead>
        <tbody>
          {votos.map((v, i) => (
            <tr key={i}>
              <td>{v.numero_lista || '-'}</td>
              <td>{v.partido || '-'}</td>
              <td>{v.cantidad}</td>
              <td>{v.porcentaje_validos !== undefined
              ? `${v.porcentaje_validos}%`
              : '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default HomePresidente;

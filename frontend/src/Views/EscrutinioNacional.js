import React, { useEffect, useState } from 'react';

const EscrutinioNacional = () => {
  const [resultados, setResultados] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('http://localhost:5000/escrutinio/nacional')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setResultados(data);
        } else {
          setError(data.error || 'Error al obtener los resultados');
        }
      })
      .catch(() => setError('No se pudo conectar con el servidor.'));
  }, []);

  // Agrupar por evento electoral
  const resultadosPorEvento = resultados.reduce((acc, r) => {
    const key = `${r.Evento_ID} - ${r.Evento_Tipo}`;
    if (!acc[key]) acc[key] = [];
    acc[key].push(r);
    return acc;
  }, {});

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Escrutinio Nacional</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {Object.entries(resultadosPorEvento).map(([evento, listas]) => (
        <div key={evento} style={{ marginBottom: '2rem' }}>
          <h3>{evento}</h3>
          <table border="1" cellPadding="5" style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th>Número de Lista</th>
                <th>Partido</th>
                <th>Total de Votos</th>
              </tr>
            </thead>
            <tbody>
              {listas.map((r, i) => (
                <tr key={i}>
                  <td>{r.Numero_Lista}</td>
                  <td>{r.Partido}</td>
                  <td>{r.Total_Votos}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
};

export default EscrutinioNacional;

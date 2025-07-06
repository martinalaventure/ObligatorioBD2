import React, { useEffect, useState } from 'react';

const ResultadosOficiales = () => {
  const [resultados, setResultados] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchResultados = async () => {
      try {
        const res = await fetch('http://localhost:5000/resultados/oficiales');
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.error || 'Error desconocido');
        }

        setResultados(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchResultados();
  }, []);

  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!resultados) return <p>Cargando resultados...</p>;

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Resultados Oficiales</h2>

      <h3>Ganador Nacional</h3>
      <p>
        Partido: <strong>{resultados.ganador_nacional.Partido}</strong> <br />
        Total de Votos: <strong>{resultados.ganador_nacional.Total_Votos}</strong>
      </p>

      <h3>Resultados por Departamento</h3>
      {Object.entries(resultados.por_departamento).map(([depto, votos]) => (
        <div key={depto} style={{ marginBottom: '1rem' }}>
          <h4>{depto}</h4>
          <ul>
            {votos.map((v, idx) => (
            <li key={idx}>
                Partido: {v.Partido} - Votos: {v.Total_Votos}
            </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default ResultadosOficiales;

import React from 'react';
import { Link } from 'react-router-dom';

const HomeAdmin = () => {
  return (
    <div style={{ padding: '2rem' }}>
      <h2>Home Administrador</h2>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '2rem' }}>

        <Link to="/resultados/oficiales">
          <button>Ver Resultados Oficiales</button>
        </Link>
        
        <Link to="/escrutinio/nacional">
          <button>Ver Escrutinio Nacional</button>
        </Link>

        <a
            href="http://localhost:5000/auditoria/reporte"
            className="audit-btn"
            download
            >
            Descargar Auditoría
        </a>
      </div>
    </div>
  );
};

export default HomeAdmin;

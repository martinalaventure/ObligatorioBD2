import React, { useEffect, useState } from 'react';
import LogoutButton from '../Components/LogoutButton';
import '../Styles/Presidente.css';

const HomePresidente = () => {
    const [votos, setVotos] = useState([]);
    const [circuitoId, setCircuitoId] = useState(null);
    const [mensaje, setMensaje] = useState('');

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
                    setCircuitoId(data.votos[0].circuito_id); //se supone que son todos del mismo circuito, da lo mismo cual voto tomemos para saber el id del circuito
                } else {
                    alert(data.error);
                }
            })
            .catch((err) => {
                console.error(err);
                alert('Error al cargar los datos');
            });
    }, []);

    const handleIniciar = () => {
        if (!circuitoId) {
            console.warn("No hay circuitoId, no se puede iniciar");
            return;
        }


        fetch('http://localhost:5000/presidente/iniciar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ circuito_id: circuitoId })
        })
            .then(res => res.json())
            .then(data => {
                setMensaje(data.message || data.error || "Sin mensaje del servidor");
            })
            .catch(err => {
                console.error("Error en fetch iniciar:", err);
                alert('Error al iniciar votación');
            });
    };


    const handleFinalizar = () => {
        if (!circuitoId) return;

        fetch('http://localhost:5000/presidente/finalizar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ circuito_id: circuitoId })
        })
            .then(res => res.json())
            .then(data => {
                if (data.votos) {
                    setMensaje(data.message);
                    setVotos(data.votos);
                } else {
                    alert(data.error);
                }
            })
            .catch(err => {
                console.error(err);
                alert('Error al finalizar votación');
            });
    };

    return (
        <div className="presidente-container">
            <LogoutButton />
            <h2>Panel del Presidente de Mesa</h2>
            <div className="button-group">
                <button onClick={handleIniciar}>Iniciar Votación</button>
                <button onClick={handleFinalizar}>Finalizar Votación</button>
            </div>

            {mensaje && <p className="mensaje">{mensaje}</p>}

            {votos.length > 0 && (
                <div className="votos-section">
                    <h3>Resumen de votos del circuito</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Lista</th>
                                <th>Partido</th>
                                <th>Cantidad</th>
                                <th>% Válidos</th>
                            </tr>
                        </thead>
                        <tbody>
                            {votos.map((v, i) => (
                                <tr key={i}>
                                    <td>{v.numero_lista || '-'}</td>
                                    <td>{v.partido || '-'}</td>
                                    <td>{v.cantidad}</td>
                                    <td>
                                        {v.porcentaje_validos !== undefined
                                            ? `${v.porcentaje_validos}%`
                                            : '-'}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default HomePresidente;

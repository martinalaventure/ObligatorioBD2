import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Card from "../Components/Card";
import "../Styles/ListasView.css";

const ListasView = () => {
  const [listas, setListas] = useState([]);
  const [numeroFiltro, setNumeroFiltro] = useState("");
  const [partidoFiltro, setPartidoFiltro] = useState("");
  const navigate = useNavigate();

  const handleListasView = async () => {
    try {
      const response = await fetch("http://localhost:5000/listas", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      const data = await response.json();

      if (response.ok) {
        setListas(data.listas);
      } else {
        if (response.status === 401) {
          localStorage.removeItem("token");
          navigate("/login/votante");
        }
      }
    } catch (error) {
      console.error("Error al cargar las listas: ", error);
    }
  };

  const listasFiltradas = listas.filter((lista) => {
    const coincideNumero =
      numeroFiltro === "" || lista.Numero.toString().includes(numeroFiltro);
    const coincidePartido =
      partidoFiltro === "" || lista.Nombre_Partido === partidoFiltro;
    return coincideNumero && coincidePartido;
  });

  const handleAnuladoClick = () => {
    navigate(`/listas/2`);
  };

  const handleEnBlancoClick = () => {
    navigate(`/listas/1`);
  };

  useEffect(() => {
    handleListasView();
  }, []);


  return (
    <div className="listasView">
      <div className="action-bar">
        <div className="search" style={{ justifyContent: "space-around" }}>
          <label>Buscar Por Lista:</label>
          <input
            type="number"
            placeholder="Ingrese el numero de lista"
            value={numeroFiltro}
            onChange={(e) => setNumeroFiltro(e.target.value)}
          />
        </div>
        <div className="filter">
          <label>Filtrar Por Partido</label>
          <select
            value={partidoFiltro}
            onChange={(e) => setPartidoFiltro(e.target.value)}
          >
            <option value="">Todos</option>
            {[...new Set(listas.map((l) => l.Nombre_Partido))].map(
              (partido) => (
                <option key={partido} value={partido}>
                  {partido}
                </option>
              )
            )}
          </select>
        </div>
        <div className="buttons">
          <button className="anulado" onClick={handleAnuladoClick}>Votar Anulado</button>
          <button className="en_blanco" onClick={handleEnBlancoClick}>Votar En Blanco</button>
        </div>
      </div>
      <div className="cards-container">
        {listasFiltradas && listasFiltradas.length > 0 ? (
          listasFiltradas.map((lista) => (
            <Card
              key={lista.Numero}
              id={lista.Numero}
              title={"Lista: " + lista.Numero}
            >
              <p>{lista.Nombre_Partido}</p>
            </Card>
          ))
        ) : (
          <p>No hay listas disponibles.</p>
        )}
      </div>
    </div>
  );
};

export default ListasView;

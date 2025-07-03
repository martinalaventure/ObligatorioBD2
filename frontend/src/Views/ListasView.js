import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Card from "../Components/Card";
import "../Styles/ListasView.css";

const ListasView = () => {
  const [listas, setListas] = useState([]);
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

  useEffect(() => {
    handleListasView();
  }, []);

  return (
    <div className="listasView">
      <div className="cards-container">
        {listas && listas.length > 0 ? (
          listas.map((lista) => (
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

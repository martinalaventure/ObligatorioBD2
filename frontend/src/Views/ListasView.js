import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Card from "../Components/Card";

const ListasView = () => {
  const [listas, setListas] = useState([]);
  const navigate = useNavigate();

  const handleListasView = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/votante/listas", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      const data = await response.json();

      if (response.ok) {
        setListas(data || []);
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
      {listas && listas.length > 0 ? (
        listas.map((lista) => <Card key={lista.numero} />)
      ) : (
        <p>No hay listas disponibles.</p>
      )}
    </div>
  );
};

export default ListasView;

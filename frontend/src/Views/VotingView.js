import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "../Styles/VotingView.css";
import Modal from "../Components/Modal";

const VotingView = () => {
  const { id } = useParams();
  const [lista, setLista] = useState({});
  const navigate = useNavigate();
  const [mensaje, setMensaje] = useState("");
  const [votoEnBlanco, setVotoEnBlanco] = useState(false);
  const [votoAnulado, setVotoAnulado] = useState(false);
  const [mostrarModal, setMostrarModal] = useState(false);


  useEffect(() => {
    if (id === "1") {
      setVotoEnBlanco(true);
      setVotoAnulado(false);
    } else if (id === "2") {
      setVotoEnBlanco(false);
      setVotoAnulado(true);
    } else {
      setVotoEnBlanco(false);
      setVotoAnulado(false);
    }
  }, [id]);

  const handleVotacionSpace = async () => {
    try {
      const response = await fetch(`http://localhost:5000/listas/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      const data = await response.json();

      if (response.ok) {
        setLista(data.lista);
      } else {
        if (response.status === 401) {
          localStorage.removeItem("token");
          navigate("/login/votante");
        }
      }
    } catch (error) {
      console.error("Error al cargar la lista: ", error);
    }
  };

  useEffect(() => {
    handleVotacionSpace();
  }, []);

  const handleVoting = async () => {
    try {
      const response = await fetch(`http://localhost:5000/votar`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          numero_Lista: lista.Numero,
          en_blanco: votoEnBlanco,
          anulado: votoAnulado,
          id_circuito: parseInt(localStorage.getItem("circuito")),
          serie: localStorage.getItem("serie"),
        }),
      });
      if (response.ok) {
        const data = await response.json();
        setMensaje(
          `Voto registrado correctamente${
            data.observado ? " (observado)" : ""
          }.`
        );
        localStorage.removeItem("token");
        localStorage.removeItem("serie");
        localStorage.removeItem("circuito");
        navigate("/final");
      } else {
        const errorData = await response.json();
        setMensaje(errorData.error || "Error al votar.");
      }
    } catch (error) {
      console.error("Error al conectar con el backend:", error);
      setMensaje("No se pudo conectar con el servidor.");
    }
  };

  useEffect(() => {
    handleVotacionSpace();
  }, []);

  const handleCancelar = () => {
    navigate(-1);
  };

  return (
    <div className="votingView">
      <button className="cancelarBtn" onClick={handleCancelar}>
        Cancelar
      </button>

      {id === "1" ? (
        <div className="votingInfo">
          <h2>Voto en Blanco</h2>
          <p>Usted ha decidido emitir su voto en blanco.</p>
        </div>
      ) : id === "2" ? (
        <div className="votingInfo">
          <h2>Voto Anulado</h2>
          <p>Usted ha decidido anular su voto.</p>
        </div>
      ) : (
        <div className="votingInfo">
          <div className="listaNumber">
            Usted seleccionó la lista: {lista.Numero}
          </div>
          <div className="listaInfo">
            <p>
              <strong>Partido:</strong> {lista.Nombre_Partido}
            </p>
            <p>
              <strong>Dirección de la sede:</strong> {lista.Dir_Sede}
            </p>
            <p>
              <strong>Departamento:</strong> {lista.Nombre_Departamento}
            </p>
          </div>
        </div>
      )}

      <button className="votarBtn" onClick={() => setMostrarModal(true)}>
        Confirmar Voto
      </button>
      {mostrarModal && (
        <Modal onClose={() => setMostrarModal(false)}>
          <h2>¿Estás seguro que deseas confirmar tu voto?</h2>
          <div className="modal-buttons">
            <button className="confirm" onClick={handleVoting}>
              Sí, confirmar
            </button>
            <button className="cancel" onClick={() => setMostrarModal(false)}>
              Cancelar
            </button>
          </div>
        </Modal>
      )}

      {mensaje && <div className="mensaje">{mensaje}</div>}
    </div>
  );
};

export default VotingView;

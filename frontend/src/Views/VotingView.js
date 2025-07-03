import React from "react";
import { useParams } from "react-router-dom";

const VotingView = () => {
  const { id } = useParams();

  return (
    <div>
      <h1>Hola</h1>
      <p>Estás en la lista {id}</p>
    </div>
  );
};

export default VotingView;

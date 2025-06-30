import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginVotante from './Views/LoginVotante';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login/votante" element={<LoginVotante />} />
        <Route path="/" element={<h2>Bienvenido a la app electoral</h2>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

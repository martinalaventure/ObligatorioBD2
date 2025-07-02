import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginVotante from './Views/LoginVotante';
import LoginAdmin from './Views/LoginAdmin';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login/votante" element={<LoginVotante />} />
        <Route path="/login/admin" element={<LoginAdmin />} />
        <Route path="/" element={<h2>Bienvenido a la app electoral</h2>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

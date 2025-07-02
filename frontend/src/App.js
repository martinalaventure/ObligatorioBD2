import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginVotante from './Views/LoginVotante';
import LoginAdmin from './Views/LoginAdmin';
import LoginPresidente from './Views/LoginPresidente';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login/votante" element={<LoginVotante />} />
        <Route path="/login/admin" element={<LoginAdmin />} />
        <Route path="/login/presidente" element={<LoginPresidente />} />
        <Route path="/" element={<h2>Bienvenido a la app electoral</h2>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

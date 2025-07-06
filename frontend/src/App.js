import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import LoginVotante from './Views/LoginVotante';
import EscrutinioNacional from './Views/EscrutinioNacional';
import HomeAdmin from './Views/HomeAdmin';
import ResultadosOficiales from './Views/ResultadosOficiales';



function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login/votante" element={<LoginVotante />} />
        <Route path="/escrutinio/nacional" element={<EscrutinioNacional />} />
        <Route path="/home/admin" element={<HomeAdmin />} />
        <Route path="/resultados/oficiales" element={<ResultadosOficiales />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;


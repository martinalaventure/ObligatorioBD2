import React from 'react';
import EscrutinioNacional from './Views/EscrutinioNacional';
import HomeAdmin from './Views/HomeAdmin';
import ResultadosOficiales from './Views/ResultadosOficiales';
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import LoginVotante from './Views/LoginVotante';
import LoginAdmin from './Views/LoginAdmin';
import LoginPresidente from './Views/LoginPresidente';
import PresidenteHome from './Views/Presidente';
import Final from './Views/Final';
import RutaProtegida from './Components/RutaProtegida';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login/votante" element={<LoginVotante />} />
        <Route path="/escrutinio/nacional" element={<EscrutinioNacional />} />
        <Route path="/home/admin" element={<HomeAdmin />} />
        <Route path="/resultados/oficiales" element={<ResultadosOficiales />} />
        <Route path="/login/admin" element={<LoginAdmin />} />
        <Route path="/login/presidente" element={<LoginPresidente />} />
        <Route path="/" element={<Navigate to="/login/votante" />} />

        {/* Rutas protegidas */}
        {/* <Route
          path="/listas"
          element={
            <RutaProtegida>
              <ListasVotante />
            </RutaProtegida>
          }
        /> */}
        <Route
          path="/presidente"
          element={
            <RutaProtegida>
              <PresidenteHome />
            </RutaProtegida>
          }
        />  
        <Route
          path="/final"
          element={
            <RutaProtegida>
              <Final />
            </RutaProtegida>
          }
        />    
      </Routes>
    </BrowserRouter>
  );
}

export default App;


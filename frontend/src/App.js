import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
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

import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginVotante from './Views/LoginVotante';
import LoginAdmin from './Views/LoginAdmin';
import LoginPresidente from './Views/LoginPresidente';
import PresidenteHome from './Views/Presidente';
import ListasView from './Views/ListasView';
import VotingView from './Views/VotingView';
import Header from './Components/Header';

function App() {
  return (
    <BrowserRouter>
      <Header/>
      <Routes>
        <Route path="/login/votante" element={<LoginVotante />} />
        <Route path="/login/admin" element={<LoginAdmin />} />
        <Route path="/login/presidente" element={<LoginPresidente />} />
        <Route path="/presidente" element={<PresidenteHome />} />
        <Route path="/listas" element={<ListasView />} />
        <Route path="/listas/:id" element={<VotingView />} />
        <Route path="/" element={<Navigate to="/login/votante" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

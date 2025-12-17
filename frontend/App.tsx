import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { Navigation } from './components/Navigation';
import { Dashboard } from './pages/Dashboard';
import { DataPreparer } from './pages/DataPreparer';
import { ModelSelector } from './pages/ModelSelector';
import { Trainer } from './pages/Trainer';
import { Evaluator } from './pages/Evaluator';
import { Deployer } from './pages/Deployer';
import { Microservices } from './pages/Microservices';
import { Datasets } from './pages/Datasets';
import { Models } from './pages/Models';
import { Settings } from './pages/Settings';
import { Login } from './pages/Login';
import { Signup } from './pages/Signup';
import { Profile } from './pages/Profile';

function AppContent() {
  const location = useLocation();
  const isAuthPage = ['/login', '/signup'].includes(location.pathname);

  return (
    <div className="min-h-screen bg-[#F5F6FA]">
      {!isAuthPage && <Navigation />}
      <main className={isAuthPage ? '' : 'pt-16'}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/" element={<Dashboard />} />
          <Route path="/data-preparer" element={<DataPreparer />} />
          <Route path="/model-selector" element={<ModelSelector />} />
          <Route path="/trainer" element={<Trainer />} />
          <Route path="/evaluator" element={<Evaluator />} />
          <Route path="/deployer" element={<Deployer />} />
          <Route path="/microservices" element={<Microservices />} />
          <Route path="/datasets" element={<Datasets />} />
          <Route path="/models" element={<Models />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}
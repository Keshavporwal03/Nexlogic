import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AppLayout } from './components/layout/AppLayout';
import CandidateSearch from './pages/CandidateSearch';
import BannerGenerator from './pages/BannerGenerator';
import PostGenerator from './pages/PostGenerator';
import CompanyProfile from './pages/CompanyProfile';
import JobManagement from './pages/JobManagement';
import { JobProvider } from './context/JobContext';

function App() {
  return (
    <JobProvider>
      <BrowserRouter>
        <AppLayout>
          <Routes>
            <Route path="/jobs" element={<JobManagement />} />
            <Route path="/" element={<CandidateSearch />} />
            <Route path="/banner" element={<BannerGenerator />} />
            <Route path="/post" element={<PostGenerator />} />
            <Route path="/profile" element={<CompanyProfile />} />
          </Routes>
        </AppLayout>
      </BrowserRouter>
    </JobProvider>
  );
}

export default App;

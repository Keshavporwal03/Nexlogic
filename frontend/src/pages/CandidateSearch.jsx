import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import api from '../api/client';
import { useJobContext } from '../context/JobContext';
import { Link } from 'react-router-dom';

export default function CandidateSearch() {
  const { selectedJobId } = useJobContext();
  const [title, setTitle] = useState('');
  const [skills, setSkills] = useState('');
  const [location, setLocation] = useState('');
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [quotaWarning, setQuotaWarning] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);
  const [searchMessage, setSearchMessage] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!selectedJobId) {
      alert('Please select or create a job first in Job Management.');
      return;
    }
    setLoading(true);
    setQuotaWarning(null);
    setSearchMessage('');
    try {
      const res = await api.post(`/candidates/search/${selectedJobId}`);
      setCandidates(res.data.candidates || []);
      setSearchMessage(res.data.message || '');
      if (res.data.quota_warning) {
        setQuotaWarning(res.data.quota_warning);
      }
    } catch (error) {
      console.error('Error fetching candidates:', error);
      alert('Failed to search candidates.');
    } finally {
      setHasSearched(true);
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    if (!selectedJobId) {
      alert('Please select or create a job first in Job Management.');
      return;
    }
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploadLoading(true);
    try {
      const res = await api.post(`/candidates/upload/${selectedJobId}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      alert(res.data.message || 'File uploaded successfully');
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Failed to upload candidates.');
    } finally {
      setUploadLoading(false);
      e.target.value = null; // Reset input
    }
  };

  return (
    <div className="space-y-6">
      <div className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold font-sans text-charcoal mb-2">Find Candidates</h1>
          <p className="text-brown-grey">Search for the best talent matching your job requirements.</p>
        </div>
        <div>
           <label className="bg-sage text-charcoal px-4 py-2 rounded-md font-medium cursor-pointer hover:bg-sage/80 transition-all inline-flex items-center shadow-sm">
             {uploadLoading ? 'Uploading...' : 'Upload CSV'}
             <input type="file" accept=".csv" className="hidden" onChange={handleFileUpload} disabled={uploadLoading} />
           </label>
        </div>
      </div>

      {quotaWarning && (
        <div className="bg-amber-50 border-l-4 border-amber-500 p-4 rounded text-amber-900 text-sm font-medium shadow-sm">
          <p className="font-semibold text-amber-950 mb-1">⚠️ Search Quota Notice</p>
          <p>{quotaWarning}</p>
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Search Criteria</CardTitle>
        </CardHeader>
        <CardContent>
          {!selectedJobId ? (
            <div className="text-center py-4">
              <p className="text-brown-grey mb-4">No active job selected.</p>
              <Link to="/jobs" className="bg-dark-olive text-cream px-4 py-2 rounded-md hover:bg-dark-olive/90">
                Go to Job Management
              </Link>
            </div>
          ) : (
            <form className="space-y-4" onSubmit={handleSearch}>
              <div className="bg-sandstone-light p-4 rounded-md mb-4">
                <p className="text-sm font-medium">Currently searching for Job ID: {selectedJobId}</p>
                <p className="text-xs text-brown-grey mt-1">Note: Search criteria is pulled directly from the job details.</p>
              </div>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <label className="block text-sm font-medium text-charcoal mb-1">Job Title</label>
                <Input type="text" placeholder="e.g. Software Engineer" value={title} onChange={e => setTitle(e.target.value)} />
              </div>
              <div>
                <label className="block text-sm font-medium text-charcoal mb-1">Skills (comma separated)</label>
                <Input type="text" placeholder="e.g. React, Python, SQL" value={skills} onChange={e => setSkills(e.target.value)} />
              </div>
              <div>
                <label className="block text-sm font-medium text-charcoal mb-1">Location</label>
                <Input type="text" placeholder="e.g. Remote, New York" value={location} onChange={e => setLocation(e.target.value)} />
              </div>
            </div>
            <div className="pt-4 flex justify-end">
              <Button type="submit" disabled={loading}>
                {loading ? 'Searching...' : 'Search Candidates'}
              </Button>
            </div>
          </form>
          )}
        </CardContent>
      </Card>

      <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {candidates.length > 0 ? (
          candidates.map((cand, idx) => {
            const isUnverified = cand.unverified || (cand.source && cand.source.includes('Google Search')) || (cand.source && cand.source.includes('Serper'));
            return (
              <Card key={idx} className={isUnverified ? "border-amber-200 bg-amber-50/20" : ""}>
                <CardContent className="pt-6">
                  <div className="flex justify-between items-start mb-1">
                    <h3 className="font-bold text-lg text-charcoal">{cand.name || 'Unknown'}</h3>
                    {cand.match_score !== undefined && (
                      <span className="text-xs font-bold px-2 py-0.5 rounded bg-sage/20 text-dark-olive">
                        Match: {Math.round(cand.match_score)}%
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-brown-grey mb-2">{cand.location || 'No location specified'}</p>
                  
                  <div className="flex flex-wrap gap-2 mb-3">
                    {(cand.skills || []).map(skill => (
                      <span key={skill} className="bg-sandstone-light text-charcoal text-xs px-2 py-1 rounded">
                        {skill}
                      </span>
                    ))}
                  </div>

                  <p className="text-xs text-dark-olive font-semibold mb-2">Source: {cand.source}</p>

                  {isUnverified && (
                    <div className="mt-2 mb-3 p-2 bg-amber-100/60 border border-amber-300 rounded text-xs text-amber-900 font-medium">
                      ⚠️ Unverified — based on public search snippet only
                      {cand.unverified_snippet && (
                        <p className="mt-1 text-[11px] text-amber-800 italic line-clamp-2">
                          "{cand.unverified_snippet}"
                        </p>
                      )}
                    </div>
                  )}

                  {cand.profile_url && (
                    <a href={cand.profile_url} target="_blank" rel="noopener noreferrer" className="text-sm text-dark-olive underline inline-block mt-1">
                      View Profile →
                    </a>
                  )}
                </CardContent>
              </Card>
            );
          })
        ) : hasSearched ? (
          <Card className="bg-sandstone-light/40 border border-charcoal/10 lg:col-span-3">
            <CardContent className="py-12 text-center">
              <div className="text-3xl mb-2">🔍</div>
              <h3 className="text-lg font-bold text-charcoal mb-1">No Candidates Found</h3>
              <p className="text-sm text-brown-grey max-w-md mx-auto mb-2">
                {searchMessage || 'No candidates matched the job requirements from available sources.'}
              </p>
              <p className="text-xs text-brown-grey italic">
                Tip: Try broadening job skills or location criteria in Job Management.
              </p>
            </CardContent>
          </Card>
        ) : (
          <Card className="opacity-50 lg:col-span-3">
            <CardContent className="py-8 text-center">
              <p className="text-sm text-brown-grey">No candidates searched yet. Click "Search Candidates" to run an automated search.</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}



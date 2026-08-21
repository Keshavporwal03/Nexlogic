import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import api from '../api/client';
import { useJobContext } from '../context/JobContext';
import { Link } from 'react-router-dom';

export default function BannerGenerator() {
  const { selectedJobIds } = useJobContext();
  const [selectedJobs, setSelectedJobs] = useState([]);
  const [loadingJobs, setLoadingJobs] = useState(false);
  const [applyLink, setApplyLink] = useState('');

  useEffect(() => {
    if (selectedJobIds && selectedJobIds.length > 0) {
      setLoadingJobs(true);
      // Fetch all jobs and filter
      api.get(`/jobs`)
        .then(res => {
          const matched = res.data.filter(j => selectedJobIds.includes(j.id));
          setSelectedJobs(matched);
          if (matched.length > 0 && matched[0].apply_link) {
            setApplyLink(matched[0].apply_link);
          }
        })
        .catch(err => console.error(err))
        .finally(() => setLoadingJobs(false));
    } else {
      setSelectedJobs([]);
    }
  }, [selectedJobIds]);
  
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!selectedJobs || selectedJobs.length === 0) {
      alert('Please select or create at least one job first in Job Management.');
      return;
    }
    setLoading(true);
    
    try {
      const activeApplyLink = applyLink || (selectedJobs[0] && selectedJobs[0].apply_link) || '';
      const payload = {
        jobs: selectedJobs.map(job => ({
            ...job,
            apply_link: activeApplyLink || job.apply_link
        })),
        company_colors: { background_color: '#F9F7F1', text_color: '#1F1F1F', secondary_color: '#A8B5A2', apply_link: activeApplyLink }
      };

      const res = await api.post('/ai/banner', payload, {
        responseType: 'blob'
      });
      
      const url = URL.createObjectURL(res.data);
      setImageUrl(url);
    } catch (error) {
      console.error('Error generating banner:', error);
      alert('Failed to generate banner.');
    } finally {
      setLoading(false);
    }
  };


  const isMultiJob = selectedJobs.length > 1;

  return (
    <div className="space-y-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold font-heading text-charcoal mb-2">Banner Generator</h1>
        <p className="text-brown-grey">Create stunning AI-generated hiring banners with your brand colors.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Job Details</CardTitle>
            </CardHeader>
            <CardContent>
              {selectedJobs.length === 0 ? (
                <div className="text-center py-4">
                  <p className="text-brown-grey mb-4">No active job selected.</p>
                  <Link to="/jobs" className="bg-dark-olive text-cream px-4 py-2 rounded-md hover:bg-dark-olive/90">
                    Go to Job Management
                  </Link>
                </div>
              ) : (
                <form className="space-y-4" onSubmit={handleGenerate}>
                  <div className="bg-sandstone-light p-4 rounded-md mb-4 flex justify-between items-center">
                    <div>
                      <p className="text-sm font-medium">Currently using {selectedJobs.length} Job(s)</p>
                      <p className="text-xs text-brown-grey mt-1">Colors will be pulled automatically from your Company Profile.</p>
                    </div>
                    <Link to="/jobs" className="text-sm text-dark-olive underline whitespace-nowrap ml-4">Edit Jobs</Link>
                  </div>
                  {loadingJobs ? <p className="text-sm text-brown-grey">Loading job details...</p> : (
                    <>
                      {isMultiJob ? (
                          <div className="bg-gray-50 border border-gray-200 rounded-md p-3 text-sm text-gray-700">
                              <p className="font-bold mb-2">Multiple Jobs Selected:</p>
                              <ul className="list-disc pl-4 space-y-1">
                                  {selectedJobs.map(job => (
                                      <li key={job.id}>{job.title} - {job.location}</li>
                                  ))}
                              </ul>
                          </div>
                      ) : (
                          <>
                            <div>
                                <label className="block text-sm font-medium text-charcoal mb-1">Job Title</label>
                                <p className="text-sm p-2 bg-gray-50 rounded-md border border-gray-200 text-gray-700">{selectedJobs[0].title}</p>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-charcoal mb-1">Experience Level</label>
                                <p className="text-sm p-2 bg-gray-50 rounded-md border border-gray-200 text-gray-700">{selectedJobs[0].experience || 'N/A'}</p>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-charcoal mb-1">Location</label>
                                <p className="text-sm p-2 bg-gray-50 rounded-md border border-gray-200 text-gray-700">{selectedJobs[0].location}</p>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-charcoal mb-1">Job Profile Summary</label>
                                <p className="text-sm p-2 bg-gray-50 rounded-md border border-gray-200 text-gray-700 min-h-[60px] whitespace-pre-wrap">{selectedJobs[0].description || 'N/A'}</p>
                            </div>
                          </>
                      )}
                      
                      <div>
                        <label className="block text-sm font-medium text-charcoal mb-1">Apply Link (Override)</label>
                        <Input type="text" placeholder={selectedJobs[0].apply_link || "https://..."} value={applyLink} onChange={e => setApplyLink(e.target.value)} />
                      </div>
                      <div className="pt-4">
                        <Button type="submit" className="w-full" disabled={loading}>
                          {loading ? 'Generating...' : 'Generate Banner'}
                        </Button>
                      </div>
                    </>
                  )}
              </form>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-2">
          <Card className="h-full min-h-[400px] flex items-center justify-center bg-sandstone-light/30 overflow-hidden">
            {loading ? (
              <CardContent className="text-center space-y-4">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-sage/20 text-dark-olive mb-4 animate-pulse">
                  <svg className="w-8 h-8 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                  </svg>
                </div>
                <p className="text-charcoal font-medium">Generating your banner...</p>
                <p className="text-brown-grey text-sm max-w-xs mx-auto">This may take up to 60-90 seconds if the AI model is warming up on the server.</p>
              </CardContent>
            ) : imageUrl ? (
              <div className="flex flex-col items-center justify-center p-6 gap-6 w-full h-full">
                <img src={imageUrl} alt="Generated Banner" className="w-full h-auto object-cover rounded shadow-sm border border-gray-200" />
                <a 
                  href={imageUrl} 
                  download={`banner-jobs.png`} 
                  className="inline-flex items-center justify-center bg-dark-olive text-cream px-6 py-2 rounded-md hover:bg-dark-olive/90 transition-colors font-medium shadow-sm"
                >
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                  </svg>
                  Download Banner
                </a>
              </div>
            ) : (
              <CardContent className="text-center space-y-4">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-sage/20 text-dark-olive mb-4">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <p className="text-brown-grey">Your generated banner will appear here.</p>
              </CardContent>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}

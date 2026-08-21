import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import api from '../api/client';
import { useJobContext } from '../context/JobContext';
import { Link } from 'react-router-dom';

export default function PostGenerator() {
  const { selectedJobIds } = useJobContext();
  const [applyLink, setApplyLink] = useState('');
  const [selectedJobs, setSelectedJobs] = useState([]);
  const [loadingJobs, setLoadingJobs] = useState(false);
  const [companyData, setCompanyData] = useState(null);

  useEffect(() => {
    // Fetch company profile for company name
    api.get('/company/profile')
      .then(res => setCompanyData(res.data))
      .catch(err => console.error('Failed to fetch company:', err));

    if (selectedJobIds && selectedJobIds.length > 0) {
      setLoadingJobs(true);
      api.get(`/jobs`)
        .then(res => {
          const matched = res.data.filter(j => selectedJobIds.includes(j.id));
          setSelectedJobs(matched);
        })
        .catch(err => console.error(err))
        .finally(() => setLoadingJobs(false));
    } else {
      setSelectedJobs([]);
    }
  }, [selectedJobIds]);
  
  const [postDraft, setPostDraft] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!selectedJobs || selectedJobs.length === 0) {
      alert('Please select or create at least one job first in Job Management.');
      return;
    }
    setLoading(true);
    try {
      const payload = {
        jobs: selectedJobs.map(job => ({
            ...job,
            company_name: companyData ? companyData.company_name : 'Your Company',
            apply_link: applyLink || job.apply_link
        }))
      };
      const res = await api.post('/ai/post', payload);
      setPostDraft(res.data.post);
    } catch (error) {
      console.error('Error generating post:', error);
      alert('Failed to generate post.');
    } finally {
      setLoading(false);
    }
  };

  const isMultiJob = selectedJobs.length > 1;

  return (
    <div className="space-y-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold font-heading text-charcoal mb-2">LinkedIn Post Generator</h1>
        <p className="text-brown-grey">Instantly draft an engaging LinkedIn post to announce your open roles.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Job Context</CardTitle>
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
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                <label className="block text-sm font-medium text-charcoal mb-1">Job Title</label>
                                <p className="text-sm p-2 bg-gray-50 rounded-md border border-gray-200 text-gray-700">{selectedJobs[0].title}</p>
                                </div>
                                <div>
                                <label className="block text-sm font-medium text-charcoal mb-1">Company Name</label>
                                <p className="text-sm p-2 bg-gray-50 rounded-md border border-gray-200 text-gray-700">
                                    {companyData ? companyData.company_name : 'Loading...'}
                                </p>
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                <label className="block text-sm font-medium text-charcoal mb-1">Location</label>
                                <p className="text-sm p-2 bg-gray-50 rounded-md border border-gray-200 text-gray-700">{selectedJobs[0].location}</p>
                                </div>
                                <div>
                                <label className="block text-sm font-medium text-charcoal mb-1">Experience</label>
                                <p className="text-sm p-2 bg-gray-50 rounded-md border border-gray-200 text-gray-700">{selectedJobs[0].experience || 'N/A'}</p>
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-charcoal mb-1">Skills</label>
                                <p className="text-sm p-2 bg-gray-50 rounded-md border border-gray-200 text-gray-700">
                                {selectedJobs[0].skills && selectedJobs[0].skills.length > 0 ? selectedJobs[0].skills.join(', ') : 'N/A'}
                                </p>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-charcoal mb-1">Job Profile / Description</label>
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
                          {loading ? 'Drafting...' : 'Draft Post'}
                        </Button>
                      </div>
                    </>
                  )}
              </form>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card className="h-full min-h-[400px] flex flex-col bg-white">
            <CardHeader>
              <CardTitle>Generated Draft</CardTitle>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col items-center justify-center text-center p-8">
              {postDraft ? (
                <div className="w-full text-left bg-sandstone-light/30 p-6 rounded-md whitespace-pre-wrap text-charcoal">
                  {postDraft}
                </div>
              ) : (
                <>
                  <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-sage/20 text-dark-olive mb-4">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                  </div>
                  <p className="text-brown-grey">Your LinkedIn post draft will appear here.</p>
                </>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

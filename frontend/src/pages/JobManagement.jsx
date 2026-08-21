import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import api from '../api/client';
import { useJobContext } from '../context/JobContext';

export default function JobManagement() {
  const { selectedJobId, setSelectedJobId, selectedJobIds, setSelectedJobIds } = useJobContext();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const [extracting, setExtracting] = useState(false);
  const [editJobId, setEditJobId] = useState(null);
  
  const [isStructured, setIsStructured] = useState(true);
  const [unstructuredText, setUnstructuredText] = useState('');

  // Form state
  const [title, setTitle] = useState('');
  const [experience, setExperience] = useState('');
  const [minExperience, setMinExperience] = useState('');
  const [maxExperience, setMaxExperience] = useState('');
  const [location, setLocation] = useState('');
  const [remoteType, setRemoteType] = useState('Remote');
  const [skills, setSkills] = useState('');
  const [salary, setSalary] = useState('');
  const [salaryMax, setSalaryMax] = useState('');
  const [salaryDisclosure, setSalaryDisclosure] = useState('Hidden');
  const [description, setDescription] = useState('');
  const [deadline, setDeadline] = useState('');
  const [applyLink, setApplyLink] = useState('');
  const [matchThreshold, setMatchThreshold] = useState('30.0');
  const [numberOfOpenings, setNumberOfOpenings] = useState('');
  const [educationRequirements, setEducationRequirements] = useState('');
  const [roleObjective, setRoleObjective] = useState('');
  const [keyResponsibilities, setKeyResponsibilities] = useState('');
  const [krmMeasurement, setKrmMeasurement] = useState('');
  const [preferredCertifications, setPreferredCertifications] = useState('');

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const res = await api.get('/jobs');
      setJobs(res.data || []);
      // If no job is selected but we have jobs, default to first one
      if (!selectedJobId && res.data && res.data.length > 0) {
        setSelectedJobId(res.data[0].id);
        setSelectedJobIds([res.data[0].id]);
      }
    } catch (err) {
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEditClick = (job) => {
    setEditJobId(job.id);
    setIsStructured(true);
    setTitle(job.title || '');
    setExperience(job.experience || '');
    setMinExperience(job.min_experience !== null ? job.min_experience : '');
    setMaxExperience(job.max_experience !== null ? job.max_experience : '');
    setLocation(job.location || '');
    setRemoteType(job.remote_type || 'Remote');
    setSkills(job.skills ? job.skills.join(', ') : '');
    setSalary(job.salary || '');
    setSalaryMax(job.salary_max || '');
    setSalaryDisclosure(job.salary_disclosure || 'Hidden');
    setDescription(job.description || '');
    setDeadline(job.deadline || '');
    setApplyLink(job.apply_link || '');
    setMatchThreshold(job.match_threshold !== null ? job.match_threshold : '30.0');
    setNumberOfOpenings(job.number_of_openings !== null ? job.number_of_openings : '');
    setEducationRequirements(job.education_requirements ? job.education_requirements.join(', ') : '');
    setRoleObjective(job.role_objective || '');
    setKeyResponsibilities(job.key_responsibilities ? job.key_responsibilities.join(', ') : '');
    setKrmMeasurement(job.krm_measurement || '');
    setPreferredCertifications(job.preferred_certifications ? job.preferred_certifications.join(', ') : '');
  };

  const handleCancelEdit = () => {
    setEditJobId(null);
    setTitle('');
    setExperience('');
    setMinExperience('');
    setMaxExperience('');
    setLocation('');
    setRemoteType('Remote');
    setSkills('');
    setSalary('');
    setSalaryMax('');
    setSalaryDisclosure('Hidden');
    setDescription('');
    setDeadline('');
    setApplyLink('');
    setMatchThreshold('30.0');
    setNumberOfOpenings('');
    setEducationRequirements('');
    setRoleObjective('');
    setKeyResponsibilities('');
    setKrmMeasurement('');
    setPreferredCertifications('');
    setUnstructuredText('');
  };

  const handleDeleteJob = async (id) => {
    if (!window.confirm("Are you sure you want to delete this job? This action cannot be undone.")) return;
    try {
      await api.delete(`/jobs/${id}`);
      setJobs(jobs.filter(j => j.id !== id));
      if (selectedJobId === id) setSelectedJobId(null);
      setSelectedJobIds(selectedJobIds.filter(jid => jid !== id));
      if (editJobId === id) handleCancelEdit();
    } catch (err) {
      console.error('Error deleting job:', err);
      alert('Failed to delete job.');
    }
  };

  const handleExtractAI = async () => {
    if (!unstructuredText) return;
    setExtracting(true);
    try {
        const res = await api.post('/ai/extract-job', { text: unstructuredText });
        const data = res.data;
        
        setTitle(data.title || '');
        setExperience(data.experience || '');
        setMinExperience(data.min_experience !== null ? data.min_experience : '');
        setMaxExperience(data.max_experience !== null ? data.max_experience : '');
        setLocation(data.location || '');
        setRemoteType(data.remote_type || 'Remote');
        setSkills(data.skills ? data.skills.join(', ') : '');
        setSalary(data.salary || '');
        setSalaryMax(data.salary_max || '');
        setSalaryDisclosure(data.salary_disclosure || 'Hidden');
        setDescription(data.description || '');
        setDeadline(data.deadline || '');
        setApplyLink(data.apply_link || '');
        if (data.match_threshold) setMatchThreshold(data.match_threshold);
        setNumberOfOpenings(data.number_of_openings !== null ? data.number_of_openings : '');
        setEducationRequirements(data.education_requirements ? data.education_requirements.join(', ') : '');
        setRoleObjective(data.role_objective || '');
        setKeyResponsibilities(data.key_responsibilities ? data.key_responsibilities.join(', ') : '');
        setKrmMeasurement(data.krm_measurement || '');
        setPreferredCertifications(data.preferred_certifications ? data.preferred_certifications.join(', ') : '');
        
        setIsStructured(true);
        alert('Extraction complete! Please review the fields before saving.');
    } catch (err) {
        console.error('Extraction error:', err);
        alert('Failed to extract data. Ensure API key is valid.');
    } finally {
        setExtracting(false);
    }
  };

  const handleSaveJob = async (e) => {
    e.preventDefault();
    setCreating(true);
    try {
      const payload = {
        title,
        experience,
        min_experience: minExperience ? parseInt(minExperience, 10) : null,
        max_experience: maxExperience ? parseInt(maxExperience, 10) : null,
        location,
        remote_type: remoteType,
        skills: skills.split(',').map(s => s.trim()).filter(Boolean),
        salary,
        salary_max: salaryMax,
        salary_disclosure: salaryDisclosure,
        description,
        deadline,
        apply_link: applyLink,
        match_threshold: matchThreshold ? parseFloat(matchThreshold) : 30.0,
        number_of_openings: numberOfOpenings ? parseInt(numberOfOpenings, 10) : null,
        education_requirements: educationRequirements.split(',').map(s => s.trim()).filter(Boolean),
        role_objective: roleObjective,
        key_responsibilities: keyResponsibilities.split(',').map(s => s.trim()).filter(Boolean),
        krm_measurement: krmMeasurement,
        preferred_certifications: preferredCertifications.split(',').map(s => s.trim()).filter(Boolean)
      };
      
      if (editJobId) {
        const res = await api.put(`/jobs/${editJobId}`, payload);
        setJobs(jobs.map(j => j.id === editJobId ? res.data : j));
        alert('Job updated successfully!');
        handleCancelEdit();
      } else {
        const res = await api.post('/jobs', payload);
        setJobs([...jobs, res.data]);
        setSelectedJobId(res.data.id);
        if (!selectedJobIds.includes(res.data.id)) {
            setSelectedJobIds([...selectedJobIds, res.data.id]);
        }
        alert('Job created successfully!');
        handleCancelEdit();
      }
    } catch (err) {
      console.error('Error saving job:', err);
      alert('Failed to save job.');
    } finally {
      setCreating(false);
    }
  };

  const toggleJobSelection = (id) => {
      if (selectedJobIds.includes(id)) {
          const newSelection = selectedJobIds.filter(jid => jid !== id);
          setSelectedJobIds(newSelection);
          if (selectedJobId === id) setSelectedJobId(newSelection.length > 0 ? newSelection[0] : null);
      } else {
          setSelectedJobIds([...selectedJobIds, id]);
          setSelectedJobId(id);
      }
  };

  return (
    <div className="space-y-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold font-heading text-charcoal mb-2">Job Management</h1>
        <p className="text-brown-grey">Create new job postings and select active jobs for AI generation tasks.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Active Job Selection */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Select Active Jobs (Multi-Select)</CardTitle>
            </CardHeader>
            <CardContent>
              {loading ? (
                <p>Loading jobs...</p>
              ) : jobs.length === 0 ? (
                <p className="text-brown-grey">No jobs found. Create one below.</p>
              ) : (
                <div className="space-y-4">
                  {jobs.map(job => (
                    <div 
                      key={job.id} 
                      className={`p-4 border rounded-md cursor-pointer transition-colors ${selectedJobIds.includes(job.id) ? 'border-primary bg-sandstone-light' : 'border-gray-200 hover:border-primary'}`}
                      onClick={() => toggleJobSelection(job.id)}
                    >
                      <div className="flex justify-between items-start">
                        <div className="flex items-center gap-3">
                            <input 
                                type="checkbox" 
                                checked={selectedJobIds.includes(job.id)} 
                                readOnly
                                className="h-4 w-4 text-primary"
                            />
                            <div>
                                <h3 className="font-bold">{job.title}</h3>
                                <p className="text-sm text-gray-500">{job.location} • {job.remote_type}</p>
                            </div>
                        </div>
                        <div className="flex gap-3">
                          <button 
                            className="text-sm font-medium text-blue-600 hover:underline"
                            onClick={(e) => { e.stopPropagation(); handleEditClick(job); }}
                          >
                            Edit
                          </button>
                          <button 
                            className="text-sm font-medium text-red-600 hover:underline"
                            onClick={(e) => { e.stopPropagation(); handleDeleteJob(job.id); }}
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Create Job Form */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle>{editJobId ? 'Edit Job' : 'Create New Job'}</CardTitle>
                <div className="flex rounded-md border border-gray-200 p-1 bg-gray-50">
                    <button
                        type="button"
                        className={`px-3 py-1 text-sm font-medium rounded-md ${!isStructured ? 'bg-white shadow border border-gray-200' : 'text-gray-500 hover:text-charcoal'}`}
                        onClick={() => setIsStructured(false)}
                    >
                        Unstructured
                    </button>
                    <button
                        type="button"
                        className={`px-3 py-1 text-sm font-medium rounded-md ${isStructured ? 'bg-white shadow border border-gray-200' : 'text-gray-500 hover:text-charcoal'}`}
                        onClick={() => setIsStructured(true)}
                    >
                        Structured
                    </button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              {!isStructured ? (
                  <div className="space-y-4">
                      <div>
                          <label className="block text-sm font-medium text-charcoal mb-1">Paste Job Description</label>
                          <textarea 
                              className="w-full rounded-md border border-sandstone-light bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-brown-grey focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
                              rows={15}
                              value={unstructuredText}
                              onChange={(e) => setUnstructuredText(e.target.value)}
                              placeholder="Paste the full job description here. Our AI will extract the structured fields automatically."
                          />
                      </div>
                      <Button onClick={handleExtractAI} disabled={extracting || !unstructuredText} className="w-full">
                          {extracting ? 'Extracting with AI...' : 'Extract with AI'}
                      </Button>
                  </div>
              ) : (
                <form className="space-y-4" onSubmit={handleSaveJob}>
                    <div>
                    <label className="block text-sm font-medium text-charcoal mb-1">Job Title *</label>
                    <Input type="text" required value={title} onChange={e => setTitle(e.target.value)} placeholder="Software Engineer" />
                    </div>
                    <div className="grid grid-cols-3 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-charcoal mb-1">Exp String *</label>
                        <Input type="text" required value={experience} onChange={e => setExperience(e.target.value)} placeholder="3+ Years" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-charcoal mb-1">Min Exp (Yrs)</label>
                        <Input type="number" value={minExperience} onChange={e => setMinExperience(e.target.value)} placeholder="3" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-charcoal mb-1">Max Exp (Yrs)</label>
                        <Input type="number" value={maxExperience} onChange={e => setMaxExperience(e.target.value)} placeholder="5" />
                    </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-charcoal mb-1">Location *</label>
                        <Input type="text" required value={location} onChange={e => setLocation(e.target.value)} placeholder="New York, NY" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-charcoal mb-1">Remote Type *</label>
                        <select 
                        className="w-full rounded-md border border-sandstone-light bg-transparent px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
                        value={remoteType}
                        onChange={e => setRemoteType(e.target.value)}
                        >
                        <option value="Remote">Remote</option>
                        <option value="Hybrid">Hybrid</option>
                        <option value="On-site">On-site</option>
                        </select>
                    </div>
                    </div>

                    <div className="grid grid-cols-3 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-charcoal mb-1">Salary Disclosure</label>
                        <select 
                            className="w-full rounded-md border border-sandstone-light bg-transparent px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
                            value={salaryDisclosure}
                            onChange={e => setSalaryDisclosure(e.target.value)}
                        >
                            <option value="Hidden">Hidden</option>
                            <option value="Show exact">Show exact</option>
                            <option value="Show range">Show range</option>
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-charcoal mb-1">Salary Min / Exact</label>
                        <Input type="text" value={salary} onChange={e => setSalary(e.target.value)} placeholder="$100k" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-charcoal mb-1">Salary Max</label>
                        <Input type="text" value={salaryMax} onChange={e => setSalaryMax(e.target.value)} placeholder="$120k" />
                    </div>
                    </div>

                    <div>
                    <label className="block text-sm font-medium text-charcoal mb-1">Skills (comma separated)</label>
                    <Input type="text" value={skills} onChange={e => setSkills(e.target.value)} placeholder="React, Node.js, Python" />
                    </div>

                    <div>
                    <label className="block text-sm font-medium text-charcoal mb-1">Education Requirements (comma separated)</label>
                    <Input type="text" value={educationRequirements} onChange={e => setEducationRequirements(e.target.value)} placeholder="B.Tech, Master's, MCA, CA" />
                    </div>

                    <div>
                    <label className="block text-sm font-medium text-charcoal mb-1">Number of Openings</label>
                    <Input type="number" value={numberOfOpenings} onChange={e => setNumberOfOpenings(e.target.value)} placeholder="1" />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-charcoal mb-1">Apply Link</label>
                        <Input type="text" value={applyLink} onChange={e => setApplyLink(e.target.value)} placeholder="https://..." />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-charcoal mb-1">Deadline</label>
                        <Input type="text" value={deadline} onChange={e => setDeadline(e.target.value)} placeholder="August 30, 2026 (Optional)" />
                    </div>
                    </div>

                    
                    <div>
                    <label className="block text-sm font-medium text-charcoal mb-1">Description *</label>
                    <textarea 
                        className="w-full flex rounded-md border border-sandstone-light bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-brown-grey focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary disabled:cursor-not-allowed disabled:opacity-50" 
                        required 
                        value={description} 
                        onChange={e => setDescription(e.target.value)} 
                        rows={4} 
                        placeholder="We are looking for..."
                    />
                    </div>
                    
                    <div>
                    <label className="block text-sm font-medium text-charcoal mb-1">Role Objective</label>
                    <textarea 
                        className="w-full flex rounded-md border border-sandstone-light bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-brown-grey focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary" 
                        value={roleObjective} 
                        onChange={e => setRoleObjective(e.target.value)} 
                        rows={3} 
                        placeholder="Primary objective of this role..."
                    />
                    </div>

                    <div>
                    <label className="block text-sm font-medium text-charcoal mb-1">Key Responsibilities (comma separated)</label>
                    <Input type="text" value={keyResponsibilities} onChange={e => setKeyResponsibilities(e.target.value)} placeholder="Manage team, Write code, Deploy infrastructure" />
                    </div>

                    <div>
                    <label className="block text-sm font-medium text-charcoal mb-1">KRM Measurement</label>
                    <textarea 
                        className="w-full flex rounded-md border border-sandstone-light bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-brown-grey focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary" 
                        value={krmMeasurement} 
                        onChange={e => setKrmMeasurement(e.target.value)} 
                        rows={3} 
                        placeholder="How will success be measured?"
                    />
                    </div>

                    <div>
                    <label className="block text-sm font-medium text-charcoal mb-1">Preferred Certifications (comma separated)</label>
                    <Input type="text" value={preferredCertifications} onChange={e => setPreferredCertifications(e.target.value)} placeholder="AWS Certified, PMP, CISSP" />
                    </div>
                    
                    <div className="pt-4 flex gap-4">
                    <Button type="submit" className="flex-1" disabled={creating}>
                        {creating ? 'Saving...' : (editJobId ? 'Update Job' : 'Save Job')}
                    </Button>
                    {editJobId && (
                        <Button type="button" variant="outline" className="flex-1 border-gray-300 text-gray-700 hover:bg-gray-50" onClick={handleCancelEdit}>
                        Cancel
                        </Button>
                    )}
                    </div>
                </form>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

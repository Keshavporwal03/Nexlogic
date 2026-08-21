import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import api from '../api/client';

export default function CompanyProfile() {
  const [applyLink, setApplyLink] = useState('');
  const [contactEmail, setContactEmail] = useState('');
  const [whyJoinUs, setWhyJoinUs] = useState('');
  const [primaryColor, setPrimaryColor] = useState('#384F3E');
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  const COLORS = [
    '#1F1F1F', // Charcoal
    '#E6DED3', // Sandstone
    '#D2C8BB', // Taupe
    '#A8B5A2', // Sage
    '#6F6A63', // Brown-Grey
    '#F5F1ED', // Sandstone Light
    '#F9F6F2', // Cream
    '#FFFFFF', // White
    '#384F3E', // Dark Olive Green
  ];

  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      try {
        const res = await api.get('/company/profile');
        if (res.data) {
          setApplyLink(res.data.apply_link || '');
          setContactEmail(res.data.contact_email || '');
          setWhyJoinUs((res.data.why_join_us || []).join('\n'));
          if (res.data.primary_color) setPrimaryColor(res.data.primary_color);
        }
      } catch (err) {
        console.error('Error fetching profile:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const payload = {
        apply_link: applyLink,
        contact_email: contactEmail,
        why_join_us: whyJoinUs.split('\n').filter(line => line.trim() !== ''),
        primary_color: primaryColor
      };
      await api.post('/company/profile', payload);
      alert('Company profile saved successfully!');
    } catch (err) {
      console.error('Error saving profile:', err);
      alert('Failed to save company profile.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold font-heading text-charcoal mb-2">Company Profile</h1>
        <p className="text-brown-grey">Manage your global company defaults for all generated banners and posts.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Company Details</CardTitle>
            </CardHeader>
            <CardContent>
              {loading ? (
                <p>Loading profile...</p>
              ) : (
                <form className="space-y-4" onSubmit={handleSave}>
                  <div>
                    <label className="block text-sm font-medium text-charcoal mb-1">Global Apply Link</label>
                    <Input type="text" placeholder="https://..." value={applyLink} onChange={e => setApplyLink(e.target.value)} />
                    <p className="text-xs text-brown-grey mt-1">This will be used as a fallback if a job-specific apply link is not provided.</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-charcoal mb-1">Contact Email</label>
                    <Input type="email" placeholder="jobs@yourcompany.com" value={contactEmail} onChange={e => setContactEmail(e.target.value)} />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-charcoal mb-1">Why Join Us (One reason per line)</label>
                    <textarea 
                      className="w-full flex rounded-md border border-sandstone-light bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-brown-grey focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary disabled:cursor-not-allowed disabled:opacity-50" 
                      placeholder="Great culture&#10;Competitive salary&#10;Remote friendly" 
                      value={whyJoinUs} 
                      onChange={e => setWhyJoinUs(e.target.value)} 
                      rows={5} 
                    />
                    <p className="text-xs text-brown-grey mt-1">These points will be automatically injected into your AI generated LinkedIn posts.</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-charcoal mb-1">Primary Brand Color</label>
                    <div className="flex gap-2 flex-wrap mt-2">
                      {COLORS.map(c => (
                        <div 
                          key={c}
                          onClick={() => setPrimaryColor(c)}
                          className={`w-8 h-8 rounded-full cursor-pointer border-2 transition-all ${primaryColor === c ? 'border-charcoal scale-110' : 'border-transparent hover:scale-105'}`}
                          style={{ backgroundColor: c }}
                        />
                      ))}
                    </div>
                  </div>
                  <div className="pt-4">
                    <Button type="submit" className="w-full" disabled={saving}>
                      {saving ? 'Saving...' : 'Save Profile'}
                    </Button>
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

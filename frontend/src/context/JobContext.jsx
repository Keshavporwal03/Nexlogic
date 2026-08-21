import React, { createContext, useContext, useState, useEffect } from 'react';

const JobContext = createContext();

export const useJobContext = () => {
    const context = useContext(JobContext);
    if (!context) {
        throw new Error('useJobContext must be used within a JobProvider');
    }
    return context;
};

export const JobProvider = ({ children }) => {
    const [selectedJobId, setSelectedJobId] = useState(() => {
        const saved = localStorage.getItem('selectedJobId');
        return saved ? parseInt(saved, 10) : null;
    });

    const [selectedJobIds, setSelectedJobIds] = useState(() => {
        const saved = localStorage.getItem('selectedJobIds');
        try {
            return saved ? JSON.parse(saved) : [];
        } catch {
            return [];
        }
    });

    useEffect(() => {
        if (selectedJobId !== null) {
            localStorage.setItem('selectedJobId', selectedJobId);
        } else {
            localStorage.removeItem('selectedJobId');
        }
    }, [selectedJobId]);

    useEffect(() => {
        localStorage.setItem('selectedJobIds', JSON.stringify(selectedJobIds));
    }, [selectedJobIds]);

    return (
        <JobContext.Provider value={{ selectedJobId, setSelectedJobId, selectedJobIds, setSelectedJobIds }}>
            {children}
        </JobContext.Provider>
    );
};

import React, { useState, useEffect } from 'react';
import './App.css';

interface PostHogStats {
  events_24h: number;
  unique_users_24h: number;
  page_views_24h: number;
  last_updated: string;
  error?: string;
}

const App: React.FC = () => {
  const [stats, setStats] = useState<PostHogStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/stats');
      const data = await response.json();
      
      if (data.error) {
        setError(data.error);
      } else {
        setStats(data);
        setError(null);
      }
    } catch (err) {
      setError('Failed to fetch stats');
      console.error('Error fetching stats:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const formatTime = (timestamp: string): string => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch {
      return 'N/A';
    }
  };

  if (loading) {
    return (
      <div className="app loading">
        <div className="loading-spinner"></div>
        <p>Loading PostHog Stats...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app error">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={fetchStats}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>PostHog Analytics Dashboard</h1>
        <p>Last updated: {stats?.last_updated ? formatTime(stats.last_updated) : 'N/A'}</p>
      </header>
      
      <main className="stats-grid">
        <div className="stat-card">
          <h2>Events (24h)</h2>
          <div className="stat-value">{stats?.events_24h || 0}</div>
        </div>
        
        <div className="stat-card">
          <h2>Unique Users (24h)</h2>
          <div className="stat-value">{stats?.unique_users_24h || 0}</div>
        </div>
        
        <div className="stat-card">
          <h2>Page Views (24h)</h2>
          <div className="stat-value">{stats?.page_views_24h || 0}</div>
        </div>
      </main>
    </div>
  );
};

export default App;
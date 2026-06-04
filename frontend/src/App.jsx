import React, { useState, useEffect } from 'react';
import { Activity, Play, Square, Zap, Globe, Clock, CheckCircle, XCircle } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './index.css';

function App() {
  const [url, setUrl] = useState('https://jsonplaceholder.typicode.com/posts');
  const [concurrency, setConcurrency] = useState(50);
  const [isRunning, setIsRunning] = useState(false);
  const [stats, setStats] = useState({
    total_requests: 0,
    successful_requests: 0,
    failed_requests: 0,
    current_rps: 0,
    average_latency_ms: 0,
    active_connections: 0
  });
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    // Connect to WebSocket
    const ws = new WebSocket('ws://127.0.0.1:8000/ws/stats');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setIsRunning(data.is_running);
      setStats(data.stats);
      
      if (data.is_running) {
        setChartData(prev => {
          const newData = [...prev, {
            time: new Date().toLocaleTimeString(),
            rps: data.stats.current_rps,
            latency: data.stats.average_latency_ms
          }];
          return newData.slice(-30); // Keep last 30 data points
        });
      }
    };

    return () => ws.close();
  }, []);

  const handleStart = async () => {
    try {
      await fetch('http://127.0.0.1:8000/api/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, concurrency: parseInt(concurrency) })
      });
      setChartData([]);
    } catch (e) {
      console.error(e);
    }
  };

  const handleStop = async () => {
    try {
      await fetch('http://127.0.0.1:8000/api/stop', { method: 'POST' });
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="dashboard-container">
      <header className="header">
        <div className="logo">
          <Activity className="logo-icon" size={32} />
          API-Pulse
        </div>
        <div className={`status-badge ${isRunning ? 'status-running' : 'status-idle'}`}>
          {isRunning && <div className="pulse-dot"></div>}
          {isRunning ? 'TEST IN PROGRESS' : 'SYSTEM IDLE'}
        </div>
      </header>

      <div className="control-panel">
        <div className="input-group" style={{ flex: 2 }}>
          <label><Globe size={14} style={{display:'inline', marginBottom:'-2px', marginRight:'4px'}}/> Target URL</label>
          <input 
            type="text" 
            value={url} 
            onChange={(e) => setUrl(e.target.value)}
            disabled={isRunning}
          />
        </div>
        <div className="input-group">
          <label><Zap size={14} style={{display:'inline', marginBottom:'-2px', marginRight:'4px'}}/> Concurrency</label>
          <input 
            type="number" 
            value={concurrency} 
            onChange={(e) => setConcurrency(e.target.value)}
            disabled={isRunning}
          />
        </div>
        {!isRunning ? (
          <button className="btn-primary" onClick={handleStart}>
            <Play size={18} /> Launch Attack
          </button>
        ) : (
          <button className="btn-danger" onClick={handleStop}>
            <Square size={18} /> Stop Test
          </button>
        )}
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-title"><Zap size={16} color="var(--accent)" /> Current RPS</div>
          <div className="stat-value">{stats.current_rps.toLocaleString()}</div>
        </div>
        <div className="stat-card">
          <div className="stat-title"><Clock size={16} color="var(--warning)" /> Avg Latency</div>
          <div className="stat-value">{stats.average_latency_ms.toFixed(1)} ms</div>
        </div>
        <div className="stat-card">
          <div className="stat-title"><CheckCircle size={16} color="var(--success)" /> Successful</div>
          <div className="stat-value" style={{color: 'var(--success)'}}>{stats.successful_requests.toLocaleString()}</div>
        </div>
        <div className="stat-card">
          <div className="stat-title"><XCircle size={16} color="var(--accent)" /> Failed</div>
          <div className="stat-value" style={{color: stats.failed_requests > 0 ? 'var(--accent)' : 'inherit'}}>{stats.failed_requests.toLocaleString()}</div>
        </div>
      </div>

      <div className="chart-container">
        <h3 style={{marginBottom: '20px', fontSize: '16px', color: 'var(--text-muted)'}}>Live Performance Metrics</h3>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorRps" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--accent)" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="var(--accent)" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis dataKey="time" stroke="var(--text-muted)" fontSize={12} tickMargin={10} />
            <YAxis stroke="var(--text-muted)" fontSize={12} tickFormatter={(value) => `${value} req/s`} />
            <Tooltip 
              contentStyle={{ backgroundColor: 'rgba(20,20,22,0.9)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px' }}
              itemStyle={{ color: 'var(--text-main)' }}
            />
            <Area type="monotone" dataKey="rps" stroke="var(--accent)" strokeWidth={3} fillOpacity={1} fill="url(#colorRps)" name="Requests / Sec" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default App;

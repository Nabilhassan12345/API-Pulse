import { render, screen, fireEvent } from '@testing-library/react';
import App from '../App';
import { vi } from 'vitest';

// Mock fetch
global.fetch = vi.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ metrics: { cpu_percent: 10, memory_percent: 20 } }),
  })
);

describe('API-Pulse Dashboard', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders logo and header correctly', () => {
    render(<App />);
    expect(screen.getByText('API-Pulse')).toBeInTheDocument();
    expect(screen.getByText('SYSTEM IDLE')).toBeInTheDocument();
  });

  test('Launch Attack button is visible when idle', () => {
    render(<App />);
    const button = screen.getByRole('button', { name: /launch attack/i });
    expect(button).toBeInTheDocument();
  });

  test('clicking Launch Attack triggers fetch API', async () => {
    render(<App />);
    const button = screen.getByRole('button', { name: /launch attack/i });
    fireEvent.click(button);
    expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/api/start', expect.any(Object));
  });

  test('renders StatsGrid correctly', () => {
    render(<App />);
    expect(screen.getByText('Current RPS')).toBeInTheDocument();
    expect(screen.getByText('Avg Latency')).toBeInTheDocument();
    expect(screen.getByText('Successful')).toBeInTheDocument();
    expect(screen.getByText('Failed')).toBeInTheDocument();
  });
});

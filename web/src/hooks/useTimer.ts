import { useState, useCallback, useEffect, useRef } from 'react';

export interface TimerState {
  id: string;
  remainingTime: number;
  remainingPercentage: number;
  urgencyLevel: 'low' | 'medium' | 'high' | 'critical';
  colourIntensity: {
    red: number;
    green: number;
    blue: number;
  };
  facialExpression: string;
  status: 'running' | 'paused' | 'expired';
}

interface UseTimerReturn {
  timerId: string | null;
  timerState: TimerState | null;
  isRunning: boolean;
  isLoading: boolean;
  error: string | null;
  start: () => Promise<void>;
  pause: () => Promise<void>;
  reset: () => Promise<void>;
  setTimerId: (id: string) => void;
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export function useTimer(): UseTimerReturn {
  const [timerId, setTimerId] = useState<string | null>(null);
  const [timerState, setTimerState] = useState<TimerState | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const fetchTimerState = useCallback(async (id: string) => {
    try {
      const response = await fetch(`${API_BASE}/timers/${id}/state`);
      if (!response.ok) {
        throw new Error(`Failed to fetch timer state: ${response.statusText}`);
      }
      const data: TimerState = await response.json();
      setTimerState(data);
      setIsRunning(data.status === 'running');
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    }
  }, []);

  const start = useCallback(async () => {
    if (!timerId) return;
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE}/timers/${timerId}/start`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error(`Failed to start timer: ${response.statusText}`);
      }
      const data: TimerState = await response.json();
      setTimerState(data);
      setIsRunning(true);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  }, [timerId]);

  const pause = useCallback(async () => {
    if (!timerId) return;
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE}/timers/${timerId}/pause`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error(`Failed to pause timer: ${response.statusText}`);
      }
      const data: TimerState = await response.json();
      setTimerState(data);
      setIsRunning(false);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  }, [timerId]);

  const reset = useCallback(async () => {
    if (!timerId) return;
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE}/timers/${timerId}/reset`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error(`Failed to reset timer: ${response.statusText}`);
      }
      const data: TimerState = await response.json();
      setTimerState(data);
      setIsRunning(data.status === 'running');
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  }, [timerId]);

  useEffect(() => {
    if (!timerId) {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
      return;
    }

    fetchTimerState(timerId);

    pollIntervalRef.current = setInterval(() => {
      fetchTimerState(timerId);
    }, 1000);

    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
    };
  }, [timerId, fetchTimerState]);

  return {
    timerId,
    timerState,
    isRunning,
    isLoading,
    error,
    start,
    pause,
    reset,
    setTimerId,
  };
}

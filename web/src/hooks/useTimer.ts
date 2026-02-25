import { useState, useEffect, useCallback } from 'react';
import {
  getTimerState,
  pauseTimer,
  resumeTimer,
  resetTimer,
  configureTimer,
} from '../api';
import { TimerState, UrgencyState, FacialState } from '../types';

const STORAGE_KEY = 'timer_duration';
const POLL_INTERVAL = 1000;

export function useTimer() {
  const [timerState, setTimerState] = useState<TimerState | null>(null);
  const [urgencyState, setUrgencyState] = useState<UrgencyState | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const facialState: FacialState = urgencyState?.facial_expression ?? 'calm';

  const fetchState = useCallback(async () => {
    try {
      setError(null);
      const timer = await getTimerState();
      setTimerState(timer);
      setUrgencyState(timer?.urgency ?? null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    }
  }, []);

  useEffect(() => {
    const initializeDuration = async () => {
      setIsLoading(true);
      await fetchState();
      setIsLoading(false);
    };
    initializeDuration();
  }, [fetchState]);

  useEffect(() => {
    const interval = setInterval(() => {
      fetchState();
    }, POLL_INTERVAL);

    return () => clearInterval(interval);
  }, [fetchState]);

  const configure = useCallback(
    async (duration: number) => {
      try {
        setError(null);
        setIsLoading(true);
        setTimerState(prev => prev ? { ...prev, duration } : null);
        localStorage.setItem(STORAGE_KEY, String(duration));
        await configureTimer(duration);
        await fetchState();
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to configure timer');
      } finally {
        setIsLoading(false);
      }
    },
    [fetchState]
  );

  const reset = useCallback(async () => {
    try {
      setError(null);
      setIsLoading(true);
      setTimerState(prev => prev ? { ...prev, elapsed: 0 } : null);
      await resetTimer();
      await fetchState();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reset timer');
    } finally {
      setIsLoading(false);
    }
  }, [fetchState]);

  const pause = useCallback(async () => {
    try {
      setError(null);
      await pauseTimer();
      await fetchState();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to pause timer');
    }
  }, [fetchState]);

  const resume = useCallback(async () => {
    try {
      setError(null);
      await resumeTimer();
      await fetchState();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to resume timer');
    }
  }, [fetchState]);

  return {
    timerState,
    urgencyState,
    facialState,
    configure,
    reset,
    pause,
    resume,
    isLoading,
    error,
  };
}

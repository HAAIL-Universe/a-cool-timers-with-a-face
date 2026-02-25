import { useState, useEffect, useCallback, useRef } from 'react';
import type { TimerState, UrgencyLevel } from '../types/timer';
import { getTimer, createTimer, resetTimer, getTimerState } from '../api/timerApi';
import { getTimeRemaining, getUrgencyLevel } from '../types/timer';

interface UseTimerReturn {
  state: TimerState | null;
  isLoading: boolean;
  error: string | null;
  timeRemaining: number;
  urgencyLevel: UrgencyLevel | null;
  start: (duration: number) => Promise<void>;
  pause: () => Promise<void>;
  reset: () => Promise<void>;
  isRunning: boolean;
}

export const useTimer = (): UseTimerReturn => {
  const [state, setState] = useState<TimerState | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const timerIdRef = useRef<string | null>(null);

  const timeRemaining = state ? getTimeRemaining(state) : 0;
  const urgencyLevel = state ? getUrgencyLevel(timeRemaining, state.duration_seconds) : null;
  const isRunning = state?.is_running ?? false;

  const pollTimerState = useCallback(async (timerId: string) => {
    try {
      const freshState = await getTimerState(timerId);
      setState(freshState);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to poll timer state');
    }
  }, []);

  const startPolling = useCallback((timerId: string) => {
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current);
    }
    timerIdRef.current = timerId;
    pollingIntervalRef.current = setInterval(() => {
      pollTimerState(timerId);
    }, 1000);
  }, [pollTimerState]);

  const stopPolling = useCallback(() => {
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current);
      pollingIntervalRef.current = null;
    }
  }, []);

  const start = useCallback(
    async (duration: number) => {
      setIsLoading(true);
      setError(null);
      try {
        const newTimer = await createTimer(duration);
        setState(newTimer);
        timerIdRef.current = newTimer.id;
        startPolling(newTimer.id);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to start timer');
      } finally {
        setIsLoading(false);
      }
    },
    [startPolling]
  );

  const pause = useCallback(async () => {
    if (!timerIdRef.current) return;
    setIsLoading(true);
    setError(null);
    try {
      stopPolling();
      const currentTimer = await getTimer(timerIdRef.current);
      setState(currentTimer);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to pause timer');
    } finally {
      setIsLoading(false);
    }
  }, [stopPolling]);

  const reset = useCallback(async () => {
    if (!timerIdRef.current) return;
    setIsLoading(true);
    setError(null);
    try {
      const resetState = await resetTimer(timerIdRef.current);
      setState(resetState);
      if (resetState.is_running) {
        startPolling(timerIdRef.current);
      } else {
        stopPolling();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reset timer');
    } finally {
      setIsLoading(false);
    }
  }, [startPolling, stopPolling]);

  useEffect(() => {
    return () => {
      stopPolling();
    };
  }, [stopPolling]);

  return {
    state,
    isLoading,
    error,
    timeRemaining,
    urgencyLevel,
    start,
    pause,
    reset,
    isRunning,
  };
};

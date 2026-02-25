import { useEffect, useState, useRef, useCallback } from 'react';
import { TimerState, FacialState } from '../types';
import { getTimerState, resetTimer, pauseTimer, resumeTimer, configureTimer } from '../api';

export function useTimer(initialDuration: number = 60) {
  const [timerState, setTimerState] = useState<TimerState>({
    seconds_remaining: initialDuration,
    total_seconds: initialDuration,
    is_running: false,
    is_expired: false,
    status: 'idle',
  });
  
  const [facialState, setFacialState] = useState<FacialState>('neutral');
  const [error, setError] = useState<string | null>(null);
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const calculateFacialState = useCallback((state: TimerState): FacialState => {
    if (state.is_expired) {
      return 'defeated';
    }
    
    if (!state.is_running) {
      return 'neutral';
    }

    const percentageRemaining = (state.seconds_remaining / state.total_seconds) * 100;

    if (percentageRemaining > 50) {
      return 'neutral';
    } else if (percentageRemaining > 25) {
      return 'anxious';
    } else {
      return 'panicked';
    }
  }, []);

  const fetchTimerState = useCallback(async () => {
    try {
      const state = await getTimerState();
      setTimerState(state);
      setFacialState(calculateFacialState(state));
      setError(null);

      if (state.is_expired && pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
        pollingIntervalRef.current = null;
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch timer state');
    }
  }, [calculateFacialState]);

  const handleReset = useCallback(async () => {
    try {
      const state = await resetTimer();
      setTimerState(state);
      setFacialState(calculateFacialState(state));
      setError(null);

      if (!pollingIntervalRef.current && state.is_running) {
        pollingIntervalRef.current = setInterval(() => {
          fetchTimerState();
        }, 500);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reset timer');
    }
  }, [calculateFacialState, fetchTimerState]);

  const handlePause = useCallback(async () => {
    try {
      const state = await pauseTimer();
      setTimerState(state);
      setFacialState(calculateFacialState(state));
      setError(null);

      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
        pollingIntervalRef.current = null;
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to pause timer');
    }
  }, [calculateFacialState]);

  const handleResume = useCallback(async () => {
    try {
      const state = await resumeTimer();
      setTimerState(state);
      setFacialState(calculateFacialState(state));
      setError(null);

      if (!pollingIntervalRef.current) {
        pollingIntervalRef.current = setInterval(() => {
          fetchTimerState();
        }, 500);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to resume timer');
    }
  }, [calculateFacialState, fetchTimerState]);

  const handleConfigure = useCallback(async (duration: number) => {
    try {
      const state = await configureTimer(duration);
      setTimerState(state);
      setFacialState(calculateFacialState(state));
      setError(null);

      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
        pollingIntervalRef.current = null;
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to configure timer');
    }
  }, [calculateFacialState]);

  useEffect(() => {
    fetchTimerState();
  }, [fetchTimerState]);

  useEffect(() => {
    if (timerState.is_running && !pollingIntervalRef.current) {
      pollingIntervalRef.current = setInterval(() => {
        fetchTimerState();
      }, 500);
    }

    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
    };
  }, [timerState.is_running, fetchTimerState]);

  return {
    timerState,
    facialState,
    error,
    onReset: handleReset,
    onPause: handlePause,
    onResume: handleResume,
    onConfigure: handleConfigure,
  };
}

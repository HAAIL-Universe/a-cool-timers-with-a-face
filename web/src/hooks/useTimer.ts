import { useState, useCallback, useEffect } from 'react';
import { TimerState } from '../types/timer';
import {
  createTimer,
  getTimerState,
  startTimer,
  pauseTimer,
  resetTimer,
} from '../api/timerApi';

const DEFAULT_DURATION = 30;
const POLL_INTERVAL = 1000;

export function useTimer(initialDuration: number = DEFAULT_DURATION) {
  const [timerId, setTimerId] = useState<string | null>(null);
  const [timerState, setTimerState] = useState<TimerState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const initTimer = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const timer = await createTimer(initialDuration);
        setTimerId(timer.id);
        const state = await getTimerState(timer.id);
        setTimerState(state);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to create timer');
      } finally {
        setIsLoading(false);
      }
    };

    initTimer();
  }, [initialDuration]);

  useEffect(() => {
    if (!timerId || !timerState?.isRunning) {
      return;
    }

    const pollTimer = async () => {
      try {
        const state = await getTimerState(timerId);
        setTimerState(state);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Poll failed');
      }
    };

    const interval = setInterval(pollTimer, POLL_INTERVAL);
    return () => clearInterval(interval);
  }, [timerId, timerState?.isRunning]);

  const start = useCallback(async () => {
    if (!timerId) {
      return;
    }
    setError(null);
    try {
      const state = await startTimer(timerId);
      setTimerState(state);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start timer');
    }
  }, [timerId]);

  const pause = useCallback(async () => {
    if (!timerId) {
      return;
    }
    setError(null);
    try {
      const state = await pauseTimer(timerId);
      setTimerState(state);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to pause timer');
    }
  }, [timerId]);

  const reset = useCallback(async () => {
    if (!timerId) {
      return;
    }
    setError(null);
    try {
      const state = await resetTimer(timerId);
      setTimerState(state);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reset timer');
    }
  }, [timerId]);

  return {
    timerId,
    timerState,
    error,
    isLoading,
    start,
    pause,
    reset,
  };
}

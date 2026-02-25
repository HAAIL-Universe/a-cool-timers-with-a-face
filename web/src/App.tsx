import { useState } from 'react';
import { TimerContainer } from './components/TimerContainer';
import type { TimerState } from './types/timer';

interface Timer {
  id: string;
  duration: number;
  elapsed: number;
  status: 'running' | 'paused' | 'completed';
}

function useTimer() {
  const [timer, setTimer] = useState<Timer | null>(null);
  const [timerState, setTimerState] = useState<TimerState | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createAndStart = async (duration: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const newTimer: Timer = {
        id: Date.now().toString(),
        duration,
        elapsed: 0,
        status: 'running',
      };
      setTimer(newTimer);
      setTimerState({ elapsed: 0, duration, status: 'running' });
      setIsRunning(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create timer');
    } finally {
      setIsLoading(false);
    }
  };

  const reset = async () => {
    setIsLoading(true);
    setError(null);
    try {
      setTimer(null);
      setTimerState(null);
      setIsRunning(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to reset timer');
    } finally {
      setIsLoading(false);
    }
  };

  return {
    timer,
    timerState,
    isRunning,
    createAndStart,
    reset,
    isLoading,
    error,
  };
}

export function App(): JSX.Element {
  const [duration, setDuration] = useState<number>(30);
  const [inputValue, setInputValue] = useState<string>('30');
  const {
    timer,
    timerState,
    isRunning,
    createAndStart,
    reset,
    isLoading,
    error,
  } = useTimer();

  const handleDurationChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInputValue(value);
    const parsed = parseInt(value, 10);
    if (!isNaN(parsed) && parsed > 0) {
      setDuration(parsed);
    }
  };

  const handleStartPause = async () => {
    if (isRunning) {
      // Pause logic (if implemented in backend)
      return;
    }
    if (!timer) {
      // Create and start a new timer
      await createAndStart(duration);
    } else if (timer.status === 'paused') {
      // Resume existing paused timer (optional)
      await createAndStart(duration);
    }
  };

  const handleReset = async () => {
    await reset();
    setDuration(30);
    setInputValue('30');
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>A Cool Timer with a Face</h1>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}

        {!timer ? (
          <div className="duration-setup">
            <label htmlFor="duration-input">Set Timer Duration (seconds):</label>
            <input
              id="duration-input"
              type="number"
              value={inputValue}
              onChange={handleDurationChange}
              min="1"
              disabled={isLoading}
              placeholder="30"
            />
            <p className="duration-hint">Duration: {duration}s</p>
          </div>
        ) : null}

        <TimerContainer
          timerState={timerState}
          isRunning={isRunning}
          onReset={handleReset}
          onStartPause={handleStartPause}
          isLoading={isLoading}
          duration={duration}
        />
      </main>

      <footer className="app-footer">
        <p>Maintain your fitness cadence with real-time feedback</p>
      </footer>
    </div>
  );
}

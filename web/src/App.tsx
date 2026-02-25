import { useState } from 'react';
import TimerContainer from './components/TimerContainer';
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
      setTimerState({
        id: newTimer.id,
        duration_seconds: duration,
        elapsed_seconds: 0,
        is_running: true,
        urgency_level: 'low',
        created_at: new Date().toISOString(),
        last_reset_at: new Date().toISOString(),
      });
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

  const startPause = async () => {
    if (isRunning) {
      setIsRunning(false);
    } else if (timer) {
      setIsRunning(true);
    }
  };

  return {
    timer,
    timerState,
    isRunning,
    createAndStart,
    reset,
    startPause,
    isLoading,
    error,
  };
}

export function App(): JSX.Element {
  const [selectedDuration, setSelectedDuration] = useState<number>(30);
  const {
    timer,
    timerState,
    isRunning,
    createAndStart,
    reset,
    startPause,
    isLoading,
    error,
  } = useTimer();

  const handleDurationSelect = (duration: number) => {
    if (!isRunning) {
      setSelectedDuration(duration);
    }
  };

  const handleStartPause = async () => {
    if (!timer) {
      await createAndStart(selectedDuration);
    } else {
      await startPause();
    }
  };

  const handleReset = async () => {
    await reset();
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

        <TimerContainer
          timerState={timerState}
          isRunning={isRunning}
          onReset={handleReset}
          onStartPause={handleStartPause}
          onDurationSelect={handleDurationSelect}
          selectedDuration={selectedDuration}
          isLoading={isLoading}
        />
      </main>

      <footer className="app-footer">
        <p>Maintain your fitness cadence with real-time feedback</p>
      </footer>
    </div>
  );
}

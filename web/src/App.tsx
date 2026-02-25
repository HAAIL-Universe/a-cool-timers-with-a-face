import { useEffect, useState } from 'react';
import { TimerContainer } from './components/TimerContainer';
import { useTimer } from './hooks/useTimer';
import { createTimer } from './api/timerApi';
import './styles/global.css';

export function App() {
  const [timerId, setTimerId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { timerState, isRunning, start, pause, reset } = useTimer(timerId);

  useEffect(() => {
    const initializeTimer = async () => {
      try {
        const timer = await createTimer();
        setTimerId(timer.id);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to initialize timer');
      }
    };

    initializeTimer();
  }, []);

  if (error) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', fontSize: '24px', color: '#FF0000' }}>
        Error: {error}
      </div>
    );
  }

  if (!timerId || !timerState) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', fontSize: '24px', color: '#FFFF00' }}>
        Loading...
      </div>
    );
  }

  return <TimerContainer timerState={timerState} isRunning={isRunning} onStart={start} onPause={pause} onReset={reset} />;
}

export default App;

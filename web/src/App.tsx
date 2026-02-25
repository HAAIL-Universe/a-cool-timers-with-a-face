import { useEffect, useState } from 'react';
import { createTimer } from './api/timerApi';
import { useTimer } from './hooks/useTimer';
import TimerContainer from './components/TimerContainer';
import './styles/global.css';

export default function App() {
  const [timerId, setTimerId] = useState<string | null>(null);
  const [initError, setInitError] = useState<string | null>(null);
  const { timerState, isRunning, start, pause, reset } = useTimer(timerId);

  useEffect(() => {
    const initializeTimer = async () => {
      try {
        const timer = await createTimer();
        setTimerId(timer.id);
      } catch (error) {
        setInitError(error instanceof Error ? error.message : 'Failed to initialize timer');
      }
    };

    initializeTimer();
  }, []);

  if (initError) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh', fontSize: '24px', color: '#FF0000' }}>
        Error: {initError}
      </div>
    );
  }

  if (!timerId || !timerState) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh', fontSize: '24px', color: '#FFFF00' }}>
        Loading timer...
      </div>
    );
  }

  return (
    <TimerContainer
      timeRemaining={timerState.timeRemaining}
      urgencyLevel={timerState.urgencyLevel}
      isRunning={isRunning}
      onStart={start}
      onPause={pause}
      onReset={reset}
    />
  );
}

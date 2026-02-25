import React, { useState } from 'react';
import { useTimer } from './hooks/useTimer';
import { TimerDisplay } from './components/TimerDisplay';
import { ControlButtons } from './components/ControlButtons';
import { SettingsPanel } from './components/SettingsPanel';
import { intensityToBackground } from './utils/colour';
import './App.css';

export function App(): JSX.Element {
  const {
    timerState,
    urgencyState,
    facialState,
    configure,
    reset,
    pause,
    resume,
    isLoading,
    error,
  } = useTimer();
  const [settingsOpen, setSettingsOpen] = useState(false);

  if (!timerState || !urgencyState) {
    return <div className="app-container loading">Loading...</div>;
  }

  const isPaused = timerState.is_paused;
  const isExpired = timerState.is_expired;
  const countdown = timerState.countdown;
  const colourIntensity = urgencyState.colour_intensity;

  const handleTogglePause = () => {
    if (isPaused) {
      resume();
    } else {
      pause();
    }
  };

  const handleOpenSettings = () => {
    setSettingsOpen(true);
  };

  const handleCloseSettings = () => {
    setSettingsOpen(false);
  };

  const backgroundGradient = intensityToBackground(colourIntensity);

  const appStyle: React.CSSProperties = {
    background: backgroundGradient,
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '2rem',
    transition: 'background 0.3s ease',
  };

  return (
    <div className="app-container" style={appStyle}>
      <div className="app-content">
        {error && <div className="error-banner">{error}</div>}

        <div className="face-section">
          <div className="facial-state">{facialState}</div>
        </div>

        <div className="display-section">
          <TimerDisplay
            countdown={countdown}
            colourIntensity={colourIntensity}
            isExpired={isExpired}
          />
        </div>

        <div className="controls-section">
          <ControlButtons
            isPaused={isPaused}
            isExpired={isExpired}
            onReset={reset}
            onTogglePause={handleTogglePause}
            onOpenSettings={handleOpenSettings}
          />
        </div>

        {isLoading && <div className="loading-indicator">Syncing...</div>}
      </div>

      <SettingsPanel
        isOpen={settingsOpen}
        onConfigure={configure}
        onClose={handleCloseSettings}
      />
    </div>
  );
}

import React from 'react';
import { useTimer } from './hooks/useTimer';
import TimerDisplay from './components/TimerDisplay';
import FaceComponent from './components/FaceComponent';
import ControlButtons from './components/ControlButtons';
import SettingsPanel from './components/SettingsPanel';
import { getUrgencyColour, getBackgroundColour } from './utils/colour';
import './styles/App.css';

const App: React.FC = () => {
  const { timerState, facialState, error, onReset, onPause, onResume, onConfigure } = useTimer(60);
  const [showSettings, setShowSettings] = React.useState(false);

  const urgencyLevel = timerState.total_seconds > 0
    ? ((timerState.total_seconds - timerState.seconds_remaining) / timerState.total_seconds) * 100
    : 0;

  const urgencyColour = getUrgencyColour(timerState.seconds_remaining, timerState.total_seconds);
  const backgroundColour = timerState.is_expired ? '#4a4a4a' : getBackgroundColour(timerState.seconds_remaining, timerState.total_seconds);

  const handleSettingsClose = () => {
    setShowSettings(false);
  };

  const handleDurationSelect = (duration: number) => {
    onConfigure(duration);
    setShowSettings(false);
  };

  return (
    <div
      className="app-container"
      style={{
        backgroundColor: backgroundColour,
        transition: 'background-color 0.3s ease',
      }}
    >
      <header className="app-header">
        <h1 className="app-title">TIMER FACE</h1>
      </header>

      <main className="app-main">
        <div className="timer-section">
          <FaceComponent facialState={facialState} urgencyLevel={urgencyLevel} />

          <TimerDisplay
            secondsRemaining={timerState.seconds_remaining}
            colour={urgencyColour}
          />

          {timerState.is_expired && (
            <div className="expired-overlay">
              <div className="expired-message">RESET TO CONTINUE</div>
            </div>
          )}
        </div>

        <footer className="app-footer">
          <ControlButtons
            isRunning={timerState.is_running}
            isExpired={timerState.is_expired}
            onReset={onReset}
            onPause={onPause}
            onResume={onResume}
            onSettingsToggle={() => setShowSettings(!showSettings)}
          />

          {error && (
            <div className="error-message">{error}</div>
          )}
        </footer>
      </main>

      {showSettings && (
        <SettingsPanel
          onClose={handleSettingsClose}
          onDurationSelect={handleDurationSelect}
        />
      )}
    </div>
  );
};

export default App;

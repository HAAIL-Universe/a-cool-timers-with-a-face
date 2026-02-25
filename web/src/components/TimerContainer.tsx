import React from 'react';
import { useTimer } from '../hooks/useTimer';
import { TimerDisplay } from './TimerDisplay';
import { FacialAvatar } from './FacialAvatar';
import { BackgroundBar } from './BackgroundBar';
import { ResetButton } from './ResetButton';
import { StartPauseButton } from './StartPauseButton';
import '../styles/timerContainer.css';

export const TimerContainer: React.FC = () => {
  const { timerState, isRunning, start, pause, reset } = useTimer();

  if (!timerState) {
    return <div className="timer-container loading">Loading timer...</div>;
  }

  const urgencyLevel = timerState.urgencyLevel;
  const timeRemaining = timerState.timeRemaining;
  const colourIntensity = timerState.colourIntensity;

  return (
    <div className="timer-container">
      <BackgroundBar colourIntensity={colourIntensity} urgencyLevel={urgencyLevel} />
      
      <div className="timer-content">
        <div className="avatar-section">
          <FacialAvatar
            expression={timerState.facialExpression}
            urgencyLevel={urgencyLevel}
            isPulsing={urgencyLevel === 'critical'}
          />
        </div>

        <div className="display-section">
          <TimerDisplay
            timeRemaining={timeRemaining}
            urgencyLevel={urgencyLevel}
          />
        </div>

        <div className="controls-section">
          <StartPauseButton
            isRunning={isRunning}
            onClick={isRunning ? pause : start}
          />
          <ResetButton
            onClick={reset}
            disabled={!isRunning && timeRemaining === timerState.initialDuration}
          />
        </div>
      </div>
    </div>
  );
};

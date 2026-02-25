import React from 'react';
import { TimerDisplay } from './TimerDisplay';
import { FacialAvatar } from './FacialAvatar';
import { BackgroundBar } from './BackgroundBar';
import { ResetButton } from './ResetButton';
import { StartPauseButton } from './StartPauseButton';
import { TimerState } from '../types/timer';
import '../styles/timerContainer.css';

interface TimerContainerProps {
  timerState: TimerState;
  isRunning: boolean;
  onStart: () => void;
  onPause: () => void;
  onReset: () => void;
}

export const TimerContainer: React.FC<TimerContainerProps> = ({
  timerState,
  isRunning,
  onStart,
  onPause,
  onReset,
}) => {
  const handleStartPause = () => {
    if (isRunning) {
      onPause();
    } else {
      onStart();
    }
  };

  return (
    <div className="timer-container">
      <BackgroundBar urgencyLevel={timerState.urgencyLevel} />
      
      <div className="timer-content">
        <div className="timer-header">
          <FacialAvatar
            urgencyLevel={timerState.urgencyLevel}
            isPulsing={timerState.urgencyLevel === 'critical'}
          />
        </div>

        <div className="timer-display-wrapper">
          <TimerDisplay
            timeRemaining={timerState.timeRemaining}
            urgencyLevel={timerState.urgencyLevel}
          />
        </div>

        <div className="timer-controls">
          <StartPauseButton
            isRunning={isRunning}
            onClick={handleStartPause}
          />
          <ResetButton
            onClick={onReset}
            disabled={timerState.timeRemaining === timerState.initialDuration}
          />
        </div>
      </div>
    </div>
  );
};

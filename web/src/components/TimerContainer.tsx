import React, { useEffect } from 'react';
import TimerDisplay from './TimerDisplay';
import { StartPauseButton } from './StartPauseButton';
import DurationSelector from './DurationSelector';
import { useKeyboard } from '../hooks/useKeyboard';
import BackgroundBar from './BackgroundBar';
import FacialAvatar from './FacialAvatar';

type UrgencyLevel = 'low' | 'medium' | 'high' | 'critical';
type FacialExpression = 'calm' | 'concerned' | 'worried' | 'panicked';

interface TimerState {
  urgencyLevel: UrgencyLevel;
  facialExpression: FacialExpression;
  remainingTime: number;
}

interface TimerContainerProps {
  timerState: TimerState | null;
  isRunning: boolean;
  onReset: () => void;
  onStartPause: () => void;
  onDurationSelect: (d: number) => void;
  selectedDuration: number;
  isLoading: boolean;
}

interface ResetButtonProps {
  onClick: () => void;
  disabled: boolean;
}

const ResetButton: React.FC<ResetButtonProps> = ({ onClick, disabled }) => {
  return (
    <button
      className={`reset-btn ${disabled ? 'disabled' : ''}`}
      onClick={onClick}
      disabled={disabled}
      aria-label="Reset timer"
    >
      Reset
    </button>
  );
};

export default function TimerContainer({
  timerState,
  isRunning,
  onReset,
  onStartPause,
  onDurationSelect,
  selectedDuration,
  isLoading,
}: TimerContainerProps): JSX.Element {
  const urgencyLevel: UrgencyLevel = timerState?.urgencyLevel ?? 'low';
  const facialExpression: FacialExpression =
    timerState?.facialExpression ?? 'calm';
  const isPulsing = urgencyLevel === 'critical' && isRunning;
  const timeRemaining = timerState?.remainingTime ?? 0;

  useKeyboard({
    onSpace: onStartPause,
    onR: onReset,
    enabled: !isLoading,
  });

  return (
    <div className="timer-container">
      <BackgroundBar urgencyLevel={urgencyLevel} isPulsing={isPulsing} />

      <div className="timer-content">
        <div className="avatar-section">
          <FacialAvatar
            expression={facialExpression}
            urgencyLevel={urgencyLevel}
            isPulsing={isPulsing}
          />
        </div>

        <div className="display-section">
          <TimerDisplay
            timeRemaining={timeRemaining}
            urgencyLevel={urgencyLevel}
          />
        </div>

        <div className="duration-section">
          <DurationSelector
            selectedDuration={selectedDuration}
            onSelect={onDurationSelect}
            disabled={isRunning || isLoading}
          />
        </div>

        <div className="controls-section">
          <StartPauseButton
            isRunning={isRunning}
            onClick={onStartPause}
            disabled={isLoading}
          />
          <ResetButton onClick={onReset} disabled={isLoading} />
        </div>

        {isLoading && <div className="loading-indicator">Loading...</div>}
      </div>
    </div>
  );
}

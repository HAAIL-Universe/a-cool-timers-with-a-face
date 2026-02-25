import React from 'react';
import TimerDisplay from './TimerDisplay';
import { StartPauseButton } from './StartPauseButton';

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
  isLoading: boolean;
  duration: number;
}

interface FacialAvatarProps {
  expression: FacialExpression;
  urgencyLevel: UrgencyLevel;
  isPulsing: boolean;
}

interface BackgroundBarProps {
  urgencyLevel: UrgencyLevel;
  isPulsing: boolean;
}

interface ResetButtonProps {
  onClick: () => void;
  disabled: boolean;
}

const BackgroundBar: React.FC<BackgroundBarProps> = ({
  urgencyLevel,
  isPulsing,
}) => {
  return (
    <div
      className={`background-bar urgency-${urgencyLevel} ${
        isPulsing ? 'pulsing' : ''
      }`}
      role="presentation"
    />
  );
};

const FacialAvatar: React.FC<FacialAvatarProps> = ({
  expression,
  urgencyLevel,
  isPulsing,
}) => {
  return (
    <div
      className={`facial-avatar expression-${expression} urgency-${urgencyLevel} ${
        isPulsing ? 'pulsing' : ''
      }`}
      role="img"
      aria-label={`Avatar with ${expression} expression`}
    />
  );
};

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
  isLoading,
  duration,
}: TimerContainerProps): JSX.Element {
  const urgencyLevel: UrgencyLevel = timerState?.urgencyLevel ?? 'low';
  const facialExpression: FacialExpression =
    timerState?.facialExpression ?? 'calm';
  const isPulsing = urgencyLevel === 'critical' && isRunning;
  const timeRemaining = timerState?.remainingTime ?? 0;

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

import React from 'react';
import { UrgencyLevel } from '../types/timer';

interface TimerDisplayProps {
  timeRemaining: number;
  urgencyLevel: UrgencyLevel;
}

const TimerDisplay: React.FC<TimerDisplayProps> = ({
  timeRemaining,
  urgencyLevel,
}) => {
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(Math.max(0, seconds) / 60);
    const secs = Math.max(0, seconds) % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };

  const getBackgroundColor = (): string => {
    switch (urgencyLevel) {
      case 'low':
        return '#2ecc71';
      case 'medium':
        return '#f39c12';
      case 'high':
        return '#e74c3c';
      case 'critical':
        return '#c0392b';
      default:
        return '#2ecc71';
    }
  };

  return (
    <div className="timer-display" style={{ backgroundColor: getBackgroundColor() }}>
      <div className="timer-face">
        <span className="timer-digits">{formatTime(timeRemaining)}</span>
      </div>
    </div>
  );
};

export default TimerDisplay;

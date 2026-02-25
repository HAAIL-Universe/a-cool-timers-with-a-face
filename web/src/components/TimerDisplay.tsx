import React from 'react';
import { UrgencyLevel } from '../types/timer';

interface TimerDisplayProps {
  timeRemaining: number;
  urgencyLevel: UrgencyLevel;
}

const getBackgroundColor = (urgency: UrgencyLevel): string => {
  switch (urgency) {
    case 'low':
      return '#00FF00';
    case 'medium':
      return '#FFFF00';
    case 'high':
      return '#FF8800';
    case 'critical':
      return '#FF0000';
    default:
      return '#00FF00';
  }
};

const formatTime = (seconds: number): string => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
};

export const TimerDisplay: React.FC<TimerDisplayProps> = ({
  timeRemaining,
  urgencyLevel,
}) => {
  const bgColor = getBackgroundColor(urgencyLevel);
  const shouldPulse = urgencyLevel === 'critical';

  return (
    <div
      style={{
        backgroundColor: bgColor,
        padding: '20px',
        borderRadius: '8px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        animation: shouldPulse ? 'pulse 1s infinite' : 'none',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <span style={{ fontSize: '32px', fontWeight: 'bold', color: '#000' }}>
          {formatTime(timeRemaining)}
        </span>
      </div>
      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  );
};

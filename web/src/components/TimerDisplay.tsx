import React from 'react';
import { TimerState, getUrgencyColor, getTimeRemaining, formatTime } from '../types/timer';
import styles from './TimerDisplay.module.css';

interface TimerDisplayProps {
  timerState: TimerState | null;
}

const TimerDisplay: React.FC<TimerDisplayProps> = ({ timerState }) => {
  if (!timerState) {
    return <div className={styles.display}>--:--</div>;
  }

  const timeRemaining = getTimeRemaining(timerState);
  const formattedTime = formatTime(timeRemaining);
  const urgencyColor = getUrgencyColor(timerState.urgency_level);

  return (
    <div
      className={styles.display}
      style={{
        color: urgencyColor,
        textShadow: `0 0 10px ${urgencyColor}`,
      }}
    >
      {formattedTime}
    </div>
  );
};

export default TimerDisplay;

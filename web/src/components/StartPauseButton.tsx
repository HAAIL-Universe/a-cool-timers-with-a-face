import React from 'react';
import '../styles/global.css';

interface StartPauseButtonProps {
  isRunning: boolean;
  onClick: () => void;
  disabled?: boolean;
}

const StartPauseButton: React.FC<StartPauseButtonProps> = ({
  isRunning,
  onClick,
  disabled = false,
}) => {
  return (
    <button
      className="arcade-button start-pause-button"
      onClick={onClick}
      disabled={disabled}
      aria-label={isRunning ? 'Pause timer' : 'Start timer'}
    >
      {isRunning ? 'PAUSE' : 'START'}
    </button>
  );
};

export default StartPauseButton;

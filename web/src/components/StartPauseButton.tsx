import React from 'react';

interface StartPauseButtonProps {
  isRunning: boolean;
  onClick: () => void;
  disabled: boolean;
}

export const StartPauseButton: React.FC<StartPauseButtonProps> = ({
  isRunning,
  onClick,
  disabled,
}) => {
  return (
    <button
      className={`start-pause-btn ${isRunning ? 'running' : 'paused'} ${
        disabled ? 'disabled' : ''
      }`}
      onClick={onClick}
      disabled={disabled}
      aria-label={isRunning ? 'Pause timer' : 'Start timer'}
      style={{
        padding: '12px 24px',
        fontSize: '16px',
        fontWeight: 'bold',
        border: 'none',
        borderRadius: '4px',
        cursor: disabled ? 'not-allowed' : 'pointer',
        backgroundColor: disabled ? '#ccc' : '#007bff',
        color: '#fff',
        transition: 'background-color 0.3s ease',
      }}
    >
      <span className="btn-inner">
        <span className="btn-icon">
          {isRunning ? (
            // Pause icon (two vertical bars)
            <>
              <span className="pause-bar pause-bar-1"></span>
              <span className="pause-bar pause-bar-2"></span>
            </>
          ) : (
            // Play icon (triangle)
            <span className="play-triangle"></span>
          )}
        </span>
        <span className="btn-label">{isRunning ? 'PAUSE' : 'START'}</span>
      </span>
    </button>
  );
};

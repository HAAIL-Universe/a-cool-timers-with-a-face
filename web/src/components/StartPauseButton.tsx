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
  const label = isRunning ? 'PAUSE' : 'START';

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="arcade-button start-pause-button"
      style={{
        position: 'relative',
        width: '120px',
        height: '60px',
        fontSize: '18px',
        fontWeight: 'bold',
        backgroundColor: isRunning ? '#FF6600' : '#00FF00',
        color: '#000000',
        border: '3px solid #000000',
        borderRadius: '4px',
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.5 : 1,
        fontFamily: '"Courier New", monospace',
        textTransform: 'uppercase',
        boxShadow: '0 4px 0 #000000',
        transform: 'translateY(0)',
        transition: 'all 100ms ease-out',
      }}
      onMouseDown={(e) => {
        if (!disabled) {
          const target = e.currentTarget as HTMLButtonElement;
          target.style.transform = 'translateY(2px)';
          target.style.boxShadow = '0 2px 0 #000000';
        }
      }}
      onMouseUp={(e) => {
        if (!disabled) {
          const target = e.currentTarget as HTMLButtonElement;
          target.style.transform = 'translateY(0)';
          target.style.boxShadow = '0 4px 0 #000000';
        }
      }}
      onMouseLeave={(e) => {
        const target = e.currentTarget as HTMLButtonElement;
        target.style.transform = 'translateY(0)';
        target.style.boxShadow = '0 4px 0 #000000';
      }}
    >
      {label}
    </button>
  );
};

export default StartPauseButton;

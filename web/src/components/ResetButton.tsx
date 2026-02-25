import React from 'react';

interface ResetButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

const ResetButton: React.FC<ResetButtonProps> = ({ onClick, disabled = false }) => {
  const baseStyle: React.CSSProperties = {
    padding: '16px 32px',
    fontSize: '24px',
    fontWeight: 'bold',
    fontFamily: 'monospace',
    backgroundColor: disabled ? '#666' : '#00FF00',
    color: '#000',
    border: '4px solid #000',
    borderRadius: '0px',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.5 : 1,
    transition: 'background-color 200ms, transform 100ms',
    boxShadow: disabled ? 'inset 2px 2px 4px rgba(0,0,0,0.3)' : '4px 4px 0px rgba(0,0,0,0.3)',
    outline: 'none',
    minWidth: '64px',
    textTransform: 'uppercase',
    letterSpacing: '2px',
  };

  const activeStyle: React.CSSProperties = disabled ? {} : {
    transform: 'translate(2px, 2px)',
    boxShadow: '2px 2px 0px rgba(0,0,0,0.3)',
  };

  const [isPressed, setIsPressed] = React.useState(false);

  const handleMouseDown = () => !disabled && setIsPressed(true);
  const handleMouseUp = () => setIsPressed(false);
  const handleMouseLeave = () => setIsPressed(false);

  return (
    <button
      style={{
        ...baseStyle,
        ...(isPressed ? activeStyle : {}),
      }}
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseLeave}
      onClick={onClick}
      disabled={disabled}
      aria-label="Reset timer"
    >
      RESET
    </button>
  );
};

export default ResetButton;

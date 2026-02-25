import React from 'react';

export const DURATION_PRESETS: number[] = [15, 30, 45, 60];

export interface DurationSelectorProps {
  selectedDuration: number;
  onSelect: (duration: number) => void;
  disabled: boolean;
}

export const DurationSelector: React.FC<DurationSelectorProps> = ({
  selectedDuration,
  onSelect,
  disabled,
}) => {
  const [pressedButton, setPressedButton] = React.useState<number | null>(null);

  const handleMouseDown = (duration: number) => {
    if (!disabled) {
      setPressedButton(duration);
    }
  };

  const handleMouseUp = () => {
    setPressedButton(null);
  };

  const handleMouseLeave = () => {
    setPressedButton(null);
  };

  const containerStyle: React.CSSProperties = {
    display: 'flex',
    gap: '12px',
    justifyContent: 'center',
    alignItems: 'center',
    flexWrap: 'wrap',
    marginBottom: '2rem',
  };

  const getButtonStyle = (duration: number): React.CSSProperties => {
    const isSelected = selectedDuration === duration;
    const isPressed = pressedButton === duration;

    const baseStyle: React.CSSProperties = {
      padding: '12px 24px',
      fontSize: '18px',
      fontWeight: 'bold',
      fontFamily: 'monospace',
      border: '3px solid #000',
      borderRadius: '0px',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      transition: 'background-color 200ms, transform 100ms',
      outline: 'none',
      textTransform: 'uppercase',
      letterSpacing: '1px',
      minWidth: '80px',
      textAlign: 'center',
    };

    if (disabled) {
      return {
        ...baseStyle,
        backgroundColor: '#999',
        color: '#000',
        boxShadow: 'inset 2px 2px 4px rgba(0,0,0,0.3)',
      };
    }

    if (isSelected) {
      return {
        ...baseStyle,
        backgroundColor: '#FF00FF',
        color: '#000',
        boxShadow: isPressed ? '2px 2px 0px rgba(0,0,0,0.3)' : '4px 4px 0px rgba(0,0,0,0.3)',
        transform: isPressed ? 'translate(2px, 2px)' : 'translate(0, 0)',
      };
    }

    return {
      ...baseStyle,
      backgroundColor: '#00FFFF',
      color: '#000',
      boxShadow: isPressed ? '2px 2px 0px rgba(0,0,0,0.3)' : '4px 4px 0px rgba(0,0,0,0.3)',
      transform: isPressed ? 'translate(2px, 2px)' : 'translate(0, 0)',
    };
  };

  return (
    <div style={containerStyle}>
      {DURATION_PRESETS.map((duration) => (
        <button
          key={duration}
          style={getButtonStyle(duration)}
          onClick={() => onSelect(duration)}
          onMouseDown={() => handleMouseDown(duration)}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseLeave}
          disabled={disabled}
          aria-label={`Set timer to ${duration} seconds`}
          aria-pressed={selectedDuration === duration}
        >
          {duration}s
        </button>
      ))}
    </div>
  );
};

export default DurationSelector;

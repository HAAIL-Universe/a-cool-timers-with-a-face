import React from 'react';

interface FacialAvatarProps {
  urgencyLevel: 'low' | 'medium' | 'high' | 'critical';
  isPulsing?: boolean;
}

const getExpressionPixels = (urgencyLevel: string): boolean[][] => {
  const empty = false;
  const filled = true;

  switch (urgencyLevel) {
    case 'low':
      return [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, filled, filled, 0, 0, 0, 0, filled, filled, 0, 0, 0, 0, 0, 0],
        [0, 0, filled, filled, 0, 0, 0, 0, filled, filled, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, filled, filled, filled, filled, filled, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, filled, filled, filled, filled, filled, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      ];
    case 'medium':
      return [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, filled, filled, 0, 0, 0, 0, filled, filled, 0, 0, 0, 0, 0, 0],
        [0, 0, filled, filled, 0, 0, 0, 0, filled, filled, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, filled, 0, 0, 0, 0, filled, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, filled, filled, 0, 0, filled, filled, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, filled, filled, 0, 0, filled, filled, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      ];
    case 'high':
      return [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, filled, filled, 0, 0, 0, 0, filled, filled, 0, 0, 0, 0, 0, 0],
        [0, 0, filled, filled, 0, 0, 0, 0, filled, filled, 0, 0, 0, 0, 0, 0],
        [0, 0, filled, filled, 0, 0, 0, 0, filled, filled, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, filled, filled, filled, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, filled, filled, filled, filled, filled, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      ];
    case 'critical':
      return [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, filled, filled, 0, 0, 0, 0, filled, filled, 0, 0, 0, 0, 0, 0],
        [0, 0, filled, filled, 0, 0, 0, 0, filled, filled, 0, 0, 0, 0, 0, 0],
        [0, 0, filled, filled, filled, 0, 0, filled, filled, filled, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, filled, filled, filled, filled, filled, filled, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, filled, filled, filled, filled, filled, filled, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, filled, filled, filled, filled, filled, filled, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      ];
    default:
      return new Array(16).fill(0).map(() => new Array(16).fill(false));
  }
};

export const FacialAvatar: React.FC<FacialAvatarProps> = ({
  urgencyLevel,
  isPulsing = false,
}) => {
  const pixels = getExpressionPixels(urgencyLevel);

  const getPixelColor = (isLit: boolean): string => {
    if (!isLit) return 'transparent';
    switch (urgencyLevel) {
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

  return (
    <div
      className={`facial-avatar ${isPulsing ? 'pulsing' : ''}`}
      data-testid="facial-avatar"
      data-urgency={urgencyLevel}
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        className="avatar-grid"
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(16, 1fr)',
          gap: '2px',
          padding: '10px',
          backgroundColor: 'rgba(0, 0, 0, 0.2)',
          borderRadius: '4px',
        }}
      >
        {pixels.map((row, rowIdx) =>
          row.map((isLit, colIdx) => (
            <div
              key={`${rowIdx}-${colIdx}`}
              className="avatar-pixel"
              style={{
                width: '20px',
                height: '20px',
                backgroundColor: getPixelColor(isLit),
                border: '1px solid rgba(0, 0, 0, 0.1)',
              }}
              data-lit={isLit}
            />
          ))
        )}
      </div>
      <style>{`
        .facial-avatar.pulsing {
          animation: pulse 1s infinite;
        }
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  );
};

import React from 'react';
import { UrgencyLevel } from '../types/timer';
import '../animations.css';

interface FacialAvatarProps {
  urgencyLevel: UrgencyLevel;
  isPulsing?: boolean;
}

const FacialAvatar: React.FC<FacialAvatarProps> = ({ urgencyLevel, isPulsing = false }) => {
  const pixelSize = 24;
  const gridSize = 16;
  const canvasSize = pixelSize * gridSize;

  const getExpressionData = (level: UrgencyLevel): { pixels: boolean[][]; color: string } => {
    const safe: boolean[][] = [
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, true, true, false, false, false, false, false, false, false, false, true, true, false, false],
      [false, false, true, true, false, false, false, false, false, false, false, false, true, true, false, false],
      [false, false, true, true, false, false, false, false, false, false, false, false, true, true, false, false],
      [false, false, true, true, false, false, false, false, false, false, false, false, true, true, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, true, true, true, true, true, true, true, true, true, true, false, false, false],
      [false, false, false, true, true, true, true, true, true, true, true, true, true, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
    ];

    const caution: boolean[][] = [
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, true, true, true, false, false, false, false, false, false, true, true, true, false, false],
      [false, false, true, true, true, false, false, false, false, false, false, true, true, true, false, false],
      [false, false, true, true, true, false, false, false, false, false, false, true, true, true, false, false],
      [false, false, true, true, true, false, false, false, false, false, false, true, true, true, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, true, true, true, true, true, true, true, true, true, true, false, false, false],
      [false, false, false, true, true, true, true, true, true, true, true, true, true, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
    ];

    const urgent: boolean[][] = [
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, true, true, true, true, false, false, false, false, true, true, true, true, false, false],
      [false, false, true, true, true, true, false, false, false, false, true, true, true, true, false, false],
      [false, false, true, true, true, true, false, false, false, false, true, true, true, true, false, false],
      [false, false, true, true, true, true, false, false, false, false, true, true, true, true, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, true, true, false, false, false, false, false, false, false, false, false, false, false, true, true],
      [false, true, true, false, false, false, false, false, false, false, false, false, false, false, true, true],
      [false, false, false, true, true, true, true, true, true, true, true, true, true, false, false, false],
      [false, false, false, true, true, true, true, true, true, true, true, true, true, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
    ];

    const critical: boolean[][] = [
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, true, true, true, true, true, false, false, true, true, true, true, true, false, false],
      [false, false, true, true, true, true, true, false, false, true, true, true, true, true, false, false],
      [false, false, true, true, true, true, true, false, false, true, true, true, true, true, false, false],
      [false, false, true, true, true, true, true, false, false, true, true, true, true, true, false, false],
      [false, true, true, false, false, false, false, false, false, false, false, false, false, true, true, false],
      [false, true, true, false, false, false, false, false, false, false, false, false, false, true, true, false],
      [false, true, true, false, false, false, false, false, false, false, false, false, false, true, true, false],
      [false, false, false, true, true, true, true, false, false, true, true, true, true, false, false, false],
      [false, false, false, true, true, true, true, false, false, true, true, true, true, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
      [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
    ];

    const colorMap: Record<UrgencyLevel, string> = {
      safe: '#00FF00',
      caution: '#FFFF00',
      urgent: '#FF8800',
      critical: '#FF0000',
    };

    const pixelMap: Record<UrgencyLevel, boolean[][]> = {
      safe,
      caution,
      urgent,
      critical,
    };

    return {
      pixels: pixelMap[level],
      color: colorMap[level],
    };
  };

  const expression = getExpressionData(urgencyLevel);

  const containerClasses = [
    isPulsing && urgencyLevel === 'critical' ? 'pulse-critical' : 'face-transition',
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div
      className={containerClasses}
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: '2rem',
        position: 'relative',
      }}
    >
      <svg
        width={canvasSize}
        height={canvasSize}
        viewBox={`0 0 ${gridSize} ${gridSize}`}
        style={{
          imageRendering: 'pixelated',
          border: `2px solid ${expression.color}`,
          backgroundColor: '#000000',
        }}
      >
        {expression.pixels.map((row, y) =>
          row.map((isPixel, x) =>
            isPixel ? (
              <rect
                key={`${x}-${y}`}
                x={x}
                y={y}
                width={1}
                height={1}
                fill={expression.color}
              />
            ) : null
          )
        )}
      </svg>
    </div>
  );
};

export default FacialAvatar;

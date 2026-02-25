import React from 'react';
import '../styles/FacialAvatar.css';

export type ExpressionState = 'calm' | 'concerned' | 'stressed' | 'critical';

interface FacialAvatarProps {
  expression: ExpressionState;
  urgencyLevel: 'safe' | 'caution' | 'urgent' | 'critical';
  isPulsing?: boolean;
}

const FacialAvatar: React.FC<FacialAvatarProps> = ({
  expression,
  urgencyLevel,
  isPulsing = false,
}) => {
  const pixelGridClass = `facial-avatar facial-avatar--${expression}`;
  const pulseClass = isPulsing ? 'facial-avatar--pulse' : '';
  const urgencyTintClass = `facial-avatar--tint-${urgencyLevel}`;

  return (
    <div
      className={`${pixelGridClass} ${urgencyTintClass} ${pulseClass}`}
      role="img"
      aria-label={`Face showing ${expression} expression at ${urgencyLevel} urgency`}
    >
      {/* 16x16 grid of pixel divs */}
      {Array.from({ length: 256 }).map((_, idx) => (
        <div
          key={idx}
          className={`pixel pixel--${expression}-${idx}`}
          data-expression={expression}
          data-index={idx}
        />
      ))}
    </div>
  );
};

export default FacialAvatar;

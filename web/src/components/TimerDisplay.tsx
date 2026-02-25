import React from 'react';
import { formatSeconds } from '../utils/format';
import { intensityToColour } from '../utils/colour';

export interface TimerDisplayProps {
  countdown: number;
  colourIntensity: number;
  isExpired: boolean;
}

export function TimerDisplay(props: TimerDisplayProps): JSX.Element {
  const { countdown, colourIntensity, isExpired } = props;

  const displayText = formatSeconds(countdown);
  const colour = intensityToColour(colourIntensity);
  const textColour = isExpired ? '#888888' : colour;

  const containerStyle: React.CSSProperties = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '200px',
    padding: '2rem',
    borderRadius: '12px',
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
  };

  const timerStyle: React.CSSProperties = {
    fontFamily: '"Press Start 2P", system-ui, monospace',
    fontSize: '4rem',
    fontWeight: 'bold',
    color: textColour,
    textShadow: `0 0 10px ${textColour}80, 0 0 20px ${colour}40`,
    letterSpacing: '0.1em',
    margin: 0,
    textAlign: 'center',
    lineHeight: 1,
    transition: 'color 0.3s ease, text-shadow 0.3s ease',
  };

  return (
    <div style={containerStyle}>
      <p style={timerStyle}>{displayText}</p>
    </div>
  );
}

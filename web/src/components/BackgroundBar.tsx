import React from 'react';
import { UrgencyLevel, getUrgencyColor } from '../types/timer';
import '../animations.css';

interface BackgroundBarProps {
  urgencyLevel: UrgencyLevel;
  isPulsing?: boolean;
}

const BackgroundBar: React.FC<BackgroundBarProps> = ({ urgencyLevel, isPulsing = false }) => {
  const baseColor = getUrgencyColor(urgencyLevel);
  const rgbColor = hexToRgb(baseColor);
  const opacity = isPulsing && urgencyLevel === 'critical' ? 0.5 : 0.3;
  const backgroundColor = `rgba(${rgbColor.r}, ${rgbColor.g}, ${rgbColor.b}, ${opacity})`;

  return (
    <div
      className={isPulsing && urgencyLevel === 'critical' ? 'pulse-critical' : 'face-transition'}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor,
        pointerEvents: 'none',
        zIndex: -1,
      }}
    />
  );
};

const hexToRgb = (hex: string): { r: number; g: number; b: number } => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : { r: 0, g: 0, b: 0 };
};

export default BackgroundBar;

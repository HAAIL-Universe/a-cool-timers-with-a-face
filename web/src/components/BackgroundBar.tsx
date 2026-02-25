import React, { useEffect, useState } from 'react';
import { UrgencyLevel, getUrgencyColor } from '../types/timer';

interface BackgroundBarProps {
  urgencyLevel: UrgencyLevel;
  isPulsing?: boolean;
}

const BackgroundBar: React.FC<BackgroundBarProps> = ({ urgencyLevel, isPulsing = false }) => {
  const [opacity, setOpacity] = useState(1);

  useEffect(() => {
    if (!isPulsing || urgencyLevel !== 'critical') {
      setOpacity(1);
      return;
    }

    let animationFrameId: number;
    let startTime = Date.now();

    const animate = () => {
      const elapsed = Date.now() - startTime;
      const cycle = 500;
      const progress = (elapsed % cycle) / cycle;
      const pulse = 0.4 + 0.6 * Math.sin(progress * Math.PI);
      setOpacity(pulse);
      animationFrameId = requestAnimationFrame(animate);
    };

    animationFrameId = requestAnimationFrame(animate);

    return () => cancelAnimationFrame(animationFrameId);
  }, [isPulsing, urgencyLevel]);

  const baseColor = getUrgencyColor(urgencyLevel);
  const rgbColor = hexToRgb(baseColor);
  const backgroundColor = `rgba(${rgbColor.r}, ${rgbColor.g}, ${rgbColor.b}, ${opacity * 0.3})`;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor,
        transition: isPulsing ? 'none' : 'background-color 500ms ease-in-out',
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

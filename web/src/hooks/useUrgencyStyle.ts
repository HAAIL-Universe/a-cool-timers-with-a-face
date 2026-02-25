import { useMemo } from 'react';
import { UrgencyLevel, ColourIntensity } from '../types';

export interface UrgencyStyle {
  backgroundColor: string;
  transition: string;
  className: string;
}

/**
 * Hook deriving inline CSS background-color and transition values from ColourIntensity RGB; adds pulse CSS class when urgencyLevel is 'critical'.
 */
export function useUrgencyStyle(
  colourIntensity: ColourIntensity,
  urgencyLevel: UrgencyLevel
): UrgencyStyle {
  return useMemo(() => {
    const rgbString = `rgb(${colourIntensity.r}, ${colourIntensity.g}, ${colourIntensity.b})`;
    const isPulsing = urgencyLevel === 'critical';
    const className = isPulsing ? 'urgency-pulse' : '';

    return {
      backgroundColor: rgbString,
      transition: 'background-color 500ms ease-in-out',
      className,
    };
  }, [colourIntensity, urgencyLevel]);
}

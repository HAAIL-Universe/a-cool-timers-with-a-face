import { useMemo } from 'react';

export interface ColourIntensity {
  red: number;
  green: number;
  blue: number;
}

export interface UrgencyStyleReturn {
  backgroundColour: string;
  transitionStyle: string;
  pulseClass: string;
  inline: React.CSSProperties;
}

export function useUrgencyStyle(
  colourIntensity: ColourIntensity | undefined,
  urgencyLevel: 'low' | 'medium' | 'high' | 'critical' | undefined
): UrgencyStyleReturn {
  return useMemo(() => {
    const rgb = colourIntensity || { red: 0, green: 255, blue: 0 };
    const urgency = urgencyLevel || 'low';

    const backgroundColour = `rgb(${rgb.red}, ${rgb.green}, ${rgb.blue})`;
    const transitionStyle = 'background-color 500ms ease-in-out';
    const pulseClass = urgency === 'critical' ? 'pulse-critical' : '';

    const inline: React.CSSProperties = {
      backgroundColor: backgroundColour,
      transition: transitionStyle,
    };

    return {
      backgroundColour,
      transitionStyle,
      pulseClass,
      inline,
    };
  }, [colourIntensity, urgencyLevel]);
}

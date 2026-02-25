import { CSSProperties } from 'react';
import { ColourIntensity, UrgencyLevel } from '../types/timer';

interface BackgroundBarProps {
  colourIntensity: ColourIntensity;
  urgencyLevel: UrgencyLevel;
}

const BackgroundBar = ({ colourIntensity, urgencyLevel }: BackgroundBarProps) => {
  const rgbString = `rgb(${colourIntensity.r}, ${colourIntensity.g}, ${colourIntensity.b})`;

  const backgroundStyle: CSSProperties = {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundColor: rgbString,
    transition: 'background-color 0.5s ease-in-out',
    zIndex: -1,
    pointerEvents: 'none',
  };

  return <div style={backgroundStyle} />;
};

export default BackgroundBar;

import React from 'react';

interface ColourIntensity {
  r: number;
  g: number;
  b: number;
}

interface BackgroundBarProps {
  colourIntensity: ColourIntensity;
  urgencyLevel: string;
}

export const BackgroundBar: React.FC<BackgroundBarProps> = ({
  colourIntensity,
  urgencyLevel,
}) => {
  const rgbColor = `rgb(${colourIntensity.r}, ${colourIntensity.g}, ${colourIntensity.b})`;

  return (
    <>
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundColor: rgbColor,
          transition: 'background-color 500ms ease-in-out',
          zIndex: -1,
        }}
        data-testid="background-bar"
        data-urgency={urgencyLevel}
      />
      <style>{`
        body {
          margin: 0;
          padding: 0;
          overflow: hidden;
        }
        html {
          margin: 0;
          padding: 0;
        }
      `}</style>
    </>
  );
};

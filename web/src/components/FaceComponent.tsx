import React from 'react';
import { FacialState } from '../types';
import { intensityToColour } from '../utils/colour';
import './FaceComponent.css';

interface FaceComponentProps {
  facialState: FacialState;
  colourIntensity: number;
}

const FaceComponent: React.FC<FaceComponentProps> = ({
  facialState,
  colourIntensity,
}) => {
  const baseColour = intensityToColour(colourIntensity);

  const getEyePattern = (): React.ReactNode => {
    switch (facialState) {
      case 'calm':
        return (
          <>
            <div className="eye left-eye">
              <div className="pupil" />
            </div>
            <div className="eye right-eye">
              <div className="pupil" />
            </div>
          </>
        );
      case 'anxious':
        return (
          <>
            <div className="eye left-eye anxious">
              <div className="pupil anxious" />
            </div>
            <div className="eye right-eye anxious">
              <div className="pupil anxious" />
            </div>
          </>
        );
      case 'alarm':
        return (
          <>
            <div className="eye left-eye alarm">
              <div className="pupil alarm" />
            </div>
            <div className="eye right-eye alarm">
              <div className="pupil alarm" />
            </div>
          </>
        );
      case 'defeated':
        return (
          <>
            <div className="eye left-eye defeated">
              <div className="pupil defeated" />
            </div>
            <div className="eye right-eye defeated">
              <div className="pupil defeated" />
            </div>
          </>
        );
      default:
        return null;
    }
  };

  const getMouthPattern = (): React.ReactNode => {
    switch (facialState) {
      case 'calm':
        return <div className="mouth calm" />;
      case 'anxious':
        return <div className="mouth anxious" />;
      case 'alarm':
        return <div className="mouth alarm" />;
      case 'defeated':
        return <div className="mouth defeated" />;
      default:
        return null;
    }
  };

  return (
    <div
      className="face-container"
      style={{
        '--face-colour': baseColour,
      } as React.CSSProperties}
    >
      <div className="face-grid">
        <div className="face-eyes">{getEyePattern()}</div>
        <div className="face-mouth">{getMouthPattern()}</div>
      </div>
    </div>
  );
};

export default FaceComponent;

import React from 'react';
import { FacialState } from '../types';
import '../styles/FaceComponent.css';

interface FaceComponentProps {
  facialState: FacialState;
  urgencyLevel: number;
}

const FaceComponent: React.FC<FaceComponentProps> = ({
  facialState,
  urgencyLevel,
}) => {
  const getPixelPattern = (): string => {
    switch (facialState) {
      case 'neutral':
        return 'face-neutral';
      case 'anxious':
        return 'face-anxious';
      case 'panicked':
        return 'face-panicked';
      case 'defeated':
        return 'face-defeated';
      default:
        return 'face-neutral';
    }
  };

  return (
    <div className={`face-container ${getPixelPattern()}`}>
      <div className="face-grid">
        <div className="face-eyes">
          <div className={`eye left-eye ${facialState === 'defeated' ? 'eye-x' : ''}`}>
            {facialState === 'defeated' ? (
              <div className="pixel-x">
                <span className="x-top-left"></span>
                <span className="x-top-right"></span>
                <span className="x-bottom-left"></span>
                <span className="x-bottom-right"></span>
              </div>
            ) : (
              <div className="pupil"></div>
            )}
          </div>
          <div className={`eye right-eye ${facialState === 'defeated' ? 'eye-x' : ''}`}>
            {facialState === 'defeated' ? (
              <div className="pixel-x">
                <span className="x-top-left"></span>
                <span className="x-top-right"></span>
                <span className="x-bottom-left"></span>
                <span className="x-bottom-right"></span>
              </div>
            ) : (
              <div className="pupil"></div>
            )}
          </div>
        </div>

        <div className="face-mouth">
          {facialState === 'defeated' ? (
            <div className="mouth-defeated">
              <span className="pixel pixel-1"></span>
              <span className="pixel pixel-2"></span>
              <span className="pixel pixel-3"></span>
              <span className="pixel pixel-4"></span>
              <span className="pixel pixel-5"></span>
            </div>
          ) : facialState === 'panicked' ? (
            <div className="mouth-o">
              <span className="pixel pixel-1"></span>
              <span className="pixel pixel-2"></span>
              <span className="pixel pixel-3"></span>
              <span className="pixel pixel-4"></span>
            </div>
          ) : facialState === 'anxious' ? (
            <div className="mouth-worried">
              <span className="pixel pixel-1"></span>
              <span className="pixel pixel-2"></span>
              <span className="pixel pixel-3"></span>
            </div>
          ) : (
            <div className="mouth-smile">
              <span className="pixel pixel-1"></span>
              <span className="pixel pixel-2"></span>
              <span className="pixel pixel-3"></span>
            </div>
          )}
        </div>
      </div>

      {facialState === 'defeated' && (
        <div className="tear tear-left"></div>
      )}
      {facialState === 'defeated' && (
        <div className="tear tear-right"></div>
      )}
    </div>
  );
};

export default FaceComponent;

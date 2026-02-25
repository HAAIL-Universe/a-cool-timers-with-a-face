import React from 'react';

export interface ControlButtonsProps {
  isPaused: boolean;
  isExpired: boolean;
  onReset: () => void;
  onTogglePause: () => void;
  onOpenSettings: () => void;
}

export function ControlButtons(props: ControlButtonsProps): JSX.Element {
  const { isPaused, isExpired, onReset, onTogglePause, onOpenSettings } = props;

  return (
    <div className="control-buttons">
      <button
        className={`control-btn start-pause-btn ${isPaused ? 'paused' : 'running'} ${isExpired ? 'expired' : ''}`}
        onClick={onTogglePause}
        disabled={isExpired}
        aria-label={isPaused ? 'Start timer' : 'Pause timer'}
      >
        {isExpired ? '■' : isPaused ? '▶' : '⏸'}
      </button>

      <button
        className="control-btn reset-btn"
        onClick={onReset}
        aria-label="Reset timer"
      >
        ↻
      </button>

      <button
        className="control-btn settings-btn"
        onClick={onOpenSettings}
        aria-label="Open settings"
      >
        ⚙
      </button>
    </div>
  );
}

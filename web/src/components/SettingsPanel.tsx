import React from 'react';

export interface SettingsPanelProps {
  isOpen: boolean;
  onConfigure: (duration: number) => void;
  onClose: () => void;
}

export function SettingsPanel(props: SettingsPanelProps): JSX.Element {
  const { isOpen, onConfigure, onClose } = props;

  if (!isOpen) {
    return <></>;
  }

  const presets = [
    { label: '30s', duration: 30 },
    { label: '60s', duration: 60 },
    { label: '90s', duration: 90 },
    { label: '120s', duration: 120 },
  ];

  return (
    <div className="settings-overlay">
      <div className="settings-panel">
        <div className="settings-header">
          <h2>Settings</h2>
          <button
            className="close-button"
            onClick={onClose}
            aria-label="Close settings"
          >
            ×
          </button>
        </div>

        <div className="settings-content">
          <p className="settings-label">Select Duration</p>
          <div className="preset-buttons">
            {presets.map((preset) => (
              <button
                key={preset.duration}
                className="preset-button"
                onClick={() => {
                  onConfigure(preset.duration);
                  onClose();
                }}
              >
                {preset.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

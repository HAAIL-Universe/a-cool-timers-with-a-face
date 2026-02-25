import React, { useState } from 'react';
import './DurationPicker.css';

interface DurationPickerProps {
  onDurationSelect: (duration: number) => void;
  isTimerRunning: boolean;
}

const PRESETS = [
  { label: '30s', value: 30 },
  { label: '60s', value: 60 },
  { label: '90s', value: 90 },
  { label: '120s', value: 120 },
];

export const DurationPicker: React.FC<DurationPickerProps> = ({
  onDurationSelect,
  isTimerRunning,
}) => {
  const [selectedDuration, setSelectedDuration] = useState<number>(30);

  const handleSelect = (duration: number) => {
    setSelectedDuration(duration);
    onDurationSelect(duration);
  };

  if (isTimerRunning) {
    return null;
  }

  return (
    <div className="duration-picker">
      <div className="duration-picker__label">Select Duration</div>
      <div className="duration-picker__buttons">
        {PRESETS.map((preset) => (
          <button
            key={preset.value}
            className={`duration-picker__button ${
              selectedDuration === preset.value
                ? 'duration-picker__button--active'
                : ''
            }`}
            onClick={() => handleSelect(preset.value)}
            type="button"
            aria-pressed={selectedDuration === preset.value}
          >
            {preset.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default DurationPicker;

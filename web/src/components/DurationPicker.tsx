import { useState } from "react";

interface DurationPickerProps {
  isRunning: boolean;
  onDurationSelect: (duration: number) => void;
}

const PRESET_DURATIONS = [
  { label: "30s", value: 30 },
  { label: "60s", value: 60 },
  { label: "90s", value: 90 },
  { label: "120s", value: 120 },
];

export function DurationPicker({
  isRunning,
  onDurationSelect,
}: DurationPickerProps): JSX.Element {
  const [selectedDuration, setSelectedDuration] = useState<number>(30);

  if (isRunning) {
    return <></>;
  }

  const handleSelect = (duration: number) => {
    setSelectedDuration(duration);
    onDurationSelect(duration);
  };

  return (
    <div className="duration-picker">
      <label htmlFor="duration-select">Workout Duration:</label>
      <div className="duration-buttons">
        {PRESET_DURATIONS.map((preset) => (
          <button
            key={preset.value}
            className={`duration-button ${
              selectedDuration === preset.value ? "active" : ""
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
}

import React from 'react';
import styles from './ResetButton.module.css';

interface ResetButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

const ResetButton: React.FC<ResetButtonProps> = ({ onClick, disabled = false }) => {
  return (
    <button
      className={`${styles.resetButton} ${disabled ? styles.disabled : ''}`}
      onClick={onClick}
      disabled={disabled}
      aria-label="Reset timer"
    >
      RESET
    </button>
  );
};

export default ResetButton;

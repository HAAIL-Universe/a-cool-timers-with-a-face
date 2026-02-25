import { useEffect } from 'react';

interface UseKeyboardShortcutsProps {
  onToggleStartPause: () => void;
  onReset: () => void;
}

export function useKeyboardShortcuts({
  onToggleStartPause,
  onReset,
}: UseKeyboardShortcutsProps): void {
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.code === 'Space') {
        event.preventDefault();
        onToggleStartPause();
      } else if (event.key.toUpperCase() === 'R') {
        event.preventDefault();
        onReset();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [onToggleStartPause, onReset]);
}

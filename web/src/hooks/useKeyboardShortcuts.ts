import { useEffect } from 'react';

interface UseKeyboardShortcutsOptions {
  onSpacebar?: () => void;
  onReset?: () => void;
  disabled?: boolean;
}

export function useKeyboardShortcuts({
  onSpacebar,
  onReset,
  disabled = false,
}: UseKeyboardShortcutsOptions): void {
  useEffect(() => {
    if (disabled) {
      return;
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.code === 'Space') {
        event.preventDefault();
        onSpacebar?.();
      } else if (event.key === 'r' || event.key === 'R') {
        event.preventDefault();
        onReset?.();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onSpacebar, onReset, disabled]);
}

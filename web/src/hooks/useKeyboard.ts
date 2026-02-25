import { useEffect } from 'react';

export interface UseKeyboardOptions {
  onSpace: () => void;
  onR: () => void;
  enabled: boolean;
}

export function useKeyboard(options: UseKeyboardOptions): void {
  const { onSpace, onR, enabled } = options;

  useEffect(() => {
    if (!enabled) return;

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.code === 'Space') {
        event.preventDefault();
        onSpace();
      } else if (event.code === 'KeyR') {
        event.preventDefault();
        onR();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [enabled, onSpace, onR]);
}

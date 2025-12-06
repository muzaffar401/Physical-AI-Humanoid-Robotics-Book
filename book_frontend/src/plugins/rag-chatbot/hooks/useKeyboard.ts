/**
 * useKeyboard hook for detecting keyboard shortcuts.
 * Detects Ctrl+K (or Cmd+K on Mac) to open chat widget.
 */

import { useEffect } from 'react';

interface UseKeyboardOptions {
  onToggle: () => void;
  enabled?: boolean;
}

export function useKeyboard({ onToggle, enabled = true }: UseKeyboardOptions): void {
  useEffect(() => {
    if (!enabled) return;

    const handleKeyDown = (event: KeyboardEvent) => {
      // Check for Ctrl+K (Windows/Linux) or Cmd+K (Mac)
      const isModifierPressed = event.ctrlKey || event.metaKey;
      const isKPressed = event.key === 'k' || event.key === 'K';

      if (isModifierPressed && isKPressed) {
        event.preventDefault();
        event.stopPropagation();
        onToggle();
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [onToggle, enabled]);
}

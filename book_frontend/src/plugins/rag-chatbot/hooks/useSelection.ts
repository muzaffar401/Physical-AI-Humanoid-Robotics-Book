/**
 * useSelection hook - Tracks text selection and manages selection state
 * Implements T054: Track selected text, clear on blur
 * Implements T058g: Minimum selection threshold (10 characters)
 */

import { useState, useEffect, useCallback } from 'react';

export interface SelectionState {
  text: string;
  range: Range | null;
  rect: DOMRect | null;
}

const MIN_SELECTION_LENGTH = 10;

export function useSelection() {
  const [selection, setSelection] = useState<SelectionState>({
    text: '',
    range: null,
    rect: null,
  });

  const handleSelectionChange = useCallback(() => {
    const windowSelection = window.getSelection();

    // Clear if no selection or selection is empty
    if (!windowSelection || windowSelection.rangeCount === 0) {
      setSelection({ text: '', range: null, rect: null });
      return;
    }

    const selectedText = windowSelection.toString().trim();

    // Only show popup if selection meets minimum length (T058g)
    if (selectedText.length < MIN_SELECTION_LENGTH) {
      setSelection({ text: '', range: null, rect: null });
      return;
    }

    try {
      const range = windowSelection.getRangeAt(0);
      const rect = range.getBoundingClientRect();

      // Only update if we have valid positioning info
      if (rect && rect.width > 0 && rect.height > 0) {
        setSelection({
          text: selectedText,
          range,
          rect,
        });
      }
    } catch (error) {
      console.warn('Error getting selection range:', error);
      setSelection({ text: '', range: null, rect: null });
    }
  }, []);

  const clearSelection = useCallback(() => {
    setSelection({ text: '', range: null, rect: null });
    window.getSelection()?.removeAllRanges();
  }, []);

  useEffect(() => {
    // Listen to selection changes
    document.addEventListener('selectionchange', handleSelectionChange);

    // Clear selection on scroll (T058e - edge case handling)
    const handleScroll = () => {
      if (selection.text) {
        // Recalculate position on scroll
        handleSelectionChange();
      }
    };

    // Clear selection on window resize (T058e - edge case handling)
    const handleResize = () => {
      if (selection.text) {
        handleSelectionChange();
      }
    };

    // Clear selection on click outside (T058e - edge case handling)
    const handleClickOutside = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      // Don't clear if clicking on selection popup
      if (!target.closest('.selection-popup')) {
        // Small delay to allow click to register
        setTimeout(() => {
          const windowSelection = window.getSelection();
          if (!windowSelection || windowSelection.toString().trim().length < MIN_SELECTION_LENGTH) {
            setSelection({ text: '', range: null, rect: null });
          }
        }, 100);
      }
    };

    window.addEventListener('scroll', handleScroll, true); // Capture phase
    window.addEventListener('resize', handleResize);
    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
      window.removeEventListener('scroll', handleScroll, true);
      window.removeEventListener('resize', handleResize);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [handleSelectionChange, selection.text]);

  return {
    selectedText: selection.text,
    selectionRange: selection.range,
    selectionRect: selection.rect,
    hasSelection: selection.text.length >= MIN_SELECTION_LENGTH,
    clearSelection,
  };
}

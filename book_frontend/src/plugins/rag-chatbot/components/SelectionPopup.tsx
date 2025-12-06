/**
 * SelectionPopup component - Floating "Ask AI" button that appears on text selection
 * Implements T058a: Create SelectionPopup component
 * Implements T058b: Positioning logic using Range.getBoundingClientRect()
 * Implements T058c: "Ask AI about this" button with icon
 * Implements T058f: CSS animations (fade in/out)
 */

import React, { useMemo } from 'react';
import { createPortal } from 'react-dom';
import '../styles/selection-popup.css';

export interface SelectionPopupProps {
  selectionRect: DOMRect | null;
  onAskAI: () => void;
  visible: boolean;
}

export function SelectionPopup({ selectionRect, onAskAI, visible }: SelectionPopupProps): JSX.Element | null {
  // Calculate optimal position for popup (T058b)
  const position = useMemo(() => {
    if (!selectionRect) {
      return { top: 0, left: 0, show: false };
    }

    const POPUP_HEIGHT = 48; // Approximate button height
    const POPUP_WIDTH = 180; // Approximate button width
    const MARGIN = 8; // Margin from selection
    const VIEWPORT_PADDING = 16; // Padding from viewport edges

    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const scrollX = window.pageXOffset || document.documentElement.scrollLeft;
    const scrollY = window.pageYOffset || document.documentElement.scrollTop;

    // Default position: above and centered on selection
    let top = selectionRect.top + scrollY - POPUP_HEIGHT - MARGIN;
    let left = selectionRect.left + scrollX + (selectionRect.width / 2) - (POPUP_WIDTH / 2);

    // Handle overflow scenarios (T058b - edge case handling)

    // If popup would go above viewport, position below selection instead
    if (top - scrollY < VIEWPORT_PADDING) {
      top = selectionRect.bottom + scrollY + MARGIN;
    }

    // If popup would go off left edge, align to left with padding
    if (left < scrollX + VIEWPORT_PADDING) {
      left = scrollX + VIEWPORT_PADDING;
    }

    // If popup would go off right edge, align to right with padding
    if (left + POPUP_WIDTH > scrollX + viewportWidth - VIEWPORT_PADDING) {
      left = scrollX + viewportWidth - POPUP_WIDTH - VIEWPORT_PADDING;
    }

    // If popup would go off bottom (unlikely but handle it)
    if (top + POPUP_HEIGHT > scrollY + viewportHeight - VIEWPORT_PADDING) {
      top = selectionRect.top + scrollY - POPUP_HEIGHT - MARGIN;
    }

    return {
      top: Math.max(scrollY + VIEWPORT_PADDING, top),
      left: Math.max(scrollX + VIEWPORT_PADDING, left),
      show: true,
    };
  }, [selectionRect]);

  if (!visible || !position.show) {
    return null;
  }

  const popup = (
    <div
      className="selection-popup"
      style={{
        position: 'absolute',
        top: `${position.top}px`,
        left: `${position.left}px`,
      }}
    >
      <button
        className="selection-popup-button"
        onClick={onAskAI}
        aria-label="Ask AI about selected text"
      >
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="selection-popup-icon"
        >
          {/* Sparkle/Star icon */}
          <path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83" />
        </svg>
        <span>Ask AI about this</span>
      </button>
    </div>
  );

  // Render using portal to append to body (ensures proper z-index stacking)
  return createPortal(popup, document.body);
}

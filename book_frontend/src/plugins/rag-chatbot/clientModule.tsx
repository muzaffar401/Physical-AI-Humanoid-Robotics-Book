/**
 * Client-side module for mounting the ChatWidget.
 * This runs in the browser and mounts the widget to the DOM.
 */

import React from 'react';
import { createRoot } from 'react-dom/client';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';
import { ChatWidget } from './components/ChatWidget';

if (ExecutionEnvironment.canUseDOM) {
  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountChatWidget);
  } else {
    mountChatWidget();
  }
}

function mountChatWidget() {
  // Create container if it doesn't exist
  let container = document.getElementById('rag-chatbot-root');
  if (!container) {
    container = document.createElement('div');
    container.id = 'rag-chatbot-root';
    document.body.appendChild(container);
  }

  // Mount React component
  const root = createRoot(container);
  root.render(<ChatWidget />);
}

export default {};

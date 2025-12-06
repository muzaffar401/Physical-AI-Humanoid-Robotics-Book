/**
 * RAG Chatbot Docusaurus Plugin.
 * Registers the chat widget with Docusaurus.
 */

import React from 'react';
import { ChatWidget } from './components/ChatWidget';

// Export the plugin
export default function ragChatbotPlugin() {
  return {
    name: 'rag-chatbot',

    getClientModules() {
      return [require.resolve('./clientModule')];
    },
  };
}

// Export the widget component for direct use if needed
export { ChatWidget };

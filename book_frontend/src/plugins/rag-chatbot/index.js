/**
 * RAG Chatbot Docusaurus Plugin (JavaScript version).
 * Registers the chat widget with Docusaurus.
 */

const path = require('path');

module.exports = function ragChatbotPlugin() {
  return {
    name: 'rag-chatbot',

    getClientModules() {
      return [path.resolve(__dirname, './clientModule.tsx')];
    },
  };
};

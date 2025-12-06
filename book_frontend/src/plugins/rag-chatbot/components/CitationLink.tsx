/**
 * CitationLink component.
 * Displays a clickable citation that navigates to the source chapter.
 */

import React from 'react';
import { SourceChunk } from '../api/chatClient';

interface CitationLinkProps {
  chunk: SourceChunk;
  index: number;
}

export function CitationLink({ chunk, index }: CitationLinkProps): JSX.Element {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    // Navigate to the chapter URL
    window.location.href = chunk.url;
  };

  return (
    <a
      href={chunk.url}
      onClick={handleClick}
      className="citation-link"
      title={`Module ${chunk.module_number}, Chapter ${chunk.chapter_number}: ${chunk.section_title}`}
    >
      [{index + 1}] Module {chunk.module_number}.{chunk.chapter_number}
    </a>
  );
}

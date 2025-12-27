import React from 'react';
import { Source } from './types';

interface SourceProps {
  source: Source;
}

const ChatSource: React.FC<SourceProps> = ({ source }) => {
  return (
    <div className="source">
      <a href={source.url} target="_blank" rel="noopener noreferrer">
        {source.url}
      </a>
      <p>{source.chunk}</p>
    </div>
  );
};

export default ChatSource;
import React from 'react';
import Layout from '@theme-original/Layout';
import RagChat from '@site/src/components/RagChat';

export default function LayoutWrapper(props) {
  return (
    <>
      <Layout {...props} />
      <RagChat />
    </>
  );
}

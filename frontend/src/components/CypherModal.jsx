import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function CypherModal({ isOpen, onClose }) {
  const [cypherText, setCypherText] = useState('');
  const [statementCount, setStatementCount] = useState(0);
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      api.getCypher()
        .then((res) => {
          setCypherText(res.cypher_script);
          setStatementCount(res.statement_count);
        })
        .catch((e) => console.error(e))
        .finally(() => setLoading(false));
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(cypherText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadCypherFile = () => {
    const blob = new Blob([cypherText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `phytotrace_neo4j_${new Date().toISOString().split('T')[0]}.cypher`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto animate-fadeIn">
      <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[85vh] flex flex-col shadow-2xl border border-outline-variant/30 overflow-hidden">
        {/* Header */}
        <div className="p-5 bg-primary-container text-white flex items-center justify-between border-b border-white/10">
          <div className="flex items-center gap-2.5">
            <span className="material-symbols-outlined text-secondary text-[24px]">terminal</span>
            <div>
              <h3 className="font-headline text-lg font-bold">Neo4j Cypher Graph Script</h3>
              <span className="font-mono text-xs text-on-primary-container">
                {statementCount} Idempotent MERGE Constraints &amp; Statements
              </span>
            </div>
          </div>

          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center transition"
          >
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        {/* Code Content */}
        <div className="p-5 flex-1 overflow-y-auto bg-slate-900 text-slate-100 font-mono text-xs">
          {loading ? (
            <div className="flex items-center justify-center py-12 text-slate-400">
              Generating Cypher script from active graph...
            </div>
          ) : (
            <pre className="whitespace-pre-wrap leading-relaxed select-all">
              {cypherText}
            </pre>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 bg-surface-container-low border-t border-outline-variant/30 flex items-center justify-between">
          <button
            onClick={downloadCypherFile}
            className="px-3.5 py-1.5 bg-surface-container-high hover:bg-surface-container border border-outline-variant/40 rounded-lg text-xs font-mono font-semibold flex items-center gap-1.5 transition text-on-surface"
          >
            <span className="material-symbols-outlined text-[16px]">file_download</span>
            <span>Download .cypher File</span>
          </button>

          <div className="flex items-center gap-2">
            <button
              onClick={copyToClipboard}
              className="px-4 py-2 bg-secondary text-white rounded-lg text-xs font-headline font-semibold hover:bg-secondary/90 transition flex items-center gap-1.5 shadow"
            >
              <span className="material-symbols-outlined text-[16px]">
                {copied ? 'check' : 'content_copy'}
              </span>
              <span>{copied ? 'Copied to Clipboard!' : 'Copy Cypher Script'}</span>
            </button>
            <button
              onClick={onClose}
              className="px-3.5 py-2 bg-surface-container-high hover:bg-surface-container rounded-lg text-xs font-headline font-semibold transition text-on-surface"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

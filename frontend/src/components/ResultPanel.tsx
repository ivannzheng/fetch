'use client'

import JsonHighlighter from './JsonHighlighter'

interface ResultPanelProps {
  result: string | null
}

export default function ResultPanel({ result }: ResultPanelProps) {
  return (
    <div className="h-full w-full flex flex-col bg-[#111111] overflow-hidden">
      <div className="flex-shrink-0 h-1 bg-gradient-to-r from-[#00ffff] to-[#bf00ff]"></div>
      <div className="flex-1 bg-[#0a0a0a] min-h-0 max-h-full overflow-hidden relative w-full">
        {result ? (
          <div className="h-full max-h-full overflow-auto">
            <JsonHighlighter jsonString={result} />
          </div>
        ) : (
          <div className="h-full flex items-center justify-center">
            <div className="text-center">
              <div className="text-[#666666] text-sm mb-2">
                Results will appear here after running a query...
              </div>
              <div className="text-xs text-[#555555] font-mono">
                Click "FETCH" to begin data extraction
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

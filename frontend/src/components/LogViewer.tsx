'use client'

import { useEffect, useRef } from 'react'

interface LogViewerProps {
  logs: string[]
  onFetch?: () => void
  isLoading?: boolean
}

export default function LogViewer({ logs, onFetch, isLoading }: LogViewerProps) {
  const logEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  return (
    <div className="h-full w-full flex flex-col bg-[#111111] overflow-hidden">
      <div className="flex-shrink-0 bg-[#111111] border-b border-[#333333] px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="text-lg font-bold bg-gradient-to-r from-[#00ffff] to-[#bf00ff] bg-clip-text text-transparent">
              process logs
            </div>
          </div>
          {onFetch && (
            <button
              onClick={onFetch}
              disabled={isLoading}
              className="cyber-button px-4 py-2 rounded-md font-bold text-xs disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center space-x-1">
                  <div className="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
                  <span>PROCESSING...</span>
                </div>
              ) : (
                <span>FETCH</span>
              )}
            </button>
          )}
        </div>
      </div>
      <div className="flex-1 p-4 overflow-y-auto bg-[#0a0a0a] min-h-0 max-h-full overflow-hidden w-full scrollbar-thin scrollbar-track-transparent scrollbar-thumb-white">
        {logs.length === 0 ? (
          <div className="text-[#666666] text-sm font-mono">
            No logs yet...
          </div>
        ) : (
          <div className="space-y-1 h-full max-h-full overflow-hidden">
            <div className="h-full max-h-full overflow-y-auto">
            {logs.map((log, index) => (
              <div key={index} className="log-entry font-mono text-white">
                <span className="text-white mr-2">[{index + 1}]</span>
                {log}
              </div>
            ))}
              <div ref={logEndRef} />
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

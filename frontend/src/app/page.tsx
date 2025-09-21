'use client'

import { useState } from 'react'
import CodeEditor from '@/components/CodeEditor'
import LogViewer from '@/components/LogViewer'
import ResultPanel from '@/components/ResultPanel'

export default function Home() {
  const [query, setQuery] = useState(`response = requests.post(
    '/fetch',
    json={
        "query": "Enter your query here",
        "output": {
            "field1": "string",
            "field2": "number",
            "field3": "string"
        },
        "max_answers": 10
    }
)`)
  const [logs, setLogs] = useState<string[]>([])
  const [result, setResult] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleFetch = async () => {
    setIsLoading(true)
    setLogs([])
    setResult(null)

    try {
      // Extract JSON from the Python code string using a more robust approach
      const jsonMatch = query.match(/json=\s*(\{[\s\S]*\})/);
      if (!jsonMatch) {
        throw new Error('Could not find JSON payload in the code');
      }

      let jsonString = jsonMatch[1];
      
      // Clean up common JSON syntax issues
      // Remove trailing commas before closing braces/brackets
      jsonString = jsonString.replace(/,(\s*[}\]])/g, '$1');
      
      // Additional cleanup for common issues
      jsonString = jsonString.replace(/,(\s*})/g, '$1'); // Remove trailing commas before }
      jsonString = jsonString.replace(/,(\s*\])/g, '$1'); // Remove trailing commas before ]
      
      console.log('Cleaned JSON string:', jsonString); // Debug log
      
      // Validate JSON before parsing
      try {
        const payload = JSON.parse(jsonString);
        
        // Validate required fields
        if (!payload.query) {
          throw new Error('Missing required field: query');
        }
        if (!payload.output) {
          throw new Error('Missing required field: output');
        }
        if (typeof payload.max_answers !== 'number') {
          throw new Error('max_answers must be a number');
        }
        
        console.log('Validated payload:', payload);

        const response = await fetch('http://localhost:8000/fetch', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body?.getReader()
      if (!reader) {
        throw new Error('No response body')
      }

      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.trim()) {
            try {
              // Remove "data: " prefix if present
              const cleanLine = line.startsWith('data: ') ? line.slice(6) : line;
              const data = JSON.parse(cleanLine)
              if (data.type === 'log') {
                setLogs(prev => [...prev, data.message])
              } else if (data.type === 'result') {
                setResult(JSON.stringify(data.data, null, 2))
              }
            } catch (e) {
              console.error('Error parsing line:', line, e)
            }
          }
        }
      }
      } catch (jsonError) {
        console.error('JSON parsing error:', jsonError)
        setLogs(prev => [...prev, `JSON Error: ${jsonError instanceof Error ? jsonError.message : 'Invalid JSON format'}`])
      }
    } catch (error) {
      console.error('Error:', error)
      setLogs(prev => [...prev, `Error: ${error instanceof Error ? error.message : 'Unknown error'}`])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="h-screen w-screen flex flex-col bg-[#0a0a0a] overflow-hidden fixed inset-0">
      {/* Header */}
      <div className="bg-[#111111] border-b border-[#333333] px-8 py-6 flex-shrink-0 h-20">
        <div className="flex items-center h-full">
          <div className="flex items-center space-x-3">
            <div className="text-2xl font-bold bg-gradient-to-r from-[#00ffff] to-[#bf00ff] bg-clip-text text-transparent">
              fetch
            </div>
            <div className="text-xs text-[#888888] font-mono">
              v1.0.0
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex min-h-0 max-h-full overflow-hidden">
        {/* Left Panel - Query Editor + Logs */}
        <div className="w-1/2 flex flex-col border-r border-[#333333] min-h-0 max-h-full overflow-hidden">
          {/* Top Half - Query Editor */}
          <div className="flex-1 border-b border-[#333333] min-h-0 max-h-1/2 overflow-hidden">
            <CodeEditor value={query} onChange={setQuery} />
          </div>
          {/* Bottom Half - Logs */}
          <div className="flex-1 min-h-0 max-h-1/2 overflow-hidden">
            <LogViewer logs={logs} onFetch={handleFetch} isLoading={isLoading} />
          </div>
        </div>


        {/* Right Panel - Results */}
        <div className="w-1/2 min-h-0 max-h-full overflow-hidden">
          <ResultPanel result={result} />
        </div>
      </div>
    </div>
  )
}
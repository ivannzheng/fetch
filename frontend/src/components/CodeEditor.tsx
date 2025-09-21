'use client'

import CodeMirror from '@uiw/react-codemirror'
import { json } from '@codemirror/lang-json'
import { oneDark } from '@codemirror/theme-one-dark'

interface CodeEditorProps {
  value: string
  onChange: (value: string) => void
}

export default function CodeEditor({ value, onChange }: CodeEditorProps) {
  return (
    <div className="h-full w-full flex flex-col bg-[#111111] border-r border-[#333333] overflow-hidden">
      <div className="flex-shrink-0 h-1 bg-gradient-to-r from-[#00ffff] to-[#bf00ff]"></div>
      <div className="flex-1 min-h-0 max-h-full overflow-hidden relative w-full">
        <CodeMirror
          value={value}
          onChange={onChange}
          extensions={[json(), oneDark]}
          basicSetup={{
            lineNumbers: true,
            foldGutter: true,
            dropCursor: false,
            allowMultipleSelections: false,
            indentOnInput: true,
            bracketMatching: true,
            closeBrackets: true,
            autocompletion: true,
            highlightSelectionMatches: false,
            searchKeymap: true,
          }}
          className="h-full overflow-auto"
        />
      </div>
    </div>
  )
}

'use client'

interface JsonHighlighterProps {
  jsonString: string
}

export default function JsonHighlighter({ jsonString }: JsonHighlighterProps) {
  const highlightJson = (json: string) => {
    try {
      const parsed = JSON.parse(json)
      const formatted = JSON.stringify(parsed, null, 2)
      
      return formatted
        .replace(/"([^"]+)":/g, '<span class="json-key">"$1":</span>')
        .replace(/: "([^"]*)"/g, ': <span class="json-string">"$1"</span>')
        .replace(/: (\d+)/g, ': <span class="json-number">$1</span>')
        .replace(/: (true|false)/g, ': <span class="json-boolean">$1</span>')
        .replace(/: null/g, ': <span class="json-null">null</span>')
        .replace(/([{}[\]])/g, '<span class="json-punctuation">$1</span>')
    } catch {
      return jsonString
    }
  }

  return (
    <pre 
      className="text-sm font-mono leading-relaxed p-4 overflow-auto h-full"
      dangerouslySetInnerHTML={{ __html: highlightJson(jsonString) }}
    />
  )
}

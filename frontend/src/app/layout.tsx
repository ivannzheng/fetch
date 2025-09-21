import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'fetch',
  description: 'Transform the internet into a structured database',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0a0a0a] text-white overflow-hidden">
        {children}
      </body>
    </html>
  )
}
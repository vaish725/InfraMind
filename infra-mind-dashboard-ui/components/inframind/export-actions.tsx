"use client"

import { useState } from "react"
import { Download, FileText, RefreshCw, History, ChevronDown, ChevronRight, Copy, Check } from "lucide-react"
import { Button } from "@/components/ui/button"
import type { AnalysisResult } from "./types"

interface ExportActionsProps {
  result: AnalysisResult
  onNewAnalysis: () => void
}

export function ExportActions({ result, onNewAnalysis }: ExportActionsProps) {
  const [showRaw, setShowRaw] = useState(false)
  const [copied, setCopied] = useState(false)

  const copyToClipboard = () => {
    navigator.clipboard.writeText(JSON.stringify(result, null, 2))
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const downloadJSON = () => {
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `${result.incidentId}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  const downloadMarkdown = () => {
    const md = `# Incident Report: ${result.incidentId}

## Executive Summary
${result.executiveSummary}

## Root Cause
${result.rootCause}
Confidence: ${result.rootCauseConfidence}% (${result.confidenceLabel})

## Contributing Factors
${result.contributingFactors.map((f) => `- ${f}`).join("\n")}

## Symptoms
${result.symptoms.map((s) => `- ${s}`).join("\n")}

## Causal Chain
${result.causalChain.map((s) => `${s.stepNumber}. [${s.type}] ${s.event} (${s.service}, ${s.confidence}%)`).join("\n")}

## Recommended Fixes
${result.fixes.map((f) => `- [${f.priority}] ${f.title}`).join("\n")}
`
    const blob = new Blob([md], { type: "text/markdown" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `${result.incidentId}.md`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-4">
      <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
        <div className="mb-4 flex items-center gap-2">
          <Download className="h-5 w-5 text-[#667eea]" />
          <h3 className="text-lg font-semibold text-[#1e3a8a]">Export & Actions</h3>
        </div>

        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          <Button
            onClick={downloadJSON}
            className="h-10 bg-[#3b82f6] text-white hover:bg-[#2563eb]"
          >
            <Download className="mr-2 h-4 w-4" />
            JSON
          </Button>
          <Button
            onClick={downloadMarkdown}
            variant="outline"
            className="h-10 border-border text-[#374151] hover:bg-[#f8fafc] bg-transparent"
          >
            <FileText className="mr-2 h-4 w-4" />
            Markdown
          </Button>
          <Button
            onClick={onNewAnalysis}
            variant="outline"
            className="h-10 border-border text-[#374151] hover:bg-[#f8fafc] bg-transparent"
          >
            <RefreshCw className="mr-2 h-4 w-4" />
            New
          </Button>
          <Button
            variant="outline"
            className="h-10 border-border text-[#374151] hover:bg-[#f8fafc] bg-transparent"
          >
            <History className="mr-2 h-4 w-4" />
            History
          </Button>
        </div>
      </div>

      <div className="rounded-xl border border-border bg-card shadow-sm">
        <button
          onClick={() => setShowRaw(!showRaw)}
          className="flex w-full items-center gap-2 px-6 py-3 text-sm font-medium text-[#667eea] hover:bg-[#f8fafc] transition-colors rounded-xl"
          type="button"
        >
          {showRaw ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
          Advanced: View Raw JSON Data
        </button>

        {showRaw && (
          <div className="border-t border-border p-4">
            <div className="relative">
              <button
                onClick={copyToClipboard}
                className="absolute right-2 top-2 flex items-center gap-1 rounded-md bg-[#334155] px-2 py-1 text-xs text-[#94a3b8] transition-colors hover:bg-[#475569] hover:text-[#e2e8f0]"
                type="button"
              >
                {copied ? (
                  <>
                    <Check className="h-3 w-3" /> Copied
                  </>
                ) : (
                  <>
                    <Copy className="h-3 w-3" /> Copy
                  </>
                )}
              </button>
              <pre className="max-h-96 overflow-auto rounded-lg bg-[#1e293b] p-4 pt-10 text-xs text-[#e2e8f0] font-mono">
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

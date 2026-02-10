"use client"

import { useState } from "react"
import { Brain, CheckCircle2, BarChart3, ChevronDown, ChevronRight } from "lucide-react"
import type { ReasoningStep } from "./types"

interface ReasoningProcessProps {
  steps: ReasoningStep[]
}

export function ReasoningProcess({ steps }: ReasoningProcessProps) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="rounded-xl border border-border bg-card shadow-sm">
      <div className="p-6">
        <div className="flex items-center gap-2">
          <Brain className="h-5 w-5 text-[#667eea]" />
          <div>
            <h3 className="text-lg font-semibold text-[#1e3a8a]">AI Reasoning Process</h3>
            <p className="text-sm text-muted-foreground">
              Step-by-step breakdown of how Gemini AI analyzed this incident
            </p>
          </div>
        </div>
      </div>

      <div className="border-t border-border">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex w-full items-center gap-2 px-6 py-3 text-sm font-medium text-[#667eea] hover:bg-[#f8fafc] transition-colors"
          type="button"
        >
          {isOpen ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
          View Detailed Reasoning Steps
        </button>

        {isOpen && (
          <div className="space-y-4 px-6 pb-6">
            {steps.map((step) => (
              <div key={step.stepNumber} className="rounded-lg border border-border bg-[#f8fafc] p-5">
                <div className="mb-3 flex items-center gap-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-[#667eea] to-[#764ba2] text-sm font-bold text-white">
                    {step.stepNumber}
                  </div>
                  <h4 className="text-sm font-semibold text-[#1e3a8a]">{step.title}</h4>
                </div>

                <div className="space-y-3 pl-11">
                  <div>
                    <div className="mb-1 flex items-center gap-1.5">
                      <CheckCircle2 className="h-3.5 w-3.5 text-[#10b981]" />
                      <span className="text-xs font-semibold uppercase tracking-wider text-[#64748b]">Conclusion</span>
                    </div>
                    <p className="text-sm leading-relaxed text-[#374151]">{step.conclusion}</p>
                  </div>

                  {step.evidence.length > 0 && (
                    <div>
                      <div className="mb-1.5 flex items-center gap-1.5">
                        <BarChart3 className="h-3.5 w-3.5 text-[#3b82f6]" />
                        <span className="text-xs font-semibold uppercase tracking-wider text-[#64748b]">
                          Supporting Evidence
                        </span>
                      </div>
                      <ul className="space-y-1">
                        {step.evidence.map((item, i) => (
                          <li key={i} className="font-mono text-xs text-[#374151] bg-card rounded px-2 py-1 border border-border">
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

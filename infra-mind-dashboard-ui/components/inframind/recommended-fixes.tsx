"use client"

import { useState } from "react"
import { Lightbulb, AlertCircle, Clock, Calendar, Wrench, TrendingUp, ChevronDown, ChevronUp } from "lucide-react"
import type { Fix } from "./types"

interface RecommendedFixesProps {
  fixes: Fix[]
}

function getPriorityConfig(priority: Fix["priority"]) {
  switch (priority) {
    case "IMMEDIATE":
      return {
        badge: "bg-[#fee2e2] text-[#dc2626]",
        icon: AlertCircle,
        sectionTitle: "Immediate Action Required",
      }
    case "SHORT_TERM":
      return {
        badge: "bg-[#fef3c7] text-[#f59e0b]",
        icon: Clock,
        sectionTitle: "Short-term Improvements",
      }
    case "LONG_TERM":
      return {
        badge: "bg-[#dbeafe] text-[#3b82f6]",
        icon: Calendar,
        sectionTitle: "Long-term Strategy",
      }
  }
}

function FixCard({ fix }: { fix: Fix }) {
  const [expanded, setExpanded] = useState(false)
  const config = getPriorityConfig(fix.priority)
  const hasDetails = fix.implementationSteps || fix.expectedImpact

  return (
    <div className="rounded-lg border border-border bg-card p-5 shadow-sm transition-shadow hover:shadow-md">
      <div className="mb-3 flex flex-wrap items-center gap-2">
        <span className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${config.badge}`}>
          {fix.priority.replace("_", "-")}
        </span>
        <span className="rounded-full bg-[#f3f4f6] px-2.5 py-0.5 text-xs font-medium text-[#6b7280]">
          {fix.categoryIcon} {fix.category}
        </span>
      </div>

      <p className="text-[15px] font-medium leading-relaxed text-[#374151]">{fix.title}</p>

      {hasDetails && (
        <>
          <button
            onClick={() => setExpanded(!expanded)}
            className="mt-3 flex items-center gap-1 text-xs font-medium text-[#667eea] hover:text-[#764ba2] transition-colors"
            type="button"
          >
            {expanded ? (
              <>
                <ChevronUp className="h-3.5 w-3.5" /> Hide details
              </>
            ) : (
              <>
                <ChevronDown className="h-3.5 w-3.5" /> Show details
              </>
            )}
          </button>

          {expanded && (
            <div className="mt-3 space-y-3 border-t border-border pt-3">
              {fix.implementationSteps && (
                <div>
                  <div className="mb-1.5 flex items-center gap-1.5">
                    <Wrench className="h-3.5 w-3.5 text-[#64748b]" />
                    <span className="text-xs font-semibold uppercase tracking-wider text-[#64748b]">
                      Implementation Steps
                    </span>
                  </div>
                  <p className="text-sm leading-relaxed text-[#374151]">{fix.implementationSteps}</p>
                </div>
              )}
              {fix.expectedImpact && (
                <div>
                  <div className="mb-1.5 flex items-center gap-1.5">
                    <TrendingUp className="h-3.5 w-3.5 text-[#64748b]" />
                    <span className="text-xs font-semibold uppercase tracking-wider text-[#64748b]">
                      Expected Impact
                    </span>
                  </div>
                  <p className="text-sm leading-relaxed text-[#374151]">{fix.expectedImpact}</p>
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  )
}

export function RecommendedFixes({ fixes }: RecommendedFixesProps) {
  const priorities: Fix["priority"][] = ["IMMEDIATE", "SHORT_TERM", "LONG_TERM"]

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
        <div className="flex items-center gap-2">
          <Lightbulb className="h-5 w-5 text-[#667eea]" />
          <div>
            <h3 className="text-lg font-semibold text-[#1e3a8a]">Recommended Fixes</h3>
            <p className="text-sm text-muted-foreground">
              Prioritized action items to resolve and prevent this incident
            </p>
          </div>
        </div>
      </div>

      {priorities.map((priority) => {
        const fixesForPriority = fixes.filter((f) => f.priority === priority)
        if (fixesForPriority.length === 0) return null

        const config = getPriorityConfig(priority)
        const Icon = config.icon

        return (
          <div key={priority} className="space-y-3">
            <div className="flex items-center gap-2 rounded-lg border border-border bg-[#f8fafc] px-4 py-2.5">
              <Icon className="h-4 w-4 text-[#667eea]" />
              <span className="text-sm font-semibold text-[#1e3a8a]">{config.sectionTitle}</span>
            </div>

            <div className="space-y-3 pl-2">
              {fixesForPriority.map((fix, i) => (
                <FixCard key={i} fix={fix} />
              ))}
            </div>
          </div>
        )
      })}
    </div>
  )
}

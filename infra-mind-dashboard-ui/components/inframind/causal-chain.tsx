import { Link2, AlertTriangle, ClipboardList, RefreshCw, ArrowDown } from "lucide-react"
import type { CausalStep } from "./types"

interface CausalChainProps {
  steps: CausalStep[]
}

function getStepStyle(type: CausalStep["type"]) {
  switch (type) {
    case "ROOT_CAUSE":
      return {
        bg: "bg-[#fee2e2]",
        border: "border-[#dc2626]",
        text: "text-[#dc2626]",
        bar: "bg-[#dc2626]",
        icon: AlertTriangle,
        label: "ROOT CAUSE",
      }
    case "SYMPTOM":
      return {
        bg: "bg-[#dbeafe]",
        border: "border-[#3b82f6]",
        text: "text-[#3b82f6]",
        bar: "bg-[#3b82f6]",
        icon: ClipboardList,
        label: "SYMPTOM",
      }
    case "PROPAGATION":
      return {
        bg: "bg-[#f3f4f6]",
        border: "border-[#6b7280]",
        text: "text-[#6b7280]",
        bar: "bg-[#6b7280]",
        icon: RefreshCw,
        label: "PROPAGATION",
      }
  }
}

export function CausalChain({ steps }: CausalChainProps) {
  return (
    <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
      <div className="mb-6 flex items-center gap-2">
        <Link2 className="h-5 w-5 text-[#667eea]" />
        <h3 className="text-lg font-semibold text-[#1e3a8a]">Causal Chain Visualization</h3>
      </div>

      <div className="space-y-0">
        {steps.map((step, index) => {
          const style = getStepStyle(step.type)
          const Icon = style.icon

          return (
            <div key={step.stepNumber}>
              <div
                className={`rounded-lg border-l-4 ${style.border} ${style.bg} p-5 transition-shadow hover:shadow-md`}
              >
                <div className="mb-3 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Icon className={`h-5 w-5 ${style.text}`} />
                    <span className={`text-xs font-bold uppercase tracking-wider ${style.text}`}>
                      Step {step.stepNumber} &middot; {style.label}
                    </span>
                  </div>
                  <span
                    className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${style.bg} ${style.text} border ${style.border}`}
                  >
                    {step.confidenceLabel} Confidence
                  </span>
                </div>

                <p className="mb-3 text-[15px] font-medium leading-relaxed text-[#374151]">{step.event}</p>

                <div className="flex items-center justify-between">
                  <span className="text-xs text-[#64748b]">
                    Service: <span className="font-medium text-[#374151]">{step.service}</span>
                  </span>
                  <div className="flex items-center gap-2">
                    <div className="h-2 w-24 overflow-hidden rounded-full bg-black/10">
                      <div
                        className={`h-full rounded-full ${style.bar} transition-all`}
                        style={{ width: `${step.confidence}%` }}
                      />
                    </div>
                    <span className={`text-xs font-semibold ${style.text}`}>{step.confidence}%</span>
                  </div>
                </div>
              </div>

              {index < steps.length - 1 && (
                <div className="flex justify-center py-2">
                  <ArrowDown className="h-6 w-6 text-[#9ca3af]" />
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

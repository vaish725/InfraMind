import { BarChart3 } from "lucide-react"

interface MetricsDashboardProps {
  confidence: number
  confidenceLabel: "HIGH" | "MEDIUM" | "LOW"
  stepsCount: number
  factorsCount: number
  fixesCount: number
}

export function MetricsDashboard({
  confidence,
  confidenceLabel,
  stepsCount,
  factorsCount,
  fixesCount,
}: MetricsDashboardProps) {
  const metrics = [
    { value: `${confidence}%`, label: "Confidence", sublabel: confidenceLabel },
    { value: stepsCount, label: "Reasoning", sublabel: "Steps" },
    { value: factorsCount, label: "Contributing", sublabel: "Factors" },
    { value: fixesCount, label: "Recommended", sublabel: "Fixes" },
  ]

  return (
    <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
      <div className="mb-5 flex items-center gap-2">
        <BarChart3 className="h-5 w-5 text-[#667eea]" />
        <h3 className="text-lg font-semibold text-[#1e3a8a]">Analysis Metrics</h3>
      </div>

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        {metrics.map((metric) => (
          <div
            key={metric.label}
            className="flex flex-col items-center rounded-lg border border-border bg-[#f8fafc] p-4 transition-shadow hover:shadow-md"
          >
            <span className="text-3xl font-bold text-[#1e3a8a]">{metric.value}</span>
            <span className="mt-1 text-xs font-medium text-[#64748b]">{metric.label}</span>
            <span className="text-xs font-semibold uppercase text-[#667eea]">{metric.sublabel}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

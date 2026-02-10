interface ExecutiveSummaryProps {
  summary: string
  rootCause: string
  rootCauseConfidence: number
  confidenceLabel: "HIGH" | "MEDIUM" | "LOW"
}

function getConfidenceStyle(label: "HIGH" | "MEDIUM" | "LOW") {
  switch (label) {
    case "HIGH":
      return { bg: "bg-[#dcfce7]", text: "text-[#10b981]", bar: "bg-[#10b981]" }
    case "MEDIUM":
      return { bg: "bg-[#fef3c7]", text: "text-[#f59e0b]", bar: "bg-[#f59e0b]" }
    case "LOW":
      return { bg: "bg-[#fee2e2]", text: "text-[#dc2626]", bar: "bg-[#dc2626]" }
  }
}

export function ExecutiveSummary({
  summary,
  rootCause,
  rootCauseConfidence,
  confidenceLabel,
}: ExecutiveSummaryProps) {
  const style = getConfidenceStyle(confidenceLabel)

  return (
    <div className="overflow-hidden rounded-xl border border-border bg-gradient-to-br from-[#eff6ff] to-card shadow-sm">
      <div className="border-l-4 border-l-[#3b82f6] p-6">
        <h3 className="mb-3 text-lg font-semibold text-[#1e3a8a]">Executive Summary</h3>
        <p className="leading-relaxed text-[#374151]">{summary}</p>
      </div>

      <div className="border-t border-border">
        <div className="flex flex-col gap-4 border-l-4 border-l-[#3b82f6] p-6 md:flex-row md:items-start md:justify-between">
          <div className="flex-1">
            <h4 className="mb-2 text-base font-semibold text-[#1e3a8a]">Root Cause</h4>
            <p className="leading-relaxed text-[#374151]">{rootCause}</p>
          </div>

          <div className="flex-shrink-0 md:ml-6">
            <div className={`flex flex-col items-center rounded-lg ${style.bg} px-5 py-3`}>
              <span className={`text-2xl font-bold ${style.text}`}>{rootCauseConfidence}%</span>
              <span className={`text-xs font-semibold uppercase ${style.text}`}>{confidenceLabel}</span>
              <div className="mt-2 h-1.5 w-20 overflow-hidden rounded-full bg-black/10">
                <div
                  className={`h-full rounded-full ${style.bar} transition-all`}
                  style={{ width: `${rootCauseConfidence}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

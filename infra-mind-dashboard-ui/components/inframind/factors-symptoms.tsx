import { AlertTriangle, Activity } from "lucide-react"

interface FactorsSymptomsProps {
  contributingFactors: string[]
  symptoms: string[]
}

export function FactorsSymptoms({ contributingFactors, symptoms }: FactorsSymptomsProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
        <div className="mb-4 flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-[#f59e0b]" />
          <h3 className="text-base font-semibold text-[#1e3a8a]">Contributing Factors</h3>
        </div>
        <ul className="space-y-3">
          {contributingFactors.map((factor, i) => (
            <li key={i} className="flex gap-3 text-sm leading-relaxed text-[#374151]">
              <span className="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-[#f59e0b]" />
              {factor}
            </li>
          ))}
        </ul>
      </div>

      <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
        <div className="mb-4 flex items-center gap-2">
          <Activity className="h-5 w-5 text-[#3b82f6]" />
          <h3 className="text-base font-semibold text-[#1e3a8a]">Symptoms</h3>
        </div>
        <ul className="space-y-3">
          {symptoms.map((symptom, i) => (
            <li key={i} className="flex gap-3 text-sm leading-relaxed text-[#374151]">
              <span className="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-[#3b82f6]" />
              {symptom}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

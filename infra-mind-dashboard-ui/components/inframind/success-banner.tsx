import { CheckCircle2 } from "lucide-react"

interface SuccessBannerProps {
  incidentId: string
}

export function SuccessBanner({ incidentId }: SuccessBannerProps) {
  return (
    <div className="relative overflow-hidden rounded-xl bg-gradient-to-r from-[#667eea] to-[#764ba2] p-8 text-center shadow-lg">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_50%,rgba(255,255,255,0.1),transparent)]" />
      <div className="relative">
        <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-white/20">
          <CheckCircle2 className="h-7 w-7 text-white" />
        </div>
        <h2 className="text-2xl font-bold text-white">Analysis Complete</h2>
        <p className="mt-2 text-sm text-white/80 font-mono">
          Incident ID: {incidentId}
        </p>
      </div>
    </div>
  )
}

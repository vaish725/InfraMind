"use client"

import { useState, useCallback } from "react"
import { Header } from "./header"
import { AnalysisForm, type AnalysisInput } from "./analysis-form"
import { SuccessBanner } from "./success-banner"
import { MetricsDashboard } from "./metrics-dashboard"
import { ExecutiveSummary } from "./executive-summary"
import { FactorsSymptoms } from "./factors-symptoms"
import { CausalChain } from "./causal-chain"
import { RecommendedFixes } from "./recommended-fixes"
import { ReasoningProcess } from "./reasoning-process"
import { ExportActions } from "./export-actions"
import type { AnalysisResult } from "./types"
import { History, Settings, ServerCrash, AlertCircle } from "lucide-react"
import { analyzeIncident } from "@/lib/api-client"
import { transformBackendResponse } from "@/lib/transform"
import { useToast } from "@/hooks/use-toast"

type Tab = "analysis" | "history" | "settings"

export function InfraMindDashboard() {
  const [activeTab, setActiveTab] = useState<Tab>("analysis")
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const { toast } = useToast()

  const handleSubmit = useCallback(async (input: AnalysisInput) => {
    setIsLoading(true)
    setError(null)
    
    try {
      console.log('🔍 Starting analysis with input:', input)
      
      // Call the real backend API
      const backendResponse = await analyzeIncident(
        input.description,
        input.serviceName,
        input.logs,
        input.metrics,
        input.traces,
        input.configs
      )
      
      console.log('✅ Analysis completed:', backendResponse.incident_id)
      
      // Transform backend response to frontend format
      const analysisResult = transformBackendResponse(backendResponse)
      
      setResult(analysisResult)
      
      toast({
        title: "Analysis Complete!",
        description: `Incident ${analysisResult.incidentId} analyzed successfully.`,
      })
    } catch (err) {
      console.error('❌ Analysis failed:', err)
      
      let errorMessage = 'Failed to analyze incident'
      
      if (err instanceof Error) {
        errorMessage = err.message
      } else if (typeof err === 'string') {
        errorMessage = err
      } else if (err && typeof err === 'object') {
        errorMessage = JSON.stringify(err, null, 2)
      }
      
      setError(errorMessage)
      
      toast({
        title: "Analysis Failed",
        description: errorMessage,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }, [toast])

  const handleNewAnalysis = useCallback(() => {
    setResult(null)
    setError(null)
  }, [])

  return (
    <div className="min-h-screen bg-background">
      <Header activeTab={activeTab} onTabChange={setActiveTab} />

      <main className="mx-auto max-w-5xl px-4 py-8 sm:px-6">
        {activeTab === "analysis" && (
          <>
            {!result ? (
              <>
                {error && (
                  <div className="mb-6 rounded-xl border border-red-200 bg-red-50 p-4">
                    <div className="flex items-start gap-3">
                      <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
                      <div>
                        <h3 className="font-semibold text-red-900">Analysis Error</h3>
                        <p className="text-sm text-red-700 mt-1">{error}</p>
                        <p className="text-xs text-red-600 mt-2">
                          Make sure the backend API is running at http://localhost:8000
                        </p>
                      </div>
                    </div>
                  </div>
                )}
                <AnalysisForm onSubmit={handleSubmit} isLoading={isLoading} />
              </>
            ) : (
              <div className="space-y-6">
                <SuccessBanner incidentId={result.incidentId} />

                <MetricsDashboard
                  confidence={result.confidence}
                  confidenceLabel={result.confidenceLabel}
                  stepsCount={result.stepsCount}
                  factorsCount={result.factorsCount}
                  fixesCount={result.fixesCount}
                />

                <ExecutiveSummary
                  summary={result.executiveSummary}
                  rootCause={result.rootCause}
                  rootCauseConfidence={result.rootCauseConfidence}
                  confidenceLabel={result.confidenceLabel}
                />

                <FactorsSymptoms
                  contributingFactors={result.contributingFactors}
                  symptoms={result.symptoms}
                />

                <CausalChain steps={result.causalChain} />

                <RecommendedFixes fixes={result.fixes} />

                <ReasoningProcess steps={result.reasoningSteps} />

                <ExportActions result={result} onNewAnalysis={handleNewAnalysis} />
              </div>
            )}
          </>
        )}

        {activeTab === "history" && (
          <div className="flex flex-col items-center justify-center rounded-xl border border-border bg-card py-20 shadow-sm">
            <History className="mb-4 h-12 w-12 text-muted-foreground" />
            <h2 className="text-xl font-semibold text-[#1e3a8a]">Incident History</h2>
            <p className="mt-2 text-sm text-muted-foreground">
              Previous analyses will appear here after you run your first analysis.
            </p>
          </div>
        )}

        {activeTab === "settings" && (
          <div className="flex flex-col items-center justify-center rounded-xl border border-border bg-card py-20 shadow-sm">
            <Settings className="mb-4 h-12 w-12 text-muted-foreground" />
            <h2 className="text-xl font-semibold text-[#1e3a8a]">Settings</h2>
            <p className="mt-2 text-sm text-muted-foreground">
              Configure your Gemini API key, notification preferences, and team settings.
            </p>
          </div>
        )}
      </main>

      <footer className="border-t border-border py-6 text-center">
        <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground">
          <ServerCrash className="h-3.5 w-3.5" />
          <span>InfraMind &middot; Powered by Gemini AI &middot; Built for SRE/DevOps teams</span>
        </div>
      </footer>
    </div>
  )
}

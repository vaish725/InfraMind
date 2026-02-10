export interface AnalysisResult {
  incidentId: string
  confidence: number
  confidenceLabel: "HIGH" | "MEDIUM" | "LOW"
  stepsCount: number
  factorsCount: number
  fixesCount: number
  executiveSummary: string
  rootCause: string
  rootCauseConfidence: number
  contributingFactors: string[]
  symptoms: string[]
  causalChain: CausalStep[]
  fixes: Fix[]
  reasoningSteps: ReasoningStep[]
}

export interface CausalStep {
  stepNumber: number
  type: "ROOT_CAUSE" | "SYMPTOM" | "PROPAGATION"
  event: string
  service: string
  confidence: number
  confidenceLabel: "HIGH" | "MEDIUM" | "LOW"
}

export interface Fix {
  priority: "IMMEDIATE" | "SHORT_TERM" | "LONG_TERM"
  category: string
  categoryIcon: string
  title: string
  implementationSteps?: string
  expectedImpact?: string
}

export interface ReasoningStep {
  stepNumber: number
  title: string
  conclusion: string
  evidence: string[]
}

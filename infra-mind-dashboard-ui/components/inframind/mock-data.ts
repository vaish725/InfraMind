import type { AnalysisResult } from "./types"

export const mockAnalysisResult: AnalysisResult = {
  incidentId: "incident-20260206-180810",
  confidence: 90,
  confidenceLabel: "HIGH",
  stepsCount: 2,
  factorsCount: 3,
  fixesCount: 4,
  executiveSummary:
    "The incident occurred within a very short timeframe (same start and end timestamp) and reported no errors. This suggests a potential monitoring or reporting issue rather than a functional failure. The root cause is likely a misconfiguration or a temporary glitch in the monitoring system itself.",
  rootCause:
    "The incident is likely a false positive triggered by a temporary glitch or misconfiguration in the monitoring system, as the reported timeframe is instantaneous and no errors were recorded.",
  rootCauseConfidence: 70,
  contributingFactors: [
    "Potential misconfiguration of monitoring alerting thresholds that may trigger on zero-duration events",
    "Temporary glitch in the monitoring system's data collection or processing pipeline",
    "Lack of validation checks for incident duration before alert escalation",
  ],
  symptoms: [
    "Reported incident with very short duration (start and end timestamps are identical)",
    "Zero errors reported during the incident timeframe",
    "No service degradation observed by end users during the reported window",
  ],
  causalChain: [
    {
      stepNumber: 1,
      type: "ROOT_CAUSE",
      event: "Potential temporary glitch or misconfiguration in the monitoring system caused a false alert to be generated.",
      service: "Monitoring System",
      confidence: 90,
      confidenceLabel: "HIGH",
    },
    {
      stepNumber: 2,
      type: "SYMPTOM",
      event: "Incident reported due to the glitch or misconfiguration, creating a zero-duration incident record with no associated errors.",
      service: "Incident Management",
      confidence: 70,
      confidenceLabel: "MEDIUM",
    },
  ],
  fixes: [
    {
      priority: "IMMEDIATE",
      category: "CONFIGURATION",
      categoryIcon: "\u2699\uFE0F",
      title: "Review and adjust monitoring system alerting thresholds to prevent false positives.",
      implementationSteps:
        "Access the monitoring configuration, identify the threshold settings that triggered the alert, and adjust them based on historical data to filter out zero-duration incidents.",
      expectedImpact:
        "Reduces false positive alerts and improves overall system reliability monitoring.",
    },
    {
      priority: "SHORT_TERM",
      category: "OBSERVABILITY",
      categoryIcon: "\uD83D\uDC41\uFE0F",
      title: "Implement additional data validation in the monitoring pipeline to catch anomalies early.",
      implementationSteps:
        "Add pre-processing validation that checks for zero-duration events, identical timestamps, and zero-error counts before escalating to incident status.",
      expectedImpact:
        "Prevents ghost incidents from reaching on-call teams and reduces alert fatigue.",
    },
    {
      priority: "SHORT_TERM",
      category: "PROCESS",
      categoryIcon: "\uD83D\uDCCB",
      title: "Create automated correlation checks that validate incidents against actual service health metrics.",
      implementationSteps:
        "Build a secondary validation service that cross-references incident alerts with real-time service health dashboards before creating incident tickets.",
      expectedImpact:
        "Ensures only genuine incidents reach the response team, improving MTTR for real issues.",
    },
    {
      priority: "LONG_TERM",
      category: "INFRASTRUCTURE",
      categoryIcon: "\uD83C\uDFD7\uFE0F",
      title: "Consider upgrading monitoring infrastructure to more robust and reliable solutions with built-in anomaly detection.",
      implementationSteps:
        "Evaluate modern observability platforms (e.g., Datadog, Grafana Cloud) that include ML-based anomaly detection and automatic false-positive suppression.",
      expectedImpact:
        "Significantly reduces operational overhead and improves incident detection accuracy long-term.",
    },
  ],
  reasoningSteps: [
    {
      stepNumber: 1,
      title: "Analyzing incident timeframe and error patterns",
      conclusion:
        "The incident duration is extremely short (identical start and end timestamps), suggesting a monitoring issue rather than an actual system failure.",
      evidence: [
        "Start time: 2026-02-06 18:08:10",
        "End time: 2026-02-06 18:08:10",
        "Duration: 0 seconds",
        "Error count: 0",
      ],
    },
    {
      stepNumber: 2,
      title: "Cross-referencing with service health data",
      conclusion:
        "No correlated service degradation was found during the reported incident window, reinforcing the false-positive hypothesis.",
      evidence: [
        "Service uptime: 99.99% during window",
        "Request latency: within normal bounds",
        "No user-reported issues in the same timeframe",
      ],
    },
    {
      stepNumber: 3,
      title: "Evaluating monitoring system configuration",
      conclusion:
        "The monitoring system lacks validation for zero-duration events and has overly sensitive thresholds that can trigger on transient data artifacts.",
      evidence: [
        "Alert threshold: any incident creation event",
        "No minimum duration filter configured",
        "No error-count minimum requirement for escalation",
      ],
    },
  ],
}

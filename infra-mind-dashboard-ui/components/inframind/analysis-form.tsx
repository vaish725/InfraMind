"use client"

import React from "react"

import { useState } from "react"
import { Rocket, FileText, FolderOpen, Loader2, FlaskConical } from "lucide-react"

const SAMPLE_INCIDENT = {
  description: `Production outage detected on payment-api service at 2025-02-06T03:24:00Z. 
Multiple 503 errors observed across all endpoints. Database connection pool exhausted — max connections (100) reached. 
Upstream dependency auth-service responding with p99 latency of 12s (baseline: 200ms). 
Kubernetes pod restarts detected: 14 restarts in the last 30 minutes due to OOMKilled events. 
Memory usage spiked to 3.8GB (limit: 4GB) correlating with a recent deployment of v2.14.0 which introduced an in-memory caching layer without TTL eviction. 
CloudWatch alarms triggered for: CPUUtilization > 90%, UnHealthyHostCount > 3, TargetResponseTime > 10s.`,
  serviceName: "payment-api",
}
import { Button } from "@/components/ui/button"
import { FileUploadZone } from "./file-upload-zone"

export interface AnalysisInput {
  description: string
  serviceName: string
  logs: File[]
  metrics: File[]
  traces: File[]
  configs: File[]
}

interface AnalysisFormProps {
  onSubmit: (input: AnalysisInput) => void
  isLoading: boolean
}

export function AnalysisForm({ onSubmit, isLoading }: AnalysisFormProps) {
  const [description, setDescription] = useState("")
  const [serviceName, setServiceName] = useState("")
  const [logs, setLogs] = useState<File[]>([])
  const [metrics, setMetrics] = useState<File[]>([])
  const [traces, setTraces] = useState<File[]>([])
  const [configs, setConfigs] = useState<File[]>([])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({ description, serviceName, logs, metrics, traces, configs })
  }

  const handleLoadSample = () => {
    setDescription(SAMPLE_INCIDENT.description)
    setServiceName(SAMPLE_INCIDENT.serviceName)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Section Header */}
      <div className="text-center">
        <h2 className="text-2xl font-bold text-[#1e3a8a]">New Analysis</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Upload your infrastructure data for AI-powered RCA
        </p>
        <Button
          type="button"
          variant="outline"
          onClick={handleLoadSample}
          disabled={isLoading}
          className="mt-4 gap-2 border-[#667eea]/30 text-[#667eea] hover:bg-[#667eea]/5 hover:text-[#5a6fd6] bg-transparent"
        >
          <FlaskConical className="h-4 w-4" />
          Load Sample Incident Data
        </Button>
      </div>

      {/* Incident Details Card */}
      <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
        <div className="mb-5 flex items-center gap-2">
          <FileText className="h-5 w-5 text-[#667eea]" />
          <h3 className="text-lg font-semibold text-[#1e3a8a]">Incident Details</h3>
        </div>

        <div className="space-y-4">
          <div>
            <label htmlFor="description" className="mb-1.5 block text-sm font-medium text-[#1e3a8a]">
              Incident Description <span className="text-[#dc2626]">*</span>
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe what went wrong..."
              required
              rows={4}
              className="w-full rounded-lg border border-border bg-[#f8fafc] px-4 py-3 text-sm text-[#374151] placeholder:text-[#9ca3af] focus:border-[#667eea] focus:outline-none focus:ring-2 focus:ring-[#667eea]/20 transition-all resize-none"
            />
          </div>

          <div>
            <label htmlFor="serviceName" className="mb-1.5 block text-sm font-medium text-[#1e3a8a]">
              Service Name
            </label>
            <input
              id="serviceName"
              type="text"
              value={serviceName}
              onChange={(e) => setServiceName(e.target.value)}
              placeholder="e.g., payment-api, auth-service"
              className="w-full rounded-lg border border-border bg-[#f8fafc] px-4 py-3 text-sm text-[#374151] placeholder:text-[#9ca3af] focus:border-[#667eea] focus:outline-none focus:ring-2 focus:ring-[#667eea]/20 transition-all"
            />
          </div>
        </div>
      </div>

      {/* Upload Data Sources Card */}
      <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
        <div className="mb-5 flex items-center gap-2">
          <FolderOpen className="h-5 w-5 text-[#667eea]" />
          <h3 className="text-lg font-semibold text-[#1e3a8a]">Upload Data Sources</h3>
        </div>

        <div className="space-y-5">
          <FileUploadZone
            label="Logs"
            acceptedFormats={[".log", ".txt", ".json"]}
            files={logs}
            onFilesChange={setLogs}
          />
          <FileUploadZone
            label="Metrics"
            optional
            acceptedFormats={[".csv", ".json"]}
            files={metrics}
            onFilesChange={setMetrics}
          />
          <FileUploadZone
            label="Traces"
            optional
            acceptedFormats={[".json", ".txt"]}
            files={traces}
            onFilesChange={setTraces}
          />
          <FileUploadZone
            label="Configuration Files"
            optional
            acceptedFormats={[".yaml", ".json", ".conf"]}
            files={configs}
            onFilesChange={setConfigs}
          />
        </div>
      </div>

      {/* Submit Button */}
      <div className="flex justify-center">
        <Button
          type="submit"
          disabled={!description.trim() || isLoading}
          className="h-12 px-8 text-base font-semibold bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white shadow-lg hover:shadow-xl hover:-translate-y-0.5 active:scale-[0.98] transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-lg"
        >
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-5 w-5 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <Rocket className="mr-2 h-5 w-5" />
              Analyze with Gemini AI
            </>
          )}
        </Button>
      </div>
    </form>
  )
}

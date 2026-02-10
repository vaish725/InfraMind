"use client"

import React from "react"

import { useCallback, useState } from "react"
import { Upload, FileText, X } from "lucide-react"

interface FileUploadZoneProps {
  label: string
  optional?: boolean
  acceptedFormats: string[]
  files: File[]
  onFilesChange: (files: File[]) => void
}

export function FileUploadZone({
  label,
  optional = false,
  acceptedFormats,
  files,
  onFilesChange,
}: FileUploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false)

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setIsDragging(false)
      const droppedFiles = Array.from(e.dataTransfer.files)
      onFilesChange([...files, ...droppedFiles])
    },
    [files, onFilesChange]
  )

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files) {
        const selected = Array.from(e.target.files)
        onFilesChange([...files, ...selected])
      }
    },
    [files, onFilesChange]
  )

  const removeFile = useCallback(
    (index: number) => {
      onFilesChange(files.filter((_, i) => i !== index))
    },
    [files, onFilesChange]
  )

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-[#1e3a8a]">
        {label}
        {optional && <span className="ml-1 text-muted-foreground font-normal">(Optional)</span>}
      </label>

      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`relative flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed p-6 transition-all ${
          isDragging
            ? "border-[#3b82f6] bg-[#eff6ff]"
            : "border-border bg-[#f8fafc] hover:border-[#667eea]/50 hover:bg-[#f1f5f9]"
        }`}
      >
        <input
          type="file"
          multiple
          onChange={handleFileInput}
          className="absolute inset-0 cursor-pointer opacity-0"
          accept={acceptedFormats.join(",")}
        />
        <Upload className={`mb-2 h-5 w-5 ${isDragging ? "text-[#3b82f6]" : "text-muted-foreground"}`} />
        <p className="text-sm text-muted-foreground">
          Drop files or <span className="font-medium text-[#667eea]">click to upload</span>
        </p>
        <div className="mt-2 flex flex-wrap gap-1.5">
          {acceptedFormats.map((format) => (
            <span
              key={format}
              className="rounded-md bg-[#e2e8f0] px-2 py-0.5 text-xs text-[#64748b]"
            >
              {format}
            </span>
          ))}
        </div>
      </div>

      {files.length > 0 && (
        <div className="space-y-1.5">
          {files.map((file, index) => (
            <div
              key={`${file.name}-${index}`}
              className="flex items-center gap-2 rounded-md bg-[#dcfce7] px-3 py-2 text-sm"
            >
              <FileText className="h-4 w-4 text-[#10b981]" />
              <span className="flex-1 truncate text-[#374151]">{file.name}</span>
              <button
                onClick={() => removeFile(index)}
                className="text-[#64748b] hover:text-[#dc2626] transition-colors"
                type="button"
              >
                <X className="h-4 w-4" />
                <span className="sr-only">Remove {file.name}</span>
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

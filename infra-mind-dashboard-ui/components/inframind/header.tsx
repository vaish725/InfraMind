"use client"

import { Brain, Settings } from "lucide-react"
import { Button } from "@/components/ui/button"

type Tab = "analysis" | "history" | "settings"

interface HeaderProps {
  activeTab: Tab
  onTabChange: (tab: Tab) => void
}

export function Header({ activeTab, onTabChange }: HeaderProps) {
  const tabs: { id: Tab; label: string }[] = [
    { id: "analysis", label: "New Analysis" },
    { id: "history", label: "Incident History" },
    { id: "settings", label: "Settings" },
  ]

  return (
    <header className="bg-card border-b border-border">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-[#667eea] to-[#764ba2]">
            <Brain className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-[#1e3a8a]">InfraMind</h1>
            <p className="text-xs text-muted-foreground">Reasoning-first AI debugger for modern infrastructure</p>
          </div>
        </div>
        <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground">
          <Settings className="h-5 w-5" />
          <span className="sr-only">Settings</span>
        </Button>
      </div>
      <div className="mx-auto max-w-5xl px-6">
        <nav className="flex gap-1" role="tablist">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              role="tab"
              aria-selected={activeTab === tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`relative px-4 py-2.5 text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? "text-[#667eea]"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {tab.label}
              {activeTab === tab.id && (
                <span className="absolute inset-x-0 bottom-0 h-0.5 rounded-full bg-gradient-to-r from-[#667eea] to-[#764ba2]" />
              )}
            </button>
          ))}
        </nav>
      </div>
    </header>
  )
}

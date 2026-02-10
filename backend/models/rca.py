"""
Root Cause Analysis (RCA) models.
Defines the structure for analysis output from Gemini.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ConfidenceLevel(str, Enum):
    """Confidence level for conclusions."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class CausalLink(BaseModel):
    """Represents a link in the causal chain."""
    event: str
    timestamp: Optional[datetime] = None
    service: Optional[str] = None
    is_root_cause: bool = False
    is_symptom: bool = False
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM


class Evidence(BaseModel):
    """Evidence supporting a conclusion."""
    source: str  # "log", "metric", "trace", "config"
    description: Optional[str] = ""  # Make optional with default empty string
    reference: Optional[str] = None  # Log line, metric name, etc.
    timestamp: Optional[datetime] = None
    relevance_score: Optional[float] = None  # Add relevance_score field if used by Gemini


class FixSuggestion(BaseModel):
    """Suggested fix for the issue."""
    priority: str  # "immediate", "short-term", "long-term"
    category: str  # "configuration", "code", "infrastructure", "observability"
    description: str
    implementation: Optional[str] = None
    impact: Optional[str] = None


class ReasoningStep(BaseModel):
    """A step in the reasoning process."""
    step_number: int
    description: str
    evidence: List[Evidence] = Field(default_factory=list)
    conclusion: Optional[str] = ""  # Make optional with default empty string


class RootCauseAnalysis(BaseModel):
    """
    Complete Root Cause Analysis output from Gemini.
    """
    incident_id: str
    analysis_timestamp: datetime = Field(default_factory=datetime.now)
    
    # Core Analysis
    summary: str
    root_cause: str
    contributing_factors: List[str] = Field(default_factory=list)
    symptoms: List[str] = Field(default_factory=list)
    
    # Causal Chain
    causal_chain: List[CausalLink] = Field(default_factory=list)
    
    # Evidence
    supporting_evidence: List[Evidence] = Field(default_factory=list)
    
    # Fixes
    fix_suggestions: List[FixSuggestion] = Field(default_factory=list)
    
    # Reasoning Trace
    reasoning_steps: List[ReasoningStep] = Field(default_factory=list)
    
    # Confidence
    overall_confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    
    # Metadata
    services_affected: List[str] = Field(default_factory=list)
    estimated_impact: Optional[str] = None
    time_to_detection: Optional[str] = None
    
    def to_markdown(self) -> str:
        """Convert RCA to markdown format."""
        md_parts = []
        
        md_parts.append(f"# Root Cause Analysis")
        md_parts.append(f"\n**Incident ID:** {self.incident_id}")
        md_parts.append(f"**Analysis Time:** {self.analysis_timestamp}")
        md_parts.append(f"**Confidence:** {self.overall_confidence}\n")
        
        md_parts.append(f"## Summary\n{self.summary}\n")
        
        md_parts.append(f"## Root Cause\n**{self.root_cause}**\n")
        
        if self.contributing_factors:
            md_parts.append("## Contributing Factors")
            for i, factor in enumerate(self.contributing_factors, 1):
                md_parts.append(f"{i}. {factor}")
            md_parts.append("")
        
        if self.causal_chain:
            md_parts.append("## Causal Chain")
            for i, link in enumerate(self.causal_chain, 1):
                icon = "🎯" if link.is_root_cause else "⚠️" if not link.is_symptom else "📊"
                label = " (ROOT CAUSE)" if link.is_root_cause else " (SYMPTOM)" if link.is_symptom else ""
                md_parts.append(f"{i}. {icon} {link.event}{label}")
                if link.service:
                    md_parts.append(f"   - Service: {link.service}")
                if link.timestamp:
                    md_parts.append(f"   - Time: {link.timestamp}")
            md_parts.append("")
        
        if self.symptoms:
            md_parts.append("## Observed Symptoms")
            for symptom in self.symptoms:
                md_parts.append(f"- {symptom}")
            md_parts.append("")
        
        if self.fix_suggestions:
            md_parts.append("## Fix Suggestions")
            
            immediate = [f for f in self.fix_suggestions if f.priority == "immediate"]
            if immediate:
                md_parts.append("### 🚨 Immediate Actions")
                for fix in immediate:
                    md_parts.append(f"**{fix.description}**")
                    if fix.implementation:
                        md_parts.append(f"```\n{fix.implementation}\n```")
                md_parts.append("")
            
            short_term = [f for f in self.fix_suggestions if f.priority == "short-term"]
            if short_term:
                md_parts.append("### ⏱️ Short-term Fixes")
                for fix in short_term:
                    md_parts.append(f"- {fix.description}")
                md_parts.append("")
            
            long_term = [f for f in self.fix_suggestions if f.priority == "long-term"]
            if long_term:
                md_parts.append("### 📈 Long-term Improvements")
                for fix in long_term:
                    md_parts.append(f"- {fix.description}")
                md_parts.append("")
        
        if self.reasoning_steps:
            md_parts.append("## Reasoning Trace")
            for step in self.reasoning_steps:
                md_parts.append(f"### Step {step.step_number}: {step.description}")
                if step.evidence:
                    md_parts.append("**Evidence:**")
                    for ev in step.evidence:
                        md_parts.append(f"- [{ev.source}] {ev.description}")
                md_parts.append(f"**Conclusion:** {step.conclusion}\n")
        
        return "\n".join(md_parts)

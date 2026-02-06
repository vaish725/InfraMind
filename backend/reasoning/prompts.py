"""
Prompt templates for SRE-focused root cause analysis.
"""
from typing import Dict, Any


class PromptTemplates:
    """Collection of prompt templates for Gemini reasoning."""
    
    @staticmethod
    def get_rca_system_prompt() -> str:
        """Get the system prompt for RCA analysis."""
        return """You are an expert Site Reliability Engineer (SRE) with deep expertise in:
- Distributed systems architecture and microservices
- Infrastructure debugging and incident response
- Database performance and connection pooling
- Application performance monitoring (APM)
- Log analysis and trace correlation
- Root cause analysis methodologies

Your role is to analyze infrastructure incidents and provide:
1. Clear root cause identification with confidence levels
2. Step-by-step reasoning showing your analysis process
3. Causal chains explaining how issues propagated
4. Concrete evidence from logs, metrics, traces, and configs
5. Actionable fix suggestions with priority levels

Guidelines:
- Be systematic: analyze timeline, then correlate events
- Look for cascading failures and dependencies
- Consider recent changes (deployments, configs) as potential triggers
- Distinguish between root causes and symptoms
- Provide evidence-based conclusions, not speculation
- Suggest both immediate fixes and long-term preventions
"""

    @staticmethod
    def get_rca_analysis_prompt(context_string: str) -> str:
        """
        Get the main analysis prompt with incident context.
        
        Args:
            context_string: Formatted incident context from UnifiedContext
            
        Returns:
            Complete prompt for Gemini
        """
        return f"""# INCIDENT DATA

{context_string}

# ANALYSIS TASK

Analyze this infrastructure incident and provide a comprehensive Root Cause Analysis (RCA).

## Required Analysis Steps:

1. **Timeline Analysis**
   - Identify when the incident started
   - Track the progression of symptoms
   - Note any changes or deployments before the incident

2. **Symptom Identification**
   - What are the user-facing symptoms?
   - Which services are affected?
   - What errors are occurring?

3. **Pattern Recognition**
   - Are there correlations between metrics spikes and errors?
   - Do trace errors follow a dependency chain?
   - Are there configuration mismatches?

4. **Root Cause Determination**
   - What is the underlying cause (not just symptoms)?
   - What triggered this specific incident?
   - Why did the system fail to handle it?

5. **Impact Assessment**
   - Which services are impacted?
   - What is the severity?
   - Are there cascading effects?

6. **Fix Recommendations**
   - Immediate actions to resolve the incident
   - Short-term fixes to prevent recurrence
   - Long-term improvements for resilience

## Output Format:

Provide your analysis in this JSON structure:

```json
{{
  "summary": "A 2-3 sentence executive summary of the incident and its root cause",
  "root_cause": "Detailed explanation of the root cause (single string)",
  "contributing_factors": ["Factor 1", "Factor 2"],
  "symptoms": ["Symptom 1", "Symptom 2"],
  "reasoning_steps": [
    {{
      "step_number": 1,
      "description": "What you observed or analyzed",
      "evidence": ["Specific log lines, metrics, or config values"],
      "conclusion": "What this tells us"
    }}
  ],
  "causal_chain": [
    {{
      "event": "Description of what happened",
      "timestamp": "When it occurred (if available)",
      "service": "Affected service",
      "is_root_cause": false,
      "is_symptom": false,
      "confidence": "HIGH|MEDIUM|LOW"
    }}
  ],
  "evidence": [
    {{
      "source": "log|metric|trace|config|deployment",
      "description": "Specific evidence with details",
      "reference": "Log line, metric name, trace ID, etc.",
      "timestamp": "When it occurred"
    }}
  ],
  "fix_suggestions": [
    {{
      "priority": "immediate|short-term|long-term",
      "category": "configuration|code|infrastructure|observability",
      "description": "Detailed fix description and steps",
      "implementation": "Specific implementation details",
      "impact": "Expected impact of this fix"
    }}
  ]
}}
```

Think through this systematically. Show your reasoning process clearly.
"""

    @staticmethod
    def get_focused_analysis_prompt(
        context_string: str,
        focus_area: str
    ) -> str:
        """
        Get a prompt focused on a specific analysis area.
        
        Args:
            context_string: Formatted incident context
            focus_area: Area to focus on (e.g., "configuration", "performance")
            
        Returns:
            Focused analysis prompt
        """
        focus_instructions = {
            "configuration": """
Focus specifically on configuration-related issues:
- Recent configuration changes
- Mismatched settings across services
- Resource limits and quotas
- Connection pool sizes and timeouts
""",
            "performance": """
Focus specifically on performance issues:
- Metric anomalies and spikes
- Slow queries or operations
- Resource exhaustion (CPU, memory, connections)
- Latency increases
""",
            "deployment": """
Focus specifically on deployment-related issues:
- Recent deployments and their timing
- Version changes
- Potential bugs introduced
- Rollback candidates
""",
            "dependencies": """
Focus specifically on service dependencies:
- Service call chains from traces
- Cascading failures
- Timeout propagation
- Circuit breaker states
"""
        }
        
        instruction = focus_instructions.get(focus_area, "")
        
        return f"""# INCIDENT DATA

{context_string}

# FOCUSED ANALYSIS

{instruction}

Analyze this incident with specific attention to {focus_area}-related factors.
Provide a focused but comprehensive analysis.

Use the same JSON output format as specified in the general RCA prompt.
"""

    @staticmethod
    def get_validation_prompt(rca: Dict[str, Any], context_string: str) -> str:
        """
        Get a prompt to validate an RCA against the evidence.
        
        Args:
            rca: Generated RCA to validate
            context_string: Original incident context
            
        Returns:
            Validation prompt
        """
        return f"""# RCA TO VALIDATE

{rca}

# ORIGINAL INCIDENT DATA

{context_string}

# VALIDATION TASK

Review this Root Cause Analysis and validate it against the incident data.

Check for:
1. **Evidence Support**: Is each claim backed by actual evidence from the logs/metrics/traces?
2. **Logic**: Does the causal chain make sense? Are there logical leaps?
3. **Completeness**: Are there important signals that were ignored?
4. **Accuracy**: Are the timestamps, service names, and metrics values correct?
5. **Actionability**: Are the fix suggestions practical and specific?

Provide validation results in this format:

```json
{{
  "is_valid": true/false,
  "confidence_score": 0.0-1.0,
  "issues_found": [
    {{
      "severity": "critical|high|medium|low",
      "description": "What's wrong",
      "suggestion": "How to fix"
    }}
  ],
  "missing_analysis": [
    "What should be addressed"
  ],
  "strengths": [
    "What was done well"
  ]
}}
```
"""

    @staticmethod
    def get_summary_prompt(rca: Dict[str, Any]) -> str:
        """
        Get a prompt to generate an executive summary.
        
        Args:
            rca: Complete RCA
            
        Returns:
            Summary generation prompt
        """
        return f"""# DETAILED RCA

{rca}

# TASK

Create a concise executive summary of this RCA suitable for:
- Incident reports
- Post-mortem documents
- Executive updates

The summary should be 3-5 paragraphs covering:
1. What happened (incident overview)
2. Why it happened (root cause)
3. Impact (services affected, duration, severity)
4. Resolution (immediate and long-term fixes)

Use clear, non-technical language where possible, but be specific about technical details when necessary.

Format as plain text, not JSON.
"""

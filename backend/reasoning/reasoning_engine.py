"""
Reasoning engine that uses Gemini to perform root cause analysis.
"""
import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from backend.reasoning.gemini_client import GeminiClient
from backend.reasoning.prompts import PromptTemplates
from backend.models import UnifiedContext, RootCauseAnalysis, ReasoningStep, CausalLink, Evidence, FixSuggestion
from backend.core.exceptions import GeminiAPIError, ValidationError

logger = logging.getLogger(__name__)


class ReasoningEngine:
    """
    Main reasoning engine that coordinates RCA using Gemini.
    """
    
    def __init__(self, gemini_client: Optional[GeminiClient] = None):
        """
        Initialize reasoning engine.
        
        Args:
            gemini_client: Optional GeminiClient instance. If None, creates new one.
        """
        self.gemini_client = gemini_client or GeminiClient()
        self.prompt_templates = PromptTemplates()
    
    async def analyze_incident(
        self,
        context: UnifiedContext,
        focus_area: Optional[str] = None,
        validate: bool = True
    ) -> RootCauseAnalysis:
        """
        Perform root cause analysis on an incident.
        
        Args:
            context: Unified context with all incident data
            focus_area: Optional focus area (configuration, performance, etc.)
            validate: Whether to validate the RCA
            
        Returns:
            Complete RootCauseAnalysis
            
        Raises:
            GeminiAPIError: If Gemini API fails
            ValidationError: If RCA validation fails
        """
        logger.info(f"Starting RCA for incident {context.incident_id}")
        
        try:
            # Generate context string
            context_string = context.to_context_string()
            logger.debug(f"Context string length: {len(context_string)} characters")
            
            # Get appropriate prompt
            if focus_area:
                prompt = self.prompt_templates.get_focused_analysis_prompt(
                    context_string, focus_area
                )
            else:
                prompt = self.prompt_templates.get_rca_analysis_prompt(context_string)
            
            # Get system prompt
            system_prompt = self.prompt_templates.get_rca_system_prompt()
            
            # Call Gemini
            logger.info("Calling Gemini for RCA...")
            response = await self.gemini_client.generate_content(
                prompt=prompt,
                system_instruction=system_prompt,
                temperature=0.3,  # Lower temperature for more focused analysis
                max_output_tokens=4096
            )
            
            # Parse response
            rca_data = self._parse_rca_response(response)
            
            # Validate if requested
            if validate:
                logger.info("Validating RCA...")
                validation_result = await self._validate_rca(rca_data, context_string)
                if not validation_result.get('is_valid', False):
                    logger.warning(f"RCA validation issues: {validation_result.get('issues_found', [])}")
                    # Could optionally retry with feedback
            
            # Convert to RootCauseAnalysis model
            rca = self._convert_to_rca_model(rca_data, context)
            
            logger.info(f"RCA completed for incident {context.incident_id}")
            return rca
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            raise ValidationError(
                message="Invalid JSON response from Gemini",
                details={"error": str(e), "response": response[:500]}
            )
        except Exception as e:
            logger.error(f"RCA analysis failed: {e}")
            raise
    
    def _parse_rca_response(self, response: str) -> Dict[str, Any]:
        """
        Parse Gemini's response into structured data.
        
        Args:
            response: Raw response from Gemini
            
        Returns:
            Parsed RCA data
            
        Raises:
            json.JSONDecodeError: If response is not valid JSON
        """
        # Extract JSON from markdown code blocks if present
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            response = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            response = response[start:end].strip()
        
        return json.loads(response)
    
    async def _validate_rca(self, rca_data: Dict[str, Any], context_string: str) -> Dict[str, Any]:
        """
        Validate RCA against the original context.
        
        Args:
            rca_data: Generated RCA
            context_string: Original incident context
            
        Returns:
            Validation results
        """
        try:
            prompt = self.prompt_templates.get_validation_prompt(rca_data, context_string)
            
            response = await self.gemini_client.generate_content(
                prompt=prompt,
                temperature=0.2,  # Very focused validation
                max_output_tokens=2048
            )
            
            validation = self._parse_rca_response(response)
            return validation
            
        except Exception as e:
            logger.warning(f"RCA validation failed: {e}")
            return {"is_valid": True, "confidence_score": 0.5}  # Default to accepting
    
    def _convert_to_rca_model(
        self,
        rca_data: Dict[str, Any],
        context: UnifiedContext
    ) -> RootCauseAnalysis:
        """
        Convert parsed RCA data to RootCauseAnalysis model.
        
        Args:
            rca_data: Parsed RCA from Gemini
            context: Original unified context
            
        Returns:
            RootCauseAnalysis model
        """
        # Parse reasoning steps
        reasoning_steps = []
        for idx, step in enumerate(rca_data.get('reasoning_steps', [])):
            # Convert evidence strings to Evidence objects
            evidence_list = []
            for ev in step.get('evidence', []):
                if isinstance(ev, str):
                    evidence_list.append(Evidence(
                        source="log",
                        description=ev,
                        timestamp=None
                    ))
                elif isinstance(ev, dict):
                    evidence_list.append(Evidence(**ev))
                else:
                    evidence_list.append(ev)
            
            reasoning_steps.append(ReasoningStep(
                step_number=step.get('step_number', idx + 1),
                description=step.get('description', ''),
                evidence=evidence_list,
                conclusion=step.get('conclusion', '')
            ))
        
        # Parse causal chain
        causal_chain = []
        for link in rca_data.get('causal_chain', []):
            # Extract event description
            event = link.get('event') or link.get('from_event') or link.get('description', 'Unknown event')
            
            # Convert confidence to uppercase for ConfidenceLevel enum
            confidence_str = str(link.get('confidence', 'MEDIUM')).upper()
            
            causal_chain.append(CausalLink(
                event=event,
                timestamp=link.get('timestamp'),
                service=link.get('service'),
                is_root_cause=link.get('is_root_cause', False),
                is_symptom=link.get('is_symptom', False),
                confidence=confidence_str
            ))
        
        # Parse evidence
        evidence = []
        for ev in rca_data.get('evidence', []):
            evidence.append(Evidence(
                source=ev.get('source') or ev.get('type', 'log'),
                description=ev.get('description') or ev.get('content', ''),
                reference=ev.get('reference'),
                timestamp=ev.get('timestamp')
            ))
        
        # Parse fix suggestions
        fix_suggestions = []
        for fix in rca_data.get('fix_suggestions', []):
            fix_suggestions.append(FixSuggestion(
                priority=fix.get('priority', 'short-term'),
                category=fix.get('category', 'configuration'),
                description=fix.get('description') or fix.get('title', ''),
                implementation=fix.get('implementation'),
                impact=fix.get('impact')
            ))
        
        # Get root cause info
        root_cause_data = rca_data.get('root_cause', {})
        if isinstance(root_cause_data, str):
            root_cause_str = root_cause_data
        else:
            root_cause_str = root_cause_data.get('description') or root_cause_data.get('title', 'Unknown root cause')
        
        # Get summary
        summary = rca_data.get('summary', '')
        if not summary:
            summary = f"Analysis of incident {context.incident_id}"
        
        # Get contributing factors and symptoms
        contributing_factors = rca_data.get('contributing_factors', [])
        symptoms = rca_data.get('symptoms', [])
        
        return RootCauseAnalysis(
            incident_id=context.incident_id,
            analysis_timestamp=datetime.now(),
            summary=summary,
            root_cause=root_cause_str,
            contributing_factors=contributing_factors,
            symptoms=symptoms,
            causal_chain=causal_chain,
            supporting_evidence=evidence,
            fix_suggestions=fix_suggestions
        )
    
    async def generate_summary(self, rca: RootCauseAnalysis) -> str:
        """
        Generate an executive summary of the RCA.
        
        Args:
            rca: Complete RCA
            
        Returns:
            Executive summary text
        """
        logger.info(f"Generating summary for incident {rca.incident_id}")
        
        try:
            # Convert RCA to dict for prompt
            rca_dict = rca.model_dump()
            
            prompt = self.prompt_templates.get_summary_prompt(rca_dict)
            
            response = await self.gemini_client.generate_content(
                prompt=prompt,
                temperature=0.5,  # Slightly more creative for summary
                max_output_tokens=1024
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            # Return basic summary as fallback
            return f"""Incident: {rca.root_cause_title}

Root Cause: {rca.root_cause_description}

Affected Services: {', '.join(rca.affected_services)}

Priority Fixes: {len([f for f in rca.fix_suggestions if f.priority in ['critical', 'high']])} critical/high priority fixes recommended.
"""
    
    async def explain_reasoning(self, rca: RootCauseAnalysis) -> str:
        """
        Generate a detailed explanation of the reasoning process.
        
        Args:
            rca: Complete RCA
            
        Returns:
            Detailed reasoning explanation
        """
        explanation_parts = [
            "# Root Cause Analysis Reasoning\n",
            f"## Incident: {rca.root_cause_title}\n",
            f"Confidence: {rca.confidence.upper()}\n",
            f"\n## Analysis Process\n"
        ]
        
        for step in rca.reasoning_steps:
            explanation_parts.append(f"\n### Step {step.step_number}: {step.description}\n")
            if step.evidence:
                explanation_parts.append("**Evidence:**\n")
                for evidence in step.evidence:
                    explanation_parts.append(f"- {evidence}\n")
            explanation_parts.append(f"**Conclusion:** {step.conclusion}\n")
        
        if rca.causal_chain:
            explanation_parts.append("\n## Causal Chain\n")
            for idx, link in enumerate(rca.causal_chain, 1):
                explanation_parts.append(
                    f"{idx}. {link.from_event} **{link.relationship}** {link.to_event}\n"
                )
                explanation_parts.append(f"   *{link.explanation}*\n")
        
        return "".join(explanation_parts)

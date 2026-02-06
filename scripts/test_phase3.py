"""
Test script for Phase 3: Gemini Reasoning Engine
Tests the RCA generation with sample data.
"""
import sys
import asyncio
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.reasoning import ReasoningEngine
from backend.ingestion import DataUnifier
from backend.models import DeploymentEvent
from datetime import datetime
import json


async def test_reasoning_engine():
    """Test the reasoning engine with sample data."""
    print("\n" + "="*70)
    print(" "*15 + "PHASE 3 REASONING ENGINE TEST")
    print("="*70)
    
    # Load sample data using DataUnifier
    print("\n📦 Loading sample data...")
    unifier = DataUnifier()
    samples_dir = Path(__file__).parent.parent / "data" / "samples"
    
    # Load log files
    log_files = []
    for log_file in (samples_dir / "logs").glob("*.log"):
        with open(log_file, 'r') as f:
            log_files.append({
                'content': f.read(),
                'source': log_file.stem
            })
    
    # Load metric files
    metric_files = []
    for metric_file in (samples_dir / "metrics").glob("*.json"):
        with open(metric_file, 'r') as f:
            metric_files.append({'content': f.read()})
    
    # Load trace files
    trace_files = []
    for trace_file in (samples_dir / "traces").glob("*.json"):
        with open(trace_file, 'r') as f:
            trace_files.append(f.read())
    
    # Load configs and find changes
    from backend.ingestion import ConfigParser
    config_parser = ConfigParser()
    
    old_config_path = samples_dir / "configs" / "payment-service-old.yaml"
    new_config_path = samples_dir / "configs" / "payment-service-new.yaml"
    
    with open(old_config_path, 'r') as f:
        old_content = f.read()
    with open(new_config_path, 'r') as f:
        new_content = f.read()
    
    old_configs = config_parser.parse_file(old_content, file_format="yaml", file_path="payment-service.yaml")
    new_configs = config_parser.parse_file(new_content, file_format="yaml", file_path="payment-service.yaml")
    config_changes = config_parser.compare_configs(old_configs, new_configs)
    
    # Load deployments
    deployments = []
    deployment_path = samples_dir / "deployments" / "deployments.json"
    if deployment_path.exists():
        with open(deployment_path, 'r') as f:
            deployment_data = json.load(f)
            for dep in deployment_data:
                deployments.append(DeploymentEvent(
                    timestamp=datetime.fromisoformat(dep['timestamp'].replace('Z', '+00:00')),
                    service=dep['service'],
                    version=dep['version'],
                    previous_version=dep.get('previous_version'),
                    environment=dep['environment'],
                    deployment_type=dep['deployment_type'],
                    status=dep['status']
                ))
    
    # Parse all data
    print("📊 Parsing data...")
    all_logs = []
    for log_file in log_files:
        logs = unifier.log_parser.parse_file(log_file['content'], log_file['source'])
        all_logs.extend(logs)
    
    all_metrics = []
    for metric_file in metric_files:
        metrics = unifier.metrics_parser.parse_file(metric_file['content'])
        summaries = unifier.metrics_parser.create_summaries(metrics)
        all_metrics.extend(summaries)
    
    all_traces = []
    for trace_file in trace_files:
        traces = unifier.trace_parser.parse_file(trace_file)
        all_traces.extend(traces)
    
    # Create unified context
    context = unifier.create_unified_context(
        logs=all_logs,
        metrics=all_metrics,
        traces=all_traces,
        configs=config_changes,
        deployments=deployments,
        time_window_minutes=None
    )
    
    print(f"✅ Context created: {len(context.logs)} logs, {len(context.metrics)} metrics, {len(context.traces)} traces")
    print(f"   Incident ID: {context.incident_id}")
    print(f"   Services: {', '.join(context.services_involved)}")
    print(f"   Error count: {context.error_count}")
    
    # Initialize reasoning engine
    print("\n🤖 Initializing Gemini Reasoning Engine...")
    engine = ReasoningEngine()
    
    # Perform RCA
    print("\n🔍 Analyzing incident with Gemini...")
    print("   This may take 10-30 seconds...\n")
    
    try:
        rca = await engine.analyze_incident(
            context=context,
            validate=True
        )
        
        print("\n" + "="*70)
        print("✅ ROOT CAUSE ANALYSIS COMPLETE")
        print("="*70)
        
        print(f"\n📋 Root Cause: {rca.root_cause_title}")
        print(f"   Confidence: {rca.confidence.upper()}")
        print(f"   Category: {rca.category}")
        
        print(f"\n📝 Description:")
        print(f"   {rca.root_cause_description}")
        
        print(f"\n🔗 Reasoning Steps: {len(rca.reasoning_steps)}")
        for step in rca.reasoning_steps[:3]:  # Show first 3
            print(f"   {step.step_number}. {step.description[:100]}...")
        if len(rca.reasoning_steps) > 3:
            print(f"   ... and {len(rca.reasoning_steps) - 3} more steps")
        
        print(f"\n⛓️  Causal Chain: {len(rca.causal_chain)} links")
        for link in rca.causal_chain[:3]:  # Show first 3
            print(f"   • {link.from_event} → {link.to_event}")
            print(f"     ({link.relationship})")
        if len(rca.causal_chain) > 3:
            print(f"   ... and {len(rca.causal_chain) - 3} more links")
        
        print(f"\n🎯 Affected Services: {', '.join(rca.affected_services)}")
        
        print(f"\n💡 Fix Suggestions: {len(rca.fix_suggestions)}")
        for fix in rca.fix_suggestions:
            print(f"   [{fix.priority.upper()}] {fix.title}")
            print(f"   └─ {fix.description[:100]}...")
        
        print(f"\n🛡️  Prevention Measures: {len(rca.prevention_measures)}")
        for measure in rca.prevention_measures[:3]:
            print(f"   • {measure}")
        
        # Generate summary
        print("\n📄 Generating executive summary...")
        summary = await engine.generate_summary(rca)
        print("\n" + "="*70)
        print("EXECUTIVE SUMMARY")
        print("="*70)
        print(summary)
        
        # Export to markdown
        print("\n💾 Exporting RCA to markdown...")
        markdown = rca.to_markdown()
        output_path = Path(__file__).parent.parent / "rca_report.md"
        with open(output_path, 'w') as f:
            f.write(markdown)
        print(f"✅ Saved to: {output_path}")
        
        # Export to JSON
        json_path = Path(__file__).parent.parent / "rca_report.json"
        with open(json_path, 'w') as f:
            json.dump(rca.model_dump(), f, indent=2, default=str)
        print(f"✅ Saved to: {json_path}")
        
        print("\n" + "="*70)
        print("✅ PHASE 3 TEST COMPLETE!")
        print("="*70)
        print("\nThe reasoning engine successfully:")
        print("  ✅ Loaded and parsed all sample data")
        print("  ✅ Created unified context")
        print("  ✅ Called Gemini for RCA")
        print("  ✅ Generated structured root cause analysis")
        print("  ✅ Created executive summary")
        print("  ✅ Exported reports (markdown + JSON)")
        print("\nReady for Phase 4: FastAPI Backend!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_reasoning_engine())

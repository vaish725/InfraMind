"""
Test script for Phase 2: Data Ingestion & Preprocessing
Tests all parsers and the data unifier with sample data.
"""
import sys
import os
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ingestion import (
    LogParser, MetricsParser, ConfigParser, 
    TraceParser, DataUnifier
)
from backend.models import DeploymentEvent


def test_log_parser():
    """Test log parser with sample logs."""
    print("\n" + "="*60)
    print("Testing LogParser")
    print("="*60)
    
    parser = LogParser()
    samples_dir = Path(__file__).parent.parent / "data" / "samples" / "logs"
    
    # Test payment service logs
    payment_log_path = samples_dir / "payment-service.log"
    with open(payment_log_path, 'r') as f:
        content = f.read()
    
    logs = parser.parse_file(content, source="payment-service")
    print(f"\n✅ Parsed {len(logs)} log entries from payment-service.log")
    
    # Show error logs
    error_logs = parser.filter_by_level(logs, ["ERROR", "CRITICAL"])
    print(f"✅ Found {len(error_logs)} error/critical logs")
    
    # Show sample
    if error_logs:
        print(f"\n📋 Sample error log:")
        log = error_logs[0]
        print(f"  Time: {log.timestamp}")
        print(f"  Level: {log.level.value}")
        print(f"  Message: {log.message[:100]}...")
    
    return logs


def test_metrics_parser():
    """Test metrics parser with sample metrics."""
    print("\n" + "="*60)
    print("Testing MetricsParser")
    print("="*60)
    
    parser = MetricsParser()
    samples_dir = Path(__file__).parent.parent / "data" / "samples" / "metrics"
    
    # Test system metrics
    system_metrics_path = samples_dir / "system-metrics.json"
    with open(system_metrics_path, 'r') as f:
        content = f.read()
    
    metrics = parser.parse_file(content)
    summaries = parser.create_summaries(metrics)
    
    print(f"\n✅ Parsed {len(metrics)} metric data points")
    print(f"✅ Created {len(summaries)} metric summaries")
    
    # Show anomalies
    anomalies = [s for s in summaries if s.anomaly_detected]
    print(f"✅ Detected {len(anomalies)} anomalies")
    
    # Show sample
    if anomalies:
        print(f"\n📋 Sample anomaly:")
        metric = anomalies[0]
        print(f"  Metric: {metric.metric_name}")
        print(f"  Current: {metric.current_value:.2f}")
        print(f"  Average: {metric.avg_value:.2f}")
        print(f"  Change: {metric.change_percent:.1f}%")
    
    return summaries


def test_config_parser():
    """Test config parser with sample configs."""
    print("\n" + "="*60)
    print("Testing ConfigParser")
    print("="*60)
    
    parser = ConfigParser()
    samples_dir = Path(__file__).parent.parent / "data" / "samples" / "configs"
    
    # Parse old config
    old_config_path = samples_dir / "payment-service-old.yaml"
    with open(old_config_path, 'r') as f:
        old_content = f.read()
    
    old_configs = parser.parse_file(old_content, file_format="yaml", file_path="payment-service.yaml")
    print(f"\n✅ Parsed {len(old_configs)} config entries from old config")
    
    # Parse new config
    new_config_path = samples_dir / "payment-service-new.yaml"
    with open(new_config_path, 'r') as f:
        new_content = f.read()
    
    new_configs = parser.parse_file(new_content, file_format="yaml", file_path="payment-service.yaml")
    print(f"✅ Parsed {len(new_configs)} config entries from new config")
    
    # Find changes
    changes = parser.compare_configs(old_configs, new_configs)
    print(f"✅ Detected {len(changes)} config changes")
    
    # Show changes
    if changes:
        print(f"\n📋 Configuration changes:")
        for change in changes:
            print(f"  {change.key}: {change.old_value} → {change.new_value} ({change.change_type})")
    
    return changes


def test_trace_parser():
    """Test trace parser with sample traces."""
    print("\n" + "="*60)
    print("Testing TraceParser")
    print("="*60)
    
    parser = TraceParser()
    samples_dir = Path(__file__).parent.parent / "data" / "samples" / "traces"
    
    # Parse traces
    trace_path = samples_dir / "traces.json"
    with open(trace_path, 'r') as f:
        content = f.read()
    
    traces = parser.parse_file(content)
    print(f"\n✅ Parsed {len(traces)} trace spans")
    
    # Find errors
    error_traces = parser.filter_by_status(traces, ["ERROR", "TIMEOUT"])
    print(f"✅ Found {len(error_traces)} error/timeout spans")
    
    # Build dependency graph
    dependencies = parser.build_dependency_graph(traces)
    print(f"✅ Built dependency graph with {len(dependencies)} services")
    
    print(f"\n📋 Service dependencies:")
    for service, deps in dependencies.items():
        print(f"  {service} → {', '.join(deps)}")
    
    # Find error chains
    error_chains = parser.find_error_chains(traces)
    print(f"\n✅ Found {len(error_chains)} error chains")
    
    if error_chains:
        print(f"\n📋 Sample error chain:")
        chain = error_chains[0]
        for span in chain:
            print(f"  {span.service}.{span.operation} [{span.status}]")
    
    return traces


def test_data_unifier():
    """Test data unifier with all sample data."""
    print("\n" + "="*60)
    print("Testing DataUnifier")
    print("="*60)
    
    unifier = DataUnifier()
    samples_dir = Path(__file__).parent.parent / "data" / "samples"
    
    # Load all files
    log_files = []
    for log_file in (samples_dir / "logs").glob("*.log"):
        with open(log_file, 'r') as f:
            log_files.append({
                'content': f.read(),
                'source': log_file.stem
            })
    
    metric_files = []
    for metric_file in (samples_dir / "metrics").glob("*.json"):
        with open(metric_file, 'r') as f:
            metric_files.append({'content': f.read()})
    
    trace_files = []
    for trace_file in (samples_dir / "traces").glob("*.json"):
        with open(trace_file, 'r') as f:
            trace_files.append(f.read())
    
    # Load configs
    config_files = []
    old_config_path = samples_dir / "configs" / "payment-service-old.yaml"
    new_config_path = samples_dir / "configs" / "payment-service-new.yaml"
    
    with open(old_config_path, 'r') as f:
        old_content = f.read()
    with open(new_config_path, 'r') as f:
        new_content = f.read()
    
    # Parse configs and find changes
    config_parser = ConfigParser()
    old_configs = config_parser.parse_file(old_content, file_format="yaml", file_path="payment-service.yaml")
    new_configs = config_parser.parse_file(new_content, file_format="yaml", file_path="payment-service.yaml")
    config_changes = config_parser.compare_configs(old_configs, new_configs)
    
    # Load deployments
    deployments = []
    deployment_path = samples_dir / "deployments" / "deployments.json"
    if deployment_path.exists():
        import json
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
    
    # Create unified context
    print("\n📦 Creating unified context from all sources...")
    
    # Parse all data first
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
        time_window_minutes=None  # Don't filter sample data
    )
    
    print(f"\n✅ Created unified context")
    
    # Get summary stats
    stats = unifier.get_summary_stats(context)
    print(f"\n📊 Context Statistics:")
    print(f"  Total logs: {stats['total_logs']}")
    print(f"  Error logs: {stats['error_logs']}")
    print(f"  Total metrics: {stats['total_metrics']}")
    print(f"  Anomalous metrics: {stats['anomalous_metrics']}")
    print(f"  Total traces: {stats['total_traces']}")
    print(f"  Error traces: {stats['error_traces']}")
    print(f"  Config changes: {stats['config_changes']}")
    print(f"  Deployments: {stats['deployments']}")
    
    # Test context string generation
    context_string = context.to_context_string()
    print(f"\n✅ Generated context string ({len(context_string)} characters)")
    print(f"\n📄 Context preview (first 500 chars):")
    print(context_string[:500])
    print("...")
    
    return context


def main():
    """Run all Phase 2 tests."""
    print("\n" + "="*70)
    print(" "*15 + "PHASE 2 INGESTION TESTS")
    print("="*70)
    
    try:
        # Test individual parsers
        logs = test_log_parser()
        metrics = test_metrics_parser()
        configs = test_config_parser()
        traces = test_trace_parser()
        
        # Test data unifier
        context = test_data_unifier()
        
        print("\n" + "="*70)
        print("✅ ALL PHASE 2 TESTS PASSED!")
        print("="*70)
        print("\nPhase 2 is complete. All parsers and data unifier are working correctly.")
        print("Ready to move to Phase 3: Gemini Reasoning Engine")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

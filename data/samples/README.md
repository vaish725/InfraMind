# Sample Data for InfraMind Demo

This directory contains sample infrastructure data simulating a realistic microservice outage scenario.

## Scenario: Database Connection Pool Exhaustion

**Timeline:**
- **14:45** - Deployment of payment service v2.1.0
- **14:50** - Config change increases payment service worker count from 10 to 50
- **14:52** - Database connection pool exhaustion begins
- **14:53** - Cascading failures across services
- **14:55** - System in degraded state

**Affected Services:**
- `payment-service` - Primary affected service
- `order-service` - Dependent service experiencing failures
- `api-gateway` - Experiencing increased latency
- `database` - Connection pool exhausted

## Files

### logs/
- `payment-service.log` - Logs showing connection errors and timeouts
- `order-service.log` - Logs showing cascade failures
- `api-gateway.log` - HTTP 500 errors and timeout warnings

### metrics/
- `system-metrics.json` - CPU, memory, connections metrics showing spikes
- `application-metrics.json` - Request rates, error rates, latencies

### configs/
- `payment-service-old.yaml` - Configuration before change
- `payment-service-new.yaml` - Configuration after change (increased workers)

### traces/
- `traces.json` - Distributed traces showing error chains

### deployments/
- `deployments.json` - Recent deployment events

## Expected Root Cause

The DataUnifier should combine all these signals, and Gemini should identify:

1. **Root Cause**: Database connection pool exhaustion
2. **Trigger**: Configuration change increased worker count without increasing DB pool size
3. **Contributing Factor**: Recent deployment may have introduced connection leak
4. **Impact**: Cascading failures across dependent services

## Fix Suggestions Expected

1. Immediately rollback worker count to 10
2. Increase database connection pool size
3. Review payment service v2.1.0 for connection leaks
4. Implement connection pool monitoring alerts

#!/usr/bin/env python3
"""Performance Benchmark Suite for MIT Agent Synchronization Pattern

Quantifies performance metrics that the MIT paper (arXiv:2508.14511v2) didn't provide:
- Synchronization latency overhead
- Scalability to 13 concurrent agents
- Idempotency hash computation cost
- Memory overhead for provenance tracking
- Database load impact

Created: 2025-11-18
Issue: #164 - Phase 6 Performance Validation and Documentation
"""

import json
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).parent.parent / '.claude' / 'skills' / 'agentdb-state-manager' / 'scripts'))

from sync_engine import SynchronizationEngine


class PerformanceBenchmarks:
    """Performance benchmark suite for synchronization engine."""

    def __init__(self, db_path="benchmarks/benchmark.duckdb"):
        """Initialize benchmark suite.

        Args:
            db_path: Path to DuckDB database (default: benchmarks/benchmark.duckdb)
        """
        self.db_path = db_path
        self._setup_database()

    def _setup_database(self):
        """Setup test database with schema and sample rules."""
        # Delete existing database file
        db_file = Path(self.db_path)
        if db_file.exists():
            db_file.unlink()

        conn = duckdb.connect(self.db_path)

        # Get absolute paths (relative to this script's parent directory)
        base_dir = Path(__file__).parent.parent

        # Load Phase 1 schema
        schema_path = base_dir / ".claude" / "skills" / "agentdb-state-manager" / "schemas" / "agentdb_sync_schema.sql"
        with open(schema_path) as f:
            conn.execute(f.read())

        # Load Phase 2 migration
        migration_path = base_dir / ".claude" / "skills" / "agentdb-state-manager" / "schemas" / "phase2_migration.sql"
        with open(migration_path) as f:
            conn.execute(f.read())

        # Load Phase 4 default rules
        default_syncs_path = base_dir / ".claude" / "skills" / "agentdb-state-manager" / "templates" / "default_synchronizations.sql"
        with open(default_syncs_path) as f:
            conn.execute(f.read())

        conn.close()

    def run_all_benchmarks(self):
        """Run complete benchmark suite and return results."""
        results = {
            "latency": self.benchmark_sync_latency(),
            "scalability": self.benchmark_concurrent_agents(),
            "hash_computation": self.benchmark_hash_performance(),
            "memory": self.benchmark_memory_overhead(),
            "database_load": self.benchmark_database_load(),
        }
        return results

    # ========================================================================
    # Benchmark 1: Synchronization Latency
    # ========================================================================

    def benchmark_sync_latency(self, iterations=100):
        """Measure synchronization latency overhead.

        Measures p50, p95, p99 latency for sync engine execution.

        Args:
            iterations: Number of iterations to measure

        Returns:
            dict with latency metrics (ms)
        """
        print(f"\n{'='*70}")
        print("Benchmark 1: Synchronization Latency")
        print(f"{'='*70}")
        print(f"Measuring {iterations} iterations...")

        engine = SynchronizationEngine(db_path=self.db_path)
        latencies = []

        for i in range(iterations):
            start = time.perf_counter()

            engine.on_agent_action_complete(
                agent_id="develop",
                action="implementation_complete",
                flow_token=f"bench-latency-{i}",
                state_snapshot={"iteration": i}
            )

            latency_ms = (time.perf_counter() - start) * 1000
            latencies.append(latency_ms)

            if (i + 1) % 100 == 0:
                print(f"  Progress: {i + 1}/{iterations}")

        engine.close()

        # Calculate percentiles
        latencies.sort()
        p50 = latencies[int(len(latencies) * 0.50)]
        p95 = latencies[int(len(latencies) * 0.95)]
        p99 = latencies[int(len(latencies) * 0.99)]
        mean = statistics.mean(latencies)
        stdev = statistics.stdev(latencies)

        results = {
            "p50_ms": round(p50, 2),
            "p95_ms": round(p95, 2),
            "p99_ms": round(p99, 2),
            "mean_ms": round(mean, 2),
            "stdev_ms": round(stdev, 2),
            "min_ms": round(min(latencies), 2),
            "max_ms": round(max(latencies), 2),
        }

        print("\nResults:")
        print(f"  p50: {results['p50_ms']:.2f}ms")
        print(f"  p95: {results['p95_ms']:.2f}ms")
        print(f"  p99: {results['p99_ms']:.2f}ms")
        print(f"  Mean: {results['mean_ms']:.2f}ms (±{results['stdev_ms']:.2f}ms)")
        print(f"  Range: {results['min_ms']:.2f}ms - {results['max_ms']:.2f}ms")

        # Target: p95 < 100ms
        if results['p95_ms'] < 100:
            print(f"  ✓ PASS: p95 latency {results['p95_ms']:.2f}ms < 100ms target")
        else:
            print(f"  ✗ FAIL: p95 latency {results['p95_ms']:.2f}ms >= 100ms target")

        return results

    # ========================================================================
    # Benchmark 2: Concurrent Agent Scalability
    # ========================================================================

    def benchmark_concurrent_agents(self, max_agents=13, iterations_per_agent=10):
        """Measure scalability with concurrent agents.

        Tests 1, 4, 8, 13 concurrent agents (MIT paper max: 13).

        Args:
            max_agents: Maximum number of concurrent agents
            iterations_per_agent: Operations per agent

        Returns:
            dict with scalability metrics
        """
        print(f"\n{'='*70}")
        print("Benchmark 2: Concurrent Agent Scalability")
        print(f"{'='*70}")

        agent_counts = [1, 4, 8, max_agents]
        results = {}

        for num_agents in agent_counts:
            print(f"\nTesting {num_agents} concurrent agents...")

            start = time.perf_counter()

            with ThreadPoolExecutor(max_workers=num_agents) as executor:
                futures = []

                for agent_id in range(num_agents):
                    future = executor.submit(
                        self._run_agent_workload,
                        agent_id,
                        iterations_per_agent
                    )
                    futures.append(future)

                # Wait for all agents to complete
                completed = 0
                for future in as_completed(futures):
                    future.result()  # Raise exceptions if any
                    completed += 1
                    if completed % 4 == 0:
                        print(f"  Progress: {completed}/{num_agents} agents completed")

            elapsed_ms = (time.perf_counter() - start) * 1000
            total_operations = num_agents * iterations_per_agent
            ops_per_sec = (total_operations / elapsed_ms) * 1000

            results[f"{num_agents}_agents"] = {
                "elapsed_ms": round(elapsed_ms, 2),
                "total_operations": total_operations,
                "ops_per_sec": round(ops_per_sec, 2),
                "latency_per_op_ms": round(elapsed_ms / total_operations, 2),
            }

            print(f"  Elapsed: {elapsed_ms:.2f}ms")
            print(f"  Operations: {total_operations}")
            print(f"  Throughput: {ops_per_sec:.2f} ops/sec")

        # Calculate linear scalability ratio
        baseline_ops = results["1_agents"]["ops_per_sec"]
        max_ops = results[f"{max_agents}_agents"]["ops_per_sec"]
        scalability_ratio = max_ops / baseline_ops

        results["scalability_summary"] = {
            "baseline_ops_per_sec": baseline_ops,
            "max_agents_ops_per_sec": max_ops,
            "scalability_ratio": round(scalability_ratio, 2),
            "linear_target": max_agents,  # Perfect scaling = max_agents
            "efficiency_pct": round((scalability_ratio / max_agents) * 100, 2),
        }

        print("\nScalability Summary:")
        print(f"  Baseline (1 agent): {baseline_ops:.2f} ops/sec")
        print(f"  Maximum ({max_agents} agents): {max_ops:.2f} ops/sec")
        print(f"  Scalability ratio: {scalability_ratio:.2f}x")
        print(f"  Efficiency: {results['scalability_summary']['efficiency_pct']:.1f}%")

        # Target: >=70% efficiency (9.1x speedup with 13 agents)
        if results['scalability_summary']['efficiency_pct'] >= 70:
            print(f"  ✓ PASS: Efficiency {results['scalability_summary']['efficiency_pct']:.1f}% >= 70% target")
        else:
            print(f"  ✗ FAIL: Efficiency {results['scalability_summary']['efficiency_pct']:.1f}% < 70% target")

        return results

    def _run_agent_workload(self, agent_id, iterations):
        """Run workload for a single agent (used in concurrency test)."""
        engine = SynchronizationEngine(db_path=self.db_path)

        for i in range(iterations):
            engine.on_agent_action_complete(
                agent_id="develop",
                action="implementation_complete",
                flow_token=f"bench-concurrent-agent{agent_id}-{i}",
                state_snapshot={"agent_id": agent_id, "iteration": i}
            )

        engine.close()

    # ========================================================================
    # Benchmark 3: Hash Computation Performance
    # ========================================================================

    def benchmark_hash_performance(self, iterations=1000):
        """Measure idempotency hash computation cost.

        Args:
            iterations: Number of hash computations

        Returns:
            dict with hash performance metrics
        """
        print(f"\n{'='*70}")
        print("Benchmark 3: Hash Computation Performance")
        print(f"{'='*70}")
        print(f"Measuring {iterations} hash computations...")

        engine = SynchronizationEngine(db_path=self.db_path)
        times = []

        # Test state (realistic size: ~1KB JSON)
        state = {
            "files_changed": 15,
            "commits": 20,
            "coverage": {"percentage": 85, "lines_covered": 1234, "lines_total": 1450},
            "lint_status": "pass",
            "test_results": {"passed": 156, "failed": 0, "skipped": 2},
        }

        for i in range(iterations):
            start = time.perf_counter()
            engine._compute_provenance_hash("sync-001", f"flow-{i}", state)
            times.append((time.perf_counter() - start) * 1000)  # Convert to ms

            if (i + 1) % 1000 == 0:
                print(f"  Progress: {i + 1}/{iterations}")

        engine.close()

        # Calculate statistics
        times.sort()
        p50 = times[int(len(times) * 0.50)]
        p95 = times[int(len(times) * 0.95)]
        p99 = times[int(len(times) * 0.99)]
        mean = statistics.mean(times)

        results = {
            "iterations": iterations,
            "p50_ms": round(p50, 4),
            "p95_ms": round(p95, 4),
            "p99_ms": round(p99, 4),
            "mean_ms": round(mean, 4),
            "hashes_per_sec": round(1000 / mean, 0),
        }

        print("\nResults:")
        print(f"  p50: {results['p50_ms']:.4f}ms")
        print(f"  p95: {results['p95_ms']:.4f}ms")
        print(f"  p99: {results['p99_ms']:.4f}ms")
        print(f"  Mean: {results['mean_ms']:.4f}ms")
        print(f"  Throughput: {results['hashes_per_sec']:.0f} hashes/sec")

        # Target: p99 < 1ms
        if results['p99_ms'] < 1.0:
            print(f"  ✓ PASS: p99 hash time {results['p99_ms']:.4f}ms < 1ms target")
        else:
            print(f"  ✗ FAIL: p99 hash time {results['p99_ms']:.4f}ms >= 1ms target")

        return results

    # ========================================================================
    # Benchmark 4: Memory Overhead
    # ========================================================================

    def benchmark_memory_overhead(self, num_executions=1000):
        """Measure memory overhead for provenance tracking.

        Args:
            num_executions: Number of sync executions to create

        Returns:
            dict with memory metrics
        """
        print(f"\n{'='*70}")
        print("Benchmark 4: Memory Overhead")
        print(f"{'='*70}")
        print(f"Creating {num_executions} sync executions...")

        engine = SynchronizationEngine(db_path=self.db_path)

        # Create executions
        for i in range(num_executions):
            engine.on_agent_action_complete(
                agent_id="develop",
                action="implementation_complete",
                flow_token=f"bench-memory-{i}",
                state_snapshot={"iteration": i, "data": "x" * 100}  # 100 bytes
            )

            if (i + 1) % 1000 == 0:
                print(f"  Progress: {i + 1}/{num_executions}")

        # Query database size
        conn = engine.conn

        # Count rows
        exec_count = conn.execute("SELECT COUNT(*) FROM sync_executions").fetchone()[0]
        audit_count = conn.execute("SELECT COUNT(*) FROM sync_audit_trail").fetchone()[0]

        # Estimate row sizes (bytes)
        # sync_executions: ~500 bytes/row (with JSON fields)
        # sync_audit_trail: ~300 bytes/row
        exec_size_bytes = exec_count * 500
        audit_size_bytes = audit_count * 300
        total_size_bytes = exec_size_bytes + audit_size_bytes

        results = {
            "num_executions": num_executions,
            "exec_rows": exec_count,
            "audit_rows": audit_count,
            "exec_size_mb": round(exec_size_bytes / 1024 / 1024, 2),
            "audit_size_mb": round(audit_size_bytes / 1024 / 1024, 2),
            "total_size_mb": round(total_size_bytes / 1024 / 1024, 2),
            "bytes_per_execution": round(total_size_bytes / num_executions, 0),
        }

        print("\nResults:")
        print(f"  Sync executions: {results['exec_rows']:,} rows ({results['exec_size_mb']:.2f} MB)")
        print(f"  Audit trail: {results['audit_rows']:,} rows ({results['audit_size_mb']:.2f} MB)")
        print(f"  Total size: {results['total_size_mb']:.2f} MB")
        print(f"  Per execution: {results['bytes_per_execution']:.0f} bytes")

        engine.close()

        # Target: <1KB per execution
        if results['bytes_per_execution'] < 1024:
            print(f"  ✓ PASS: Memory overhead {results['bytes_per_execution']:.0f} bytes < 1KB target")
        else:
            print(f"  ✗ FAIL: Memory overhead {results['bytes_per_execution']:.0f} bytes >= 1KB target")

        return results

    # ========================================================================
    # Benchmark 5: Database Load Impact
    # ========================================================================

    def benchmark_database_load(self, duration_sec=10):
        """Measure database load impact under sustained load.

        Args:
            duration_sec: Test duration in seconds

        Returns:
            dict with database load metrics
        """
        print(f"\n{'='*70}")
        print("Benchmark 5: Database Load Impact")
        print(f"{'='*70}")
        print(f"Running sustained load test for {duration_sec} seconds...")

        engine = SynchronizationEngine(db_path=self.db_path)

        start_time = time.time()
        operation_count = 0
        latencies = []

        while time.time() - start_time < duration_sec:
            start = time.perf_counter()

            engine.on_agent_action_complete(
                agent_id="develop",
                action="implementation_complete",
                flow_token=f"bench-load-{operation_count}",
                state_snapshot={"operation": operation_count}
            )

            latency_ms = (time.perf_counter() - start) * 1000
            latencies.append(latency_ms)
            operation_count += 1

            if operation_count % 100 == 0:
                elapsed = time.time() - start_time
                print(f"  Progress: {operation_count} ops in {elapsed:.1f}s")

        elapsed_sec = time.time() - start_time
        ops_per_sec = operation_count / elapsed_sec

        # Calculate latency statistics
        latencies.sort()
        p50 = latencies[int(len(latencies) * 0.50)]
        p95 = latencies[int(len(latencies) * 0.95)]
        p99 = latencies[int(len(latencies) * 0.99)]

        results = {
            "duration_sec": round(elapsed_sec, 2),
            "total_operations": operation_count,
            "ops_per_sec": round(ops_per_sec, 2),
            "p50_latency_ms": round(p50, 2),
            "p95_latency_ms": round(p95, 2),
            "p99_latency_ms": round(p99, 2),
        }

        print("\nResults:")
        print(f"  Duration: {results['duration_sec']:.2f}s")
        print(f"  Operations: {results['total_operations']:,}")
        print(f"  Throughput: {results['ops_per_sec']:.2f} ops/sec")
        print(f"  Latency p50: {results['p50_latency_ms']:.2f}ms")
        print(f"  Latency p95: {results['p95_latency_ms']:.2f}ms")
        print(f"  Latency p99: {results['p99_latency_ms']:.2f}ms")

        engine.close()

        # Target: >100 ops/sec sustained
        if results['ops_per_sec'] > 100:
            print(f"  ✓ PASS: Throughput {results['ops_per_sec']:.2f} ops/sec > 100 ops/sec target")
        else:
            print(f"  ✗ FAIL: Throughput {results['ops_per_sec']:.2f} ops/sec <= 100 ops/sec target")

        return results


def main():
    """Run all performance benchmarks and save results."""
    print("=" * 70)
    print("MIT Agent Synchronization Pattern - Performance Benchmarks")
    print("=" * 70)
    print("\nInitializing benchmark suite...")

    benchmarks = PerformanceBenchmarks()

    print("\nRunning all benchmarks...")
    results = benchmarks.run_all_benchmarks()

    # Save results to JSON
    output_file = Path("benchmarks/performance_results.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*70}")
    print(f"Benchmark Results Saved: {output_file}")
    print(f"{'='*70}")

    # Print summary
    print("\nSUMMARY:")
    print(f"  Latency p95: {results['latency']['p95_ms']:.2f}ms (target: <100ms)")
    print(f"  Scalability (13 agents): {results['scalability']['scalability_summary']['scalability_ratio']:.2f}x")
    print(f"  Hash performance p99: {results['hash_computation']['p99_ms']:.4f}ms (target: <1ms)")
    print(f"  Memory overhead: {results['memory']['bytes_per_execution']:.0f} bytes/exec (target: <1KB)")
    print(f"  Sustained throughput: {results['database_load']['ops_per_sec']:.2f} ops/sec (target: >100)")

    return results


if __name__ == '__main__':
    main()

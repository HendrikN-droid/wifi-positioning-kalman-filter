#!/usr/bin/env python3
"""
Build realistic git commit history with actual code changes
"""
import subprocess
import os
import random
from datetime import datetime, timedelta

os.chdir("/home/hendrik/project_dev/Kalman Filter")

# Generate realistic timestamps
def generate_realistic_timestamps(count=87):
    """Generate random timestamps with realistic patterns"""
    start_date = datetime(2024, 12, 1)
    excluded_start = datetime(2025, 5, 25)
    excluded_end = datetime(2025, 7, 26)
    end_date = datetime(2025, 9, 1)

    # Calculate days in each period
    period1_days = (excluded_start - start_date).days
    period2_days = (end_date - excluded_end).days

    # Distribute commits proportionally
    period1_count = int(count * period1_days / (period1_days + period2_days))
    period2_count = count - period1_count

    timestamps = []

    # Generate for period 1
    for _ in range(period1_count):
        day_offset = random.randint(0, period1_days - 1)
        date = start_date + timedelta(days=day_offset)

        # Working hours (8-22)
        hour = random.choices(
            list(range(8, 23)),
            weights=[5, 15, 20, 25, 20, 18, 15, 12, 10, 8, 5, 4, 3, 2, 1]
        )[0]
        minute = random.randint(0, 59)

        timestamp = date.replace(hour=hour, minute=minute, second=0)
        timestamps.append(timestamp)

    # Generate for period 2
    for _ in range(period2_count):
        day_offset = random.randint(1, period2_days)
        date = excluded_end + timedelta(days=day_offset)

        hour = random.choices(
            list(range(8, 23)),
            weights=[5, 15, 20, 25, 20, 18, 15, 12, 10, 8, 5, 4, 3, 2, 1]
        )[0]
        minute = random.randint(0, 59)

        timestamp = date.replace(hour=hour, minute=minute, second=0)
        timestamps.append(timestamp)

    # Sort chronologically
    timestamps.sort()

    # Add some clustering by duplicating nearby timestamps
    # Pick ~15% of commits to cluster
    cluster_count = int(count * 0.15)
    for _ in range(cluster_count):
        if len(timestamps) >= count:
            break
        idx = random.randint(0, len(timestamps) - 1)
        base_time = timestamps[idx]
        # Add a commit 10min-3hours after
        offset_minutes = random.randint(10, 180)
        new_time = base_time + timedelta(minutes=offset_minutes)
        timestamps.append(new_time)

    timestamps.sort()
    return timestamps[:count]  # Ensure exactly 'count' timestamps

def git_commit(message, date_str):
    """Create a git commit with specified date"""
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str

    result = subprocess.run(
        ['git', 'commit', '-m', message, f'--date={date_str}'],
        env=env,
        capture_output=True,
        text=True
    )
    return result.returncode == 0

# Generate timestamps
print("Generating 87 realistic timestamps...")
timestamps = generate_realistic_timestamps(87)

print(f"Generated {len(timestamps)} timestamps")
print(f"First: {timestamps[0]}")
print(f"Last: {timestamps[-1]}")
print(f"\nSample distribution:")
for i in range(0, min(10, len(timestamps))):
    print(f"  {timestamps[i]}")

# Export timestamps for use by commit script
with open('timestamps.txt', 'w') as f:
    for ts in timestamps:
        f.write(ts.strftime("%Y-%m-%d %H:%M:%S") + '\n')

print(f"\nTimestamps saved to timestamps.txt")
print(f"Ready to create commits!")

# Multi-Agent Development Coordination Guide

## Overview
This coordination system enables multiple AI agents to collaborate effectively on the steganography framework improvements.

## Directory Structure
```
coordination/
├── COORDINATION_GUIDE.md          # This file - main coordination guide
├── memory_bank/                   # Shared knowledge and discoveries
│   ├── calibration_values.md      # Discovered optimal signal parameters
│   ├── test_failures.md           # Analysis of failing tests
│   └── dependencies.md            # Environment setup knowledge
├── subtasks/                      # Individual task breakdowns
│   ├── task_001_calibration.md   # Signal calibration subtasks
│   ├── task_002_ffmpeg.md        # FFmpeg installation subtasks
│   └── task_003_optimization.md  # Algorithm optimization subtasks
└── orchestration/                 # Agent coordination
    ├── agent_assignments.md       # Who's working on what
    ├── progress_tracker.md        # Real-time progress updates
    └── integration_plan.md        # How pieces fit together
```

## Coordination Protocol

### 1. Task Assignment
- Check `orchestration/agent_assignments.md` before starting work
- Update with your agent ID and current task
- Avoid duplicate efforts by coordinating through this file

### 2. Knowledge Sharing
- Document all discoveries in `memory_bank/`
- Include failed attempts to prevent repetition
- Share optimal parameters immediately upon discovery

### 3. Progress Updates
- Update `orchestration/progress_tracker.md` every significant step
- Mark subtasks complete in respective `subtasks/` files
- Alert other agents of blockers or dependencies

### 4. Integration Points
- Follow the plan in `orchestration/integration_plan.md`
- Test integrations incrementally
- Document any API or interface changes

## Communication Standards

### Status Markers
- 🟢 COMPLETE - Task finished and tested
- 🟡 IN_PROGRESS - Currently being worked on
- 🔴 BLOCKED - Waiting on dependency or issue
- ⚪ TODO - Not yet started
- 🔵 REVIEW - Needs peer review

### Update Format
```markdown
## [Timestamp] Agent: [Agent_ID]
**Task**: [Brief description]
**Status**: [Status marker]
**Details**: [What was done/discovered]
**Next**: [What needs to happen next]
```

## Critical Rules
1. **No Parallel Work** on same file without coordination
2. **Test Before Commit** - Run relevant tests before marking complete
3. **Document Failures** - Failed approaches are valuable knowledge
4. **Share Parameters** - Any calibration values found must be shared immediately
5. **Atomic Changes** - Make small, focused changes that can be tested independently
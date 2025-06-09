# SPARC Quick Reference Card

## Basic Commands
```bash
# Show help
./claude-sparc.sh --help

# Basic usage
./claude-sparc.sh my-project requirements.md

# Dry run (preview)
./claude-sparc.sh --dry-run --verbose my-project spec.md
```

## Development Modes
| Mode | Description | Use Case |
|------|-------------|----------|
| `full` | Complete full-stack development | Web applications, complete systems |
| `backend-only` | Backend services and APIs | Microservices, server applications |
| `frontend-only` | Frontend application only | SPAs, mobile apps, UI libraries |
| `api-only` | REST/GraphQL API development | API services, data layers |

## Research Depths
| Depth | Description | Time Investment |
|-------|-------------|-----------------|
| `basic` | Quick overview and tech stack | Fast prototyping |
| `standard` | Comprehensive with competitive analysis | Most projects |
| `comprehensive` | Extensive with academic papers | Complex/research projects |

## Common Workflows

### Rapid Prototyping
```bash
./claude-sparc.sh --skip-research --coverage 80 --mode frontend-only prototype spec.md
```

### Production API
```bash
./claude-sparc.sh --mode api-only --research-depth comprehensive --verbose api-service spec.md
```

### Enterprise Application
```bash
./claude-sparc.sh --research-depth comprehensive --coverage 100 --commit-freq feature enterprise-app requirements.md
```

### Quick Backend Service
```bash
./claude-sparc.sh --mode backend-only --skip-research --no-parallel service spec.md
```

## Configuration Options

### Research Control
- `--skip-research` - Skip web research phase
- `--research-depth basic|standard|comprehensive` - Research thoroughness

### Development Control
- `--mode full|backend-only|frontend-only|api-only` - Development scope
- `--coverage 0-100` - Test coverage target (default: 100)
- `--skip-tests` - Skip test development (not recommended)

### Execution Control
- `--no-parallel` - Disable parallel execution
- `--commit-freq phase|feature|manual` - Commit frequency
- `--no-commits` - Disable automatic commits

### Output Control
- `--verbose` - Detailed logging
- `--quiet` - Minimal output
- `--output text|json|markdown` - Output format
- `--dry-run` - Preview without execution

## Tool Usage by Configuration

| Configuration | Tools Used |
|---------------|------------|
| Default | All tools (WebFetch, Batch, dispatch_agent, etc.) |
| `--skip-research` | No WebFetchTool |
| `--no-parallel` | No BatchTool, dispatch_agent |
| `--skip-research --no-parallel` | Basic tools only (View, Edit, Bash, etc.) |

## Success Indicators
- `<SPARC-COMPLETE>` - Full development lifecycle finished
- All quality gates passed
- Target test coverage achieved
- Production deployment ready

## Troubleshooting
```bash
# Check configuration
./claude-sparc.sh --dry-run --verbose project spec.md

# Validate README exists
ls -la your-readme.md

# Check MCP config
ls -la .roo/mcp.json
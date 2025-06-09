# SPARC Automated Development System

## Overview

The SPARC Automated Development System (`claude-sparc.sh`) is a comprehensive, generic workflow for automated software development using the SPARC methodology (Specification, Pseudocode, Architecture, Refinement, Completion). This system leverages Claude Code's built-in tools for parallel task orchestration, comprehensive research, and Test-Driven Development.

## Features

- **Comprehensive Research Phase**: Automated web research using parallel batch operations
- **Full SPARC Methodology**: Complete implementation of all 5 SPARC phases
- **TDD London School**: Test-driven development with mocks and behavior testing
- **Parallel Orchestration**: Concurrent development tracks and batch operations
- **Quality Assurance**: Automated linting, testing, and security validation
- **Detailed Commit History**: Structured commit messages for each development phase

## Usage

### Basic Usage
```bash
./claude-sparc.sh
```

### With Arguments
```bash
./claude-sparc.sh [OPTIONS] [PROJECT_NAME] [README_PATH]
```

### Help
```bash
./claude-sparc.sh --help
```

## Command Line Options

### Core Options
- `-h, --help` - Show help message and exit
- `-v, --verbose` - Enable verbose output for detailed logging
- `-d, --dry-run` - Show what would be executed without running
- `-c, --config FILE` - Specify MCP configuration file (default: .roo/mcp.json)

### Research Options
- `--skip-research` - Skip the web research phase entirely
- `--research-depth LEVEL` - Set research depth: basic, standard, comprehensive (default: standard)

### Development Options
- `--mode MODE` - Development mode: full, backend-only, frontend-only, api-only (default: full)
- `--skip-tests` - Skip test development (not recommended)
- `--coverage TARGET` - Test coverage target percentage (default: 100)
- `--no-parallel` - Disable parallel execution

### Commit Options
- `--commit-freq FREQ` - Commit frequency: phase, feature, manual (default: phase)
- `--no-commits` - Disable automatic commits

### Output Options
- `--output FORMAT` - Output format: text, json, markdown (default: text)
- `--quiet` - Suppress non-essential output

## Examples

### Basic Development
```bash
# Full-stack development with default settings
./claude-sparc.sh my-app docs/requirements.md

# Backend API development with verbose output
./claude-sparc.sh --mode api-only --verbose user-service api-spec.md

# Frontend-only development with custom coverage
./claude-sparc.sh --mode frontend-only --coverage 90 web-app ui-spec.md
```

### Research Configuration
```bash
# Skip research for rapid prototyping
./claude-sparc.sh --skip-research --coverage 80 prototype-app readme.md

# Comprehensive research for complex projects
./claude-sparc.sh --research-depth comprehensive enterprise-app requirements.md

# Basic research for simple projects
./claude-sparc.sh --research-depth basic simple-tool spec.md
```

### Development Modes
```bash
# API-only development
./claude-sparc.sh --mode api-only --commit-freq feature api-service spec.md

# Backend services only
./claude-sparc.sh --mode backend-only --no-parallel backend-service requirements.md

# Frontend application only
./claude-sparc.sh --mode frontend-only --output json frontend-app ui-spec.md
```

### Testing and Quality
```bash
# Skip tests for rapid prototyping (not recommended)
./claude-sparc.sh --skip-tests --commit-freq manual prototype readme.md

# Custom coverage target
./claude-sparc.sh --coverage 95 --verbose production-app requirements.md

# Manual commit control
./claude-sparc.sh --no-commits --dry-run complex-app spec.md
```

### Advanced Usage
```bash
# Dry run to preview execution
./claude-sparc.sh --dry-run --verbose my-project requirements.md

# Custom MCP configuration
./claude-sparc.sh --config custom-mcp.json --mode full my-app spec.md

# Quiet mode with JSON output
./claude-sparc.sh --quiet --output json --mode api-only service spec.md
```

## SPARC Phases Explained

### Phase 0: Research & Discovery
- **Parallel Web Research**: Uses `BatchTool` and `WebFetchTool` for comprehensive domain research
- **Technology Stack Analysis**: Researches best practices and framework comparisons
- **Implementation Patterns**: Gathers code examples and architectural patterns
- **Competitive Analysis**: Studies existing solutions and industry trends

### Phase 1: Specification
- **Requirements Analysis**: Extracts functional and non-functional requirements
- **User Stories**: Defines acceptance criteria and system boundaries
- **Technical Constraints**: Identifies technology stack and deployment requirements
- **Performance Targets**: Establishes SLAs and scalability goals

### Phase 2: Pseudocode
- **High-Level Architecture**: Defines major components and data flow
- **Algorithm Design**: Core business logic and optimization strategies
- **Test Strategy**: TDD approach with comprehensive test planning
- **Error Handling**: Recovery strategies and validation algorithms

### Phase 3: Architecture
- **Component Architecture**: Detailed specifications and interface definitions
- **Data Architecture**: Database design and access patterns
- **Infrastructure Architecture**: Deployment and CI/CD pipeline design
- **Security Architecture**: Access controls and compliance requirements

### Phase 4: Refinement (TDD Implementation)
- **Parallel Development Tracks**: Backend, frontend, and integration tracks
- **TDD London School**: Red-Green-Refactor cycles with behavior testing
- **Quality Gates**: Automated linting, analysis, and security scans
- **Performance Optimization**: Benchmarking and critical path optimization

### Phase 5: Completion
- **System Integration**: End-to-end testing and requirement validation
- **Documentation**: API docs, deployment guides, and runbooks
- **Production Readiness**: Monitoring, alerting, and security review
- **Deployment**: Automated deployment with validation

## Tool Utilization

### Core Tools
- **`BatchTool`**: Parallel execution of independent operations
- **`WebFetchTool`**: Comprehensive research and documentation gathering
- **`Bash`**: Git operations, CI/CD, testing, and deployment
- **`Edit/Replace`**: Code implementation and refactoring
- **`GlobTool/GrepTool`**: Code analysis and pattern detection
- **`dispatch_agent`**: Complex subtask delegation

### Quality Assurance Tools
- **Linting**: ESLint, Prettier, markdownlint
- **Testing**: Jest, Vitest, Cypress for comprehensive coverage
- **Security**: Security scans and vulnerability assessments
- **Performance**: Benchmarking and profiling tools
- **Documentation**: Automated API documentation generation

## Development Standards

### Code Quality
- **Modularity**: Files ≤ 500 lines, functions ≤ 50 lines
- **Security**: No hardcoded secrets, comprehensive input validation
- **Testing**: 100% test coverage with TDD London School approach
- **Documentation**: Self-documenting code with strategic comments
- **Performance**: Optimized critical paths with benchmarking

### Commit Standards
- **`feat:`** New features and major functionality
- **`test:`** Test implementation and coverage improvements
- **`fix:`** Bug fixes and issue resolution
- **`docs:`** Documentation updates and improvements
- **`arch:`** Architectural changes and design updates
- **`quality:`** Code quality improvements and refactoring
- **`deploy:`** Deployment and infrastructure changes

## Parallel Execution Strategy

### Research Phase
```bash
BatchTool(
  WebFetchTool("domain research"),
  WebFetchTool("technology analysis"),
  WebFetchTool("competitive landscape"),
  WebFetchTool("implementation patterns")
)
```

### Development Phase
```bash
# Concurrent tracks
Track 1: Backend Development (TDD)
Track 2: Frontend Development (TDD)
Track 3: Integration & QA
```

### Quality Assurance
```bash
BatchTool(
  Bash("npm run lint"),
  Bash("npm run test"),
  Bash("npm run security-scan"),
  Bash("npm run performance-test")
)
```

## Success Criteria

- ✅ **100% Test Coverage**: All code covered by comprehensive tests
- ✅ **Quality Gates Passed**: Linting, security, and performance validation
- ✅ **Production Deployment**: Successful deployment with monitoring
- ✅ **Documentation Complete**: Comprehensive docs and runbooks
- ✅ **Security Validated**: Security scans and compliance checks
- ✅ **Performance Optimized**: Benchmarks meet or exceed targets

## Configuration

### MCP Configuration
The system uses `.roo/mcp.json` for MCP server configuration. Ensure your MCP setup includes:
- File system access
- Web search capabilities
- Git integration
- Testing frameworks

### Allowed Tools
The script automatically configures the following tools:
```bash
--allowedTools "WebFetchTool,BatchTool,Bash,Edit,Replace,GlobTool,GrepTool,View,LS,dispatch_agent"
```

## Examples

### Web Application Development
```bash
./claude-sparc.sh "ecommerce-platform" "requirements/ecommerce-spec.md"
```

### API Service Development
```bash
./claude-sparc.sh "user-service-api" "docs/api-requirements.md"
```

### Data Processing Pipeline
```bash
./claude-sparc.sh "data-pipeline" "specs/data-processing-requirements.md"
```

## Troubleshooting

### Common Issues
1. **MCP Configuration**: Ensure `.roo/mcp.json` is properly configured
2. **Tool Permissions**: Use `--dangerously-skip-permissions` for development
3. **Network Access**: Ensure internet connectivity for web research
4. **Git Configuration**: Ensure git is configured for commits

### Debug Mode
Add `--verbose` flag for detailed execution logs:
```bash
./claude-sparc.sh "project" "readme.md" --verbose
```

## Contributing

To extend the SPARC system:
1. Fork the repository
2. Create feature branch
3. Follow SPARC methodology for changes
4. Submit pull request with comprehensive tests

## License

This SPARC Automated Development System is part of the claude-code-flow project and follows the same licensing terms.
# Project Overview: claude-code-flow

Last Updated: 2025-01-06

## Project Identity
- **Name**: claude-code-flow
- **Type**: RooCode MCP mode configuration project
- **Purpose**: Autonomous code execution and refinement agent for the RooCode agentic pipeline ecosystem
- **Status**: Specification phase (no implementation yet)

## Core Objectives
1. Create an autonomous agent that manages code generation, refactoring, and logic-level updates
2. Integrate seamlessly with the RooCode agent ecosystem
3. Implement MCP-based inputs and recursive task loops
4. Provide automated tool usage for complex codebase operations

## Architecture Overview

### Two MCP Modes

#### 1. code-flow Mode
- **Role**: Autonomous code execution and structural refinement
- **Capabilities**:
  - Code generation and refactoring
  - Logic-level updates
  - MCP-based input processing
  - Recursive task loop management
- **Integration Points**: tdd-runner, critic, reflection, memory-manager

#### 2. claude-code Mode  
- **Role**: General coding assistant with MCP tool integration
- **Capabilities**:
  - Multi-file editing
  - Pattern searching
  - Project navigation
  - Complex codebase operations

### Planned Directory Structure
```
/modes
  ├── code-flow/
  │   ├── handler.ts
  │   ├── config.json
  │   └── prompts/
  │       └── base_prompt.txt
/src
  └── ...
.mcp.json
.roomodes
```

## Integration Ecosystem

### Required Companion Modes
- `prompt-generator` - Generates prompts for code tasks
- `tdd-runner` - Executes test-driven development cycles
- `memory-manager` - Maintains context and state
- `reflection` - Analyzes and improves code quality
- `critic` - Provides code review and feedback

### Optional Modes
- `doc-writer` - Generates documentation

## Current Focus Areas

### Agentic Commands Stego Integration
The repository currently contains a fully implemented ultrasonic steganography system (`agentic_commands_stego/`) that demonstrates:
- Audio/video embedding and decoding
- MCP server integration
- Comprehensive test coverage
- API server implementation

This serves as a reference implementation for understanding:
- MCP tool patterns
- Testing strategies
- API design
- Multi-component integration

## Development Principles
1. **Autonomous Operation**: Minimize human intervention
2. **Tool Integration**: Leverage MCP tools effectively
3. **Quality Focus**: Maintain high code standards
4. **Ecosystem Compatibility**: Seamless integration with RooCode agents
5. **Iterative Refinement**: Continuous improvement through feedback loops
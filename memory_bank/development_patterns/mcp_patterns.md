# MCP Tool Usage Patterns

Last Updated: 2025-01-06

## Core MCP Tools and Their Optimal Usage

### File Discovery Tools

#### Glob Tool
**Purpose**: Find files by name pattern
**When to use**:
- Locating files with specific extensions
- Finding all test files
- Discovering configuration files
- Identifying component files

**Patterns**:
```bash
# Find all TypeScript files
pattern: "**/*.ts"

# Find all test files
pattern: "**/*.{test,spec}.{ts,js}"

# Find specific component files
pattern: "**/components/**/*.tsx"

# Find configuration files
pattern: "**/{package.json,tsconfig.json,.eslintrc.*}"
```

#### Grep Tool
**Purpose**: Search file contents
**When to use**:
- Finding function/class definitions
- Locating imports/dependencies
- Searching for TODO comments
- Finding configuration values

**Patterns**:
```bash
# Find class definitions
pattern: "^(export )?class \\w+"

# Find function definitions
pattern: "^(export )?(async )?function \\w+"

# Find imports from specific module
pattern: "from ['\"]@mcp/"

# Find TODO comments
pattern: "// (TODO|FIXME|HACK):"
```

### File Manipulation Tools

#### Read Tool
**Purpose**: Examine file contents
**Best practices**:
- Always read before editing
- Use offset/limit for large files
- Read multiple related files together
- Verify file exists before reading

#### Edit Tool
**Purpose**: Make single file changes
**Best practices**:
- Preserve exact indentation
- Use unique old_string values
- Make minimal changes
- Verify changes with Read after

#### MultiEdit Tool
**Purpose**: Make multiple changes to one file
**When to use**:
- Refactoring multiple functions
- Updating multiple imports
- Batch replacing patterns
- Complex file modifications

**Pattern**:
```json
{
  "file_path": "/path/to/file.ts",
  "edits": [
    {
      "old_string": "import old",
      "new_string": "import new"
    },
    {
      "old_string": "oldFunction",
      "new_string": "newFunction",
      "replace_all": true
    }
  ]
}
```

### Execution Tools

#### Bash Tool
**Purpose**: Execute commands
**Common uses**:
- Running tests
- Git operations
- Package management
- Build processes
- File system operations

**Best practices**:
- Quote file paths with spaces
- Use absolute paths
- Check command success
- Capture and handle errors

#### Task Tool
**Purpose**: Delegate complex operations
**When to use**:
- Multi-step operations
- Parallel investigations
- Complex searches
- Detailed analysis

**Pattern**:
```
description: "Analyze test coverage"
prompt: "Find all test files using Glob pattern '**/*.test.ts', 
         read each file to identify what components they test,
         create a coverage report showing which components have tests"
```

### Workflow Management

#### TodoWrite/TodoRead Tools
**Purpose**: Track development tasks
**When to use**:
- Multi-step implementations
- Complex refactoring
- Feature development
- Bug fix workflows

**Best practices**:
- Create specific, actionable items
- Update status in real-time
- Mark complete immediately
- Use priority levels appropriately

## Common Workflow Patterns

### Pattern 1: Codebase Analysis
```
1. Glob("**/*.{ts,tsx}") - Find all source files
2. Grep("export.*function|class") - Find exports
3. Read(selected_files) - Examine structure
4. TodoWrite(analysis_tasks) - Plan next steps
```

### Pattern 2: Refactoring Workflow
```
1. Grep(old_pattern) - Find all occurrences
2. Read(affected_files) - Understand context
3. TodoWrite(refactor_steps) - Plan changes
4. MultiEdit(batch_changes) - Apply refactoring
5. Bash("npm test") - Verify changes
```

### Pattern 3: Feature Implementation
```
1. Read(requirements) - Understand needs
2. Glob(related_files) - Find integration points
3. TodoWrite(implementation_plan) - Break down tasks
4. Edit/MultiEdit(implement) - Write code
5. Edit(write_tests) - Add tests
6. Bash("npm test") - Run tests
```

### Pattern 4: Debugging Workflow
```
1. Grep(error_pattern) - Find error locations
2. Read(error_context) - Understand issue
3. Task(investigate_cause) - Deep analysis
4. Edit(apply_fix) - Fix issue
5. Bash("npm test") - Verify fix
```

## Performance Optimization Patterns

### Batch Operations
- Use Task tool for parallel searches
- Combine multiple Glob patterns
- Read multiple files in one operation
- Use MultiEdit over multiple Edit calls

### Efficient Searching
- Start broad with Glob, narrow with Grep
- Use specific patterns to reduce results
- Leverage file path filters in Grep
- Cache search results for reuse

### Minimal File Operations
- Read once, edit multiple times
- Use MultiEdit for batch changes
- Avoid redundant file reads
- Clean up temporary files

## Error Handling Patterns

### File Not Found
```typescript
// Check existence with LS first
LS("/path/to/directory")
// Then safely read
Read("/path/to/directory/file.ts")
```

### Invalid Edit String
```typescript
// Read file first to get exact content
const content = Read(file_path)
// Use exact string from read output
Edit(file_path, exact_string_from_content, new_string)
```

### Command Failures
```typescript
// Capture and handle errors
const result = Bash("npm test")
if (result.includes("FAILED")) {
  // Handle test failures
}
```

## Integration Patterns

### With Agent Ecosystem
- Use Task to coordinate with other agents
- Pass structured data between tools
- Maintain context through TodoWrite
- Use consistent file paths

### With Version Control
```bash
# Standard git workflow
Bash("git status")
Bash("git add .")
Bash("git commit -m 'feat: description'")
Bash("git push")
```

### With Testing Frameworks
```bash
# Run specific test suites
Bash("npm test -- --testPathPattern=component")
# Run with coverage
Bash("npm test -- --coverage")
# Run in watch mode
Bash("npm test -- --watch")
```

## Best Practices Summary

1. **Always Read Before Edit**: Understand context
2. **Use Right Tool for Job**: Don't use Bash for file reading
3. **Batch When Possible**: Reduce tool calls
4. **Handle Errors Gracefully**: Expect failures
5. **Document Tool Usage**: Help future sessions
6. **Verify Changes**: Always test after modifications
7. **Maintain Clean State**: Clean up after operations
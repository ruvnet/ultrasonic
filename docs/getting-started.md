# Getting Started with Claude Code SDK

Welcome to the Claude Code SDK! This guide will help you get up and running with the SDK quickly and efficiently.

## 📋 Prerequisites

Before you begin, ensure you have:
- Node.js (version 14 or higher) installed on your system
- An Anthropic account with API access
- Basic familiarity with command line interfaces

## 🚀 Installation

### NPM Installation (Recommended)

```bash
npm install -g claude-code-sdk
```

### Yarn Installation

```bash
yarn global add claude-code-sdk
```

### Direct Download

For systems without Node.js package managers, you can download the binary directly from our releases page.

### Verify Installation

After installation, verify that the SDK is properly installed:

```bash
claude --version
```

## 🔐 Authentication

### Creating an Anthropic API Key

1. Visit the [Anthropic Console](https://console.anthropic.com/)
2. Sign in to your account or create a new one
3. Navigate to the API Keys section
4. Click "Create Key" and give it a descriptive name
5. Copy the generated API key (keep it secure!)

### Setting Up Environment Variables

#### On macOS/Linux

Add the following line to your shell configuration file (`.bashrc`, `.zshrc`, or `.profile`):

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Then reload your shell configuration:

```bash
source ~/.bashrc  # or ~/.zshrc
```

#### On Windows (Command Prompt)

```cmd
setx ANTHROPIC_API_KEY "your-api-key-here"
```

#### On Windows (PowerShell)

```powershell
$env:ANTHROPIC_API_KEY = "your-api-key-here"
```

#### Temporary Session (All Platforms)

For a temporary session, you can set the environment variable directly:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Verify Authentication

Test your authentication setup:

```bash
claude -p "Hello, Claude!"
```

## 🎯 First Steps

### Basic Usage

The Claude Code SDK supports command line usage with simple and powerful commands. Here are some basic examples to get you started:

#### Simple Text Generation

```bash
claude -p "Write a function to calculate Fibonacci numbers"
```

#### Using Stdin with Pipes

You can pipe content to Claude for analysis or processing:

```bash
echo "Explain this code" | claude -p
```

```bash
cat my-script.js | claude -p "Review this code for potential improvements"
```

#### File Processing

```bash
claude -p "Analyze this code for bugs" < my-file.py
```

### Output Formats

The SDK supports multiple output formats to suit different use cases:

#### JSON Output

For structured data and programmatic processing:

```bash
claude -p "Generate a hello world function" --output-format json
```

#### Streaming JSON

For real-time output during longer operations:

```bash
claude -p "Build a React component" --output-format stream-json
```

#### Plain Text (Default)

```bash
claude -p "Explain how recursion works"
```

## 🖥️ Command Line Basics

### Core Commands

| Command | Description | Example |
|---------|-------------|----------|
| `-p, --prompt` | Specify the prompt text | `claude -p "Your prompt here"` |
| `--output-format` | Set output format (text, json, stream-json) | `claude -p "Hello" --output-format json` |
| `--help` | Show help information | `claude --help` |
| `--version` | Display version information | `claude --version` |

### Advanced Options

#### Model Selection

```bash
claude -p "Your prompt" --model claude-3-sonnet
```

#### Temperature Control

```bash
claude -p "Creative writing task" --temperature 0.8
```

#### Maximum Tokens

```bash
claude -p "Long analysis task" --max-tokens 2000
```

### Configuration Files

You can create a configuration file to set default options:

**~/.claude-config.json**
```json
{
  "model": "claude-3-sonnet",
  "temperature": 0.7,
  "max_tokens": 1000,
  "output_format": "text"
}
```

## 🔧 Common Use Cases

### Code Generation

```bash
claude -p "Create a Python class for managing a todo list"
```

### Code Review

```bash
cat my-code.js | claude -p "Review this code and suggest improvements"
```

### Documentation

```bash
claude -p "Generate documentation for this function" < function.py
```

### Debugging Help

```bash
claude -p "Help me debug this error: TypeError: Cannot read property 'length' of undefined"
```

## 💡 Tips and Best Practices

### 🎯 Writing Effective Prompts

- **Be specific**: Instead of "fix my code", try "optimize this function for better performance"
- **Provide context**: Include relevant information about your project or requirements
- **Use examples**: Show Claude what you're looking for with concrete examples

### 🔒 Security Considerations

- Never commit API keys to version control
- Use environment variables for sensitive configuration
- Regularly rotate your API keys
- Be mindful of the code you share with the API

### ⚡ Performance Tips

- Use streaming output for long-running tasks
- Batch similar requests when possible
- Consider using configuration files for repeated settings

## 🚧 Coming Soon

The Claude Code SDK is actively being developed. Here's what's coming:

- **TypeScript SDK**: Full TypeScript support with type definitions
- **Python SDK**: Native Python integration and bindings
- **IDE Extensions**: VS Code, IntelliJ, and other popular IDE integrations
- **Advanced MCP Features**: Enhanced Model Context Protocol capabilities

## 🆘 Troubleshooting

### Common Issues

#### Authentication Errors

```
Error: Invalid API key
```

**Solution**: Verify your `ANTHROPIC_API_KEY` environment variable is set correctly.

#### Command Not Found

```
claude: command not found
```

**Solution**: Ensure the SDK is installed globally and your PATH includes npm global binaries.

#### Network Issues

```
Error: Request timeout
```

**Solution**: Check your internet connection and firewall settings.

### Getting Help

If you encounter issues:

1. Check the [troubleshooting section](troubleshooting.md) in our documentation
2. Search existing issues in our GitHub repository
3. Join our community Discord for real-time help
4. Create a new issue with detailed information about your problem

## 📚 Next Steps

Now that you have the basics down, explore these advanced topics:

- [Core Concepts](core-concepts.md) - Understand the SDK architecture
- [MCP Integration](mcp-integration/overview.md) - Connect external tools and services
- [Advanced Usage](usage-guides/advanced-usage.md) - Complex workflows and optimization
- [API Reference](api-reference.md) - Complete command and option reference

---

*Ready to start building? Try your first command and see the power of Claude Code SDK in action!*
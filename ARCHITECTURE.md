# LLM DocGen - Architecture Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Principles](#architecture-principles)
3. [Component Design](#component-design)
4. [Data Flow](#data-flow)
5. [Module Structure](#module-structure)
6. [Extension Points](#extension-points)
7. [Security Considerations](#security-considerations)
8. [Performance Optimization](#performance-optimization)

---

## System Overview

### Purpose
LLM DocGen is a command-line tool that automatically generates documentation for Python projects (with a focus on LLM/ML codebases) by:
1. Parsing Python source code using AST
2. Extracting usage examples from Jupyter notebooks
3. Rendering documentation using Jinja2 templates
4. Outputting Markdown (or HTML) documentation

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Layer                             │
│  (Click commands: generate, init, list-templates)            │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator Layer                        │
│  (Repository processing, coordination)                       │
└─────┬──────────────────────────────────────────────┬────────┘
      │                                                │
      ▼                                                ▼
┌──────────────────┐                          ┌───────────────┐
│  Parser Layer    │                          │ Template Layer│
│                  │                          │               │
│ - Python Parser  │                          │ - Jinja2 Env  │
│ - Notebook Parser│                          │ - Built-in    │
│ - (Future: JS)   │                          │   Templates   │
└──────┬───────────┘                          │ - Custom      │
       │                                      │   Templates   │
       │                                      └───────┬───────┘
       ▼                                              │
┌──────────────────┐                                  │
│   Data Models    │◄─────────────────────────────────┘
│  (Dataclasses)   │
│                  │
│ - ClassInfo      │
│ - FunctionInfo   │
│ - ExampleInfo    │
└──────┬───────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│                      Output Layer                             │
│  (File writing, validation, formatting)                       │
└──────────────────────────────────────────────────────────────┘
```

---

## Architecture Principles

### 1. Separation of Concerns
- **Parsing** is independent of **rendering**
- **Data models** act as contract between layers
- **CLI** handles user interaction, not business logic

### 2. Extensibility
- New parsers can be added without changing core logic
- Templates are pluggable and customizable
- Configuration-driven behavior

### 3. Testability
- Pure functions where possible
- Dependency injection for file I/O
- Minimal global state

### 4. Simplicity
- Prefer standard library over dependencies
- Avoid over-engineering
- Clear, readable code over clever optimizations

### 5. Fail-Fast with Grace
- Validate inputs early
- Fail loudly on user errors
- Recover gracefully from expected failures (bad files)

---

## Component Design

### 3.1 CLI Layer (`src/llm_docgen/cli/`)

#### Responsibilities
- Parse command-line arguments
- Validate user input
- Coordinate high-level workflow
- Display progress and errors to user

#### Key Modules

**`commands.py`** - Main CLI commands
```python
@click.group()
def cli():
    """Main CLI entry point"""

@cli.command()
@click.option('--repo', required=True)
@click.option('--output', default='docs')
@click.option('--template', default='default')
def generate(repo: str, output: str, template: str):
    """Generate documentation"""
    # 1. Validate inputs
    # 2. Load configuration
    # 3. Call orchestrator
    # 4. Display results
```

**Design Decisions:**
- Use Click for CLI (better than argparse for complex CLIs)
- Keep CLI thin - delegate to orchestrator
- Rich progress bars using tqdm
- Structured error messages

---

### 3.2 Orchestrator Layer (`src/llm_docgen/core/`)

#### Responsibilities
- Coordinate parsing and rendering
- Handle repository cloning
- Manage file discovery and filtering
- Collect statistics

#### Key Modules

**`orchestrator.py`** - Main workflow coordinator
```python
class DocumentationGenerator:
    def __init__(self, config: Config):
        self.config = config
        self.parsers = {
            '.py': PythonParser(),
            '.ipynb': NotebookParser()
        }
    
    def generate(self, repo_path: Path) -> GenerationResult:
        """Main generation workflow"""
        # 1. Discover files
        # 2. Parse each file
        # 3. Aggregate results
        # 4. Render templates
        # 5. Write output
        # 6. Return statistics
```

**`repository.py`** - Repository handling
```python
class RepositoryProcessor:
    def clone(self, url: str, dest: Path) -> Path:
        """Clone Git repository"""
    
    def discover_files(self, root: Path, 
                      patterns: List[str]) -> List[Path]:
        """Find all relevant files"""
    
    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded"""
```

**Design Decisions:**
- Single orchestrator class for clarity
- Strategy pattern for different parsers
- Progress reporting via callbacks
- Collect errors but don't fail immediately

---

### 3.3 Parser Layer (`src/llm_docgen/parsers/`)

#### Responsibilities
- Extract structured data from source files
- Handle parsing errors gracefully
- Return standardized data models

#### Key Modules

**`base.py`** - Base parser interface
```python
class Parser(ABC):
    @abstractmethod
    def parse(self, file_path: Path) -> ParseResult:
        """Parse file and return structured data"""
    
    @abstractmethod
    def can_parse(self, file_path: Path) -> bool:
        """Check if this parser can handle the file"""
```

**`python_parser.py`** - Python AST parser
```python
class PythonParser(Parser):
    def parse(self, file_path: Path) -> ParseResult:
        """Parse Python file using AST"""
        # 1. Read file
        # 2. Parse AST
        # 3. Visit nodes (classes, functions)
        # 4. Extract metadata
        # 5. Return ParseResult
    
class CodeAnalyzer(ast.NodeVisitor):
    """AST visitor for extracting information"""
    def visit_ClassDef(self, node):
        """Extract class information"""
    
    def visit_FunctionDef(self, node):
        """Extract function information"""
```

**`notebook_parser.py`** - Jupyter notebook parser
```python
class NotebookParser(Parser):
    def parse(self, file_path: Path) -> ParseResult:
        """Parse Jupyter notebook"""
        # 1. Load notebook with nbformat
        # 2. Extract code cells
        # 3. Find example markers
        # 4. Extract markdown context
        # 5. Return ParseResult
```

**Design Decisions:**
- Abstract base class for consistent interface
- AST visitor pattern for Python parsing
- Error handling at parser level (return errors, don't raise)
- Immutable data models

---

### 3.4 Data Models (`src/llm_docgen/models/`)

#### Responsibilities
- Define data structures for parsed code
- Provide type safety
- Enable serialization/deserialization

#### Key Models

```python
@dataclass
class FunctionInfo:
    """Information about a function"""
    name: str
    docstring: str
    parameters: List[Parameter]
    return_type: Optional[str]
    decorators: List[str]
    lineno: int
    file_path: Path
    is_async: bool = False
    is_method: bool = False

@dataclass
class Parameter:
    """Function parameter"""
    name: str
    type_hint: Optional[str] = None
    default_value: Optional[str] = None

@dataclass
class ClassInfo:
    """Information about a class"""
    name: str
    docstring: str
    methods: List[FunctionInfo]
    bases: List[str]
    attributes: List[Attribute]
    lineno: int
    file_path: Path

@dataclass
class ExampleInfo:
    """Usage example from notebook"""
    description: str
    code: str
    output: Optional[str] = None
    cell_index: int = 0
    notebook_path: Optional[Path] = None

@dataclass
class ParseResult:
    """Result of parsing a file"""
    file_path: Path
    classes: List[ClassInfo]
    functions: List[FunctionInfo]
    examples: List[ExampleInfo]
    module_docstring: Optional[str]
    errors: List[str]
    parse_time: float

@dataclass
class GenerationResult:
    """Result of documentation generation"""
    files_processed: int
    files_skipped: int
    total_classes: int
    total_functions: int
    total_examples: int
    output_path: Path
    errors: List[str]
    generation_time: float
```

**Design Decisions:**
- Use dataclasses for simplicity
- Immutable where possible (frozen=True)
- Optional fields have defaults
- Include metadata (line numbers, paths) for linking

---

### 3.5 Template Layer (`src/llm_docgen/templating/`)

#### Responsibilities
- Manage Jinja2 environment
- Load and validate templates
- Provide custom filters
- Render documentation

#### Key Modules

**`renderer.py`** - Template rendering
```python
class TemplateRenderer:
    def __init__(self, template_dirs: List[Path]):
        self.env = self._create_jinja_env(template_dirs)
        self._add_custom_filters()
    
    def render(self, template_name: str, 
               context: Dict) -> str:
        """Render template with context"""
        template = self.env.get_template(template_name)
        return template.render(context)
    
    def validate_template(self, template_name: str) -> bool:
        """Check if template is valid"""
    
    def _add_custom_filters(self):
        """Add custom Jinja2 filters"""
        self.env.filters['code_block'] = code_block_filter
        self.env.filters['markdown_escape'] = markdown_escape_filter
```

**`filters.py`** - Custom Jinja2 filters
```python
def code_block_filter(code: str, language: str = 'python') -> str:
    """Format code as markdown code block"""
    return f"```{language}\n{code}\n```"

def markdown_escape_filter(text: str) -> str:
    """Escape special markdown characters"""
    # Escape *, _, [, ], etc.

def indent_filter(text: str, spaces: int = 4) -> str:
    """Indent text by N spaces"""
```

**Design Decisions:**
- Jinja2 for templating (de facto standard)
- Support template inheritance
- Custom filters for common formatting tasks
- Template discovery from multiple locations

---

### 3.6 Configuration (`src/llm_docgen/config/`)

#### Responsibilities
- Load configuration from files
- Merge CLI args with config file
- Validate configuration
- Provide defaults

#### Key Modules

**`config.py`** - Configuration management
```python
@dataclass
class Config:
    """Application configuration"""
    project_name: str
    output_dir: Path
    template_name: str
    exclude_patterns: List[str]
    include_private: bool
    verbose: bool
    
    @classmethod
    def from_file(cls, path: Path) -> 'Config':
        """Load config from YAML file"""
    
    @classmethod
    def from_cli(cls, **kwargs) -> 'Config':
        """Create config from CLI args"""
    
    def merge(self, other: 'Config') -> 'Config':
        """Merge two configs (other takes precedence)"""
```

**Design Decisions:**
- YAML for config files (readable, standard)
- Dataclass for type safety
- CLI args override file config
- Validation on load

---

## Data Flow

### End-to-End Generation Flow

```
1. User Input (CLI)
   ├─ Repository URL/path
   ├─ Output directory
   ├─ Template name
   └─ Options/flags
        │
        ▼
2. Configuration Loading
   ├─ Load .llmdocgen.yaml (if exists)
   ├─ Merge with CLI args
   └─ Validate config
        │
        ▼
3. Repository Processing
   ├─ Clone repo (if URL) or use local path
   ├─ Discover files (.py, .ipynb)
   └─ Filter exclusions
        │
        ▼
4. Parsing Phase (parallel)
   ├─ For each .py file:
   │   ├─ Parse with PythonParser
   │   ├─ Extract classes/functions
   │   └─ Create ParseResult
   │
   └─ For each .ipynb file:
       ├─ Parse with NotebookParser
       ├─ Extract examples
       └─ Create ParseResult
        │
        ▼
5. Aggregation
   ├─ Collect all ParseResults
   ├─ Group by type (classes, functions, examples)
   ├─ Sort/organize
   └─ Build template context
        │
        ▼
6. Template Rendering
   ├─ Load template
   ├─ Validate template
   ├─ Render with context
   └─ Generate markdown
        │
        ▼
7. Output Writing
   ├─ Create output directory
   ├─ Write documentation files
   ├─ Generate index/TOC
   └─ Copy assets (if any)
        │
        ▼
8. Result Reporting
   ├─ Display statistics
   ├─ Report errors/warnings
   └─ Exit with status code
```

### Error Handling Flow

```
Error Occurs
    │
    ├─ Fatal Error (validation, template not found)
    │   ├─ Log error
    │   ├─ Display user-friendly message
    │   └─ Exit with code 1
    │
    └─ Non-Fatal Error (parse error in file)
        ├─ Log warning
        ├─ Add to error list
        ├─ Continue processing
        └─ Report in summary
```

---

## Module Structure

### Current Structure
```
llm-docgen/
├── src/
│   └── llm_docgen/
│       ├── __init__.py
│       ├── cli/
│       │   ├── __init__.py
│       │   └── commands.py
│       ├── parsers/
│       │   ├── __init__.py
│       │   ├── python_parser.py
│       │   └── notebook_parser.py
│       ├── templating/
│       │   ├── __init__.py
│       │   └── renderer.py
│       └── templates/
│           ├── base.md.j2
│           └── api.md.j2
├── tests/
│   ├── unit/
│   │   └── test_python_parser.py
│   └── test_templating.py
├── pyproject.toml
└── README.md
```

### Recommended Structure (Complete)
```
llm-docgen/
├── src/
│   └── llm_docgen/
│       ├── __init__.py           # Package init, version
│       ├── cli/
│       │   ├── __init__.py
│       │   └── commands.py       # CLI commands
│       ├── core/
│       │   ├── __init__.py
│       │   ├── orchestrator.py   # Main workflow
│       │   └── repository.py     # Repo handling
│       ├── parsers/
│       │   ├── __init__.py
│       │   ├── base.py           # Base parser class
│       │   ├── python_parser.py
│       │   └── notebook_parser.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── data_models.py    # Dataclasses
│       ├── templating/
│       │   ├── __init__.py
│       │   ├── renderer.py       # Template engine
│       │   └── filters.py        # Custom filters
│       ├── config/
│       │   ├── __init__.py
│       │   └── config.py         # Config management
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── file_utils.py     # File operations
│       │   ├── git_utils.py      # Git operations
│       │   └── logging_utils.py  # Logging setup
│       └── templates/
│           ├── base.md.j2
│           ├── default.md.j2
│           ├── api-reference.md.j2
│           ├── examples.md.j2
│           └── minimal.md.j2
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── unit/
│   │   ├── test_python_parser.py
│   │   ├── test_notebook_parser.py
│   │   ├── test_orchestrator.py
│   │   ├── test_renderer.py
│   │   └── test_config.py
│   ├── integration/
│   │   ├── test_full_workflow.py
│   │   └── test_cli.py
│   └── fixtures/
│       ├── sample_project/       # Sample Python project
│       ├── sample_notebook.ipynb
│       └── sample_config.yaml
├── docs/
│   ├── quickstart.md
│   ├── templates.md
│   ├── configuration.md
│   └── architecture.md
├── scripts/
│   ├── test_parser.py
│   └── benchmark.py
├── pyproject.toml
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── CHANGELOG.md
```

---

## Extension Points

### Adding a New Parser

1. Create parser class inheriting from `Parser`
2. Implement `parse()` and `can_parse()` methods
3. Register in orchestrator's parser registry
4. Add tests

Example:
```python
# src/llm_docgen/parsers/javascript_parser.py
class JavaScriptParser(Parser):
    def can_parse(self, file_path: Path) -> bool:
        return file_path.suffix in ['.js', '.ts']
    
    def parse(self, file_path: Path) -> ParseResult:
        # Use esprima or similar JS parser
        # Extract JSDoc comments
        # Return ParseResult
```

### Adding a New Template

1. Create `.j2` file in templates directory
2. Use base template if desired
3. Document available variables in comments
4. Add example usage

### Adding Custom Filters

1. Create filter function in `filters.py`
2. Register in `TemplateRenderer._add_custom_filters()`
3. Document filter usage

---

## Security Considerations

### Input Validation
- Validate all file paths (prevent path traversal)
- Sanitize repository URLs
- Limit clone depth and size
- Timeout for long operations

### Code Execution
- **Never** use `eval()` or `exec()` on parsed code
- Use AST parsing only (no runtime execution)
- Sandbox notebook execution if adding that feature

### Template Injection
- Use Jinja2's autoescaping where appropriate
- Validate template syntax before rendering
- Don't allow user-provided templates from untrusted sources

### Dependency Security
- Regular dependency updates
- Use `safety` to check for vulnerabilities
- Pin critical dependencies

---

## Performance Optimization

### Parsing Optimization
- **Parallel processing** - Parse files concurrently
- **Caching** - Cache AST for large files
- **Lazy loading** - Don't load all files into memory
- **Incremental parsing** - Only reparse changed files

### Memory Optimization
- **Streaming** - Process files one at a time
- **Garbage collection** - Clean up after each file
- **Limit recursion** - Set max depth for nested classes

### I/O Optimization
- **Batch writes** - Write multiple files at once
- **Compression** - Compress large output files
- **Async I/O** - Use asyncio for network operations

---

## Future Architecture Considerations

### Plugin System
- Allow third-party parsers
- Plugin discovery mechanism
- Plugin API contract

### Distributed Processing
- Split large repos across workers
- Message queue for coordination
- Distributed cache

### Web Service
- REST API for documentation generation
- Web UI for configuration
- Real-time preview

---

## Design Trade-offs

### Trade-off 1: Sync vs Async
**Decision:** Use sync for MVP, add async later  
**Reasoning:** Simpler code, easier testing, sufficient for most use cases  
**Future:** Add async for large repos or web service

### Trade-off 2: Dependency on AST vs Runtime Inspection
**Decision:** Use AST only  
**Reasoning:** Safe, no code execution, works on any code  
**Limitation:** Can't get runtime type information

### Trade-off 3: Single File vs Multi-File Output
**Decision:** Support both  
**Reasoning:** Different use cases (simple vs comprehensive docs)

### Trade-off 4: Built-in vs External Template Engine
**Decision:** Use Jinja2  
**Reasoning:** Standard, powerful, well-documented  
**Alternative considered:** Custom template engine (rejected: too complex)

---

## Conclusion

This architecture provides a solid foundation for the LLM DocGen project:

**Strengths:**
- Clear separation of concerns
- Extensible design
- Testable components
- Simple but powerful

**Areas for Improvement:**
- Performance optimization needed for large repos
- Plugin system not yet designed
- Limited to Python currently

**Next Steps:**
- Implement missing components (orchestrator, models)
- Add comprehensive testing
- Optimize performance
- Document public APIs

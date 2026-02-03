# NV Line Agent

A sophisticated AI-powered research agent that conducts deep research and generates comprehensive reports using multi-agent orchestration.

## 🚀 Features

- **Multi-Agent Research System**: Coordinates specialized agents for efficient research execution
- **Intelligent Research Scope Clarification**: Interactive user clarification to refine research requirements
- **Comprehensive Web Search**: Integration with Tavily search API for real-time information gathering
- **Cloud Storage Integration**: Automatic report storage to Supabase cloud storage
- **Structured Report Generation**: Professional markdown reports with proper citations
- **Async Workflow**: Non-blocking execution for optimal performance

## 🏗️ Architecture

The system operates in two distinct phases:

### Phase 1: Research Scope Clarification
- **User Interaction**: Gathers and refines research requirements through iterative questioning
- **Research Brief Generation**: Creates comprehensive research briefs from user input
- **Quality Control**: Limits clarification exchanges to maintain efficiency (max 3 rounds)

### Phase 2: Research Execution
- **Supervisor Agent**: Coordinates research tasks and delegates to specialized sub-agents
- **Researcher Agents**: Conduct actual data collection and analysis using web search tools
- **Writer Agent**: Synthesizes findings into comprehensive final reports
- **Cloud Storage**: Automatically uploads reports to Supabase storage

## 📁 Project Structure

```
NV-Line-Agent/
├── helper/                          # Utility modules and configurations
│   ├── state_config.py             # State management for agent workflows
│   ├── prompts.py                  # Prompt templates for all agents
│   ├── tools.py                    # Research tools (search, thinking, delegation)
│   ├── utils.py                    # Utility functions
│   └── llm_output_schema_config.py # LLM output schemas
├── phases/                          # Workflow phase implementations
│   ├── research_scope.py           # Research scope clarification phase
│   └── research_execution/         # Research execution phase
│       ├── lead_researcher.py      # Supervisor agent implementation
│       ├── researcher.py          # Individual researcher agent
│       └── writer.py              # Report generation and cloud storage
├── main.py                         # Main orchestrator and entry point
├── pyproject.toml                  # Project dependencies and configuration
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.12 or higher
- UV package manager (recommended) or pip

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NV-Line-Agent
   ```

2. **Install dependencies**
   ```bash
   uv sync
   # or with pip: pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your API keys:
   ```env
   # Required for research agents with external search
   TAVILY_API_KEY=your_tavily_api_key_here
   
   # Required for model usage
   OPENAI_BASE_URL=your_openai_base_url_here
   OPENAI_API_KEY=your_openai_api_key_here
   
   # For evaluation and tracing (optional)
   LANGSMITH_API_KEY=your_langsmith_api_key_here
   LANGSMITH_TRACING=true
   LANGSMITH_PROJECT=deep_research_from_scratch
   
   # For cloud storage (Supabase)
   SUPABASE_URL=your_supabase_project_url_here
   SUPABASE_KEY=your_supabase_service_role_key_here
   ```

### Supabase Setup (for cloud storage)

1. **Create a Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Create a new free project
   - Note your project URL and service role key

2. **Create Storage Bucket**
   - In Supabase Dashboard → Storage
   - Create a bucket named `"reports"`
   - Set bucket to public (optional) or keep private

3. **Update Environment Variables**
   - Add your Supabase URL and service role key to `.env`

## 🚀 Usage

### Running the Research Agent

```bash
python main.py
```

The system will:
1. **Prompt for research topic**: Enter your research question
2. **Clarify requirements**: Answer up to 3 clarification questions if needed
3. **Conduct research**: Automatically execute multi-agent research
4. **Generate report**: Create comprehensive markdown report
5. **Save to cloud**: Upload report to Supabase storage

### Example Workflow

```
User: What are the latest developments in quantum computing?

Agent: I need to clarify your research needs:
- Are you interested in hardware advances or theoretical breakthroughs?
- Any specific companies or research institutions to focus on?
- What timeframe for "latest" developments?

User: Focus on hardware advances from major tech companies in the last 6 months

Agent: [Conducts research using multiple specialized agents]
[Generates comprehensive report with citations]
[Uploads report to Supabase cloud storage]
```

## 🔧 Configuration

### Model Configuration
- Default model: `openai:gpt-4.1` (configurable in code)
- Token limits: 32,000 tokens for report generation
- Supports OpenAI-compatible APIs

### Research Parameters
- **Clarification rounds**: Maximum 3 exchanges
- **Search results**: 3 results per query
- **Research iterations**: Configurable limits for depth vs. efficiency
- **Parallel agents**: Up to 3 concurrent research units

### Storage Configuration
- **Local**: Timestamped filenames (if enabled)
- **Cloud**: Supabase storage with organized folder structure
- **Format**: Markdown files with proper metadata

## 🤖 Agent System

### Research Supervisor
- **Role**: Orchestrates research tasks and delegates to specialists
- **Tools**: `ConductResearch`, `ResearchComplete`, `think_tool`
- **Strategy**: Breaks complex topics into manageable sub-tasks

### Research Agents
- **Role**: Conduct actual web searches and gather information
- **Tools**: `tavily_search`, `think_tool`
- **Process**: Search → Reflect → Analyze → Continue/Complete

### Writer Agent
- **Role**: Synthesizes findings into comprehensive reports
- **Features**: Structured markdown, proper citations, cloud storage
- **Output**: Professional research reports with source references

## 📊 State Management

The system uses LangGraph for sophisticated state management:

- **AgentState**: Main workflow state with research brief, notes, and messages
- **ResearcherState**: Individual agent state with iteration tracking
- **SupervisorState**: Coordination state for multi-agent orchestration
- **Thread Isolation**: Separate contexts for different research sessions

## 🔍 Research Tools

### Tavily Search Integration
- Real-time web search capabilities
- Content summarization and processing
- Deduplication of search results
- Support for various content types

### Thinking Tool
- Strategic reflection after each search
- Gap assessment and quality evaluation
- Decision-making for research continuation
- Systematic approach planning

## 📈 Performance Features

- **Async/Await Patterns**: Non-blocking execution
- **Parallel Research**: Multiple agents working simultaneously
- **Memory Management**: Efficient state tracking and cleanup
- **Error Handling**: Graceful failure recovery and reporting

## 🛡️ Safety & Quality

- **Input Validation**: Proper sanitization of user inputs
- **Output Filtering**: Removal of internal agent reasoning from final reports
- **Citation Management**: Proper source attribution and verification
- **Error Boundaries**: Isolated failure handling between components

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section below
2. Review the configuration requirements
3. Verify API key setup
4. Check Supabase bucket configuration

## 🔧 Troubleshooting

### Common Issues

**Git Lock File Error**
```bash
rm -f .git/index.lock
git reset --hard HEAD
```

**Missing Environment Variables**
- Verify `.env` file exists and is properly configured
- Check all required API keys are set
- Ensure Supabase credentials are correct

**Supabase Upload Failures**
- Verify bucket exists and is named `"reports"`
- Check service role key permissions
- Ensure bucket permissions allow uploads

**Search API Issues**
- Verify Tavily API key is valid
- Check internet connectivity
- Ensure search queries are properly formatted

### Debug Mode

Enable detailed logging by setting:
```env
LANGSMITH_TRACING=true
```

This will provide detailed execution traces for debugging.

---

**Built with ❤️ using LangGraph, LangChain, and Supabase**
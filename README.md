# Chat Session Analysis Pipeline

A robust Python pipeline for analyzing chat session data, classifying user intents, and extracting insights from conversational data.

## 🎯 Overview

This pipeline processes JSONL chat session data and performs comprehensive analysis including:

- **Intent Classification**: Categorizes user queries into 6 intent types
- **Funnel Stage Mapping**: Maps queries to customer journey stages
- **Brand Detection**: Identifies mentions of 100+ major brands across industries
- **Support Query Flagging**: Identifies troubleshooting and support requests
- **Session Analytics**: Tracks session-level metrics and engagement patterns

## 📊 Features

### Intent Classification

- **Commercial**: Purchase, pricing, subscription queries
- **Paraphrase/Edit**: Rewriting, summarization, grammar requests
- **Educational/Quiz**: Learning, testing, concept explanation
- **Informational**: How-to, what-is, general knowledge questions
- **Navigational**: Account access, settings, dashboard requests
- **Other**: Uncategorized queries

### Funnel Stages

- **Awareness**: Discovery and learning queries
- **Consideration**: Comparison and research queries
- **Decision**: Commercial and purchase intent
- **Retention**: Support and troubleshooting

### Brand Detection

Covers 100+ brands across categories:

- Global Tech (Google, Microsoft, Apple, etc.)
- SaaS & Cloud (OpenAI, Slack, AWS, etc.)
- Ecommerce & D2C (Nike, Tesla, Amazon, etc.)
- Automotive (Ford, Toyota, BMW, etc.)
- Travel & Hospitality (Expedia, Airbnb, etc.)
- Food & Beverage (McDonald's, Starbucks, etc.)
- Media & Entertainment (Disney, Netflix, etc.)
- Financial Services (Bank of America, JPMorgan, etc.)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pandas
- pyarrow (for Parquet support)

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd analysis
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your data**

   - Place your JSONL chat session file as `chat_sessions_dec2024.json`
   - Each line should contain a JSON object with `id` and `messages` fields

4. **Run the pipeline**
   ```bash
   python sample_pipeline.py
   ```

## ⚙️ Configuration

Edit the configuration section in `sample_pipeline.py`:

```python
FILE_PATH    = "./chat_sessions_dec2024.json"  # your JSONL path
CHUNKSIZE    = 100_000                        # adjust for your RAM
SAMPLE_FRAC  = 0.01                           # 1% sampling
SMOKE_TEST   = True                          # set to False for full run
```

### Configuration Options

- **FILE_PATH**: Path to your JSONL chat session file
- **CHUNKSIZE**: Number of sessions to process per chunk (memory optimization)
- **SAMPLE_FRAC**: Fraction of user messages to sample (0.01 = 1%)
- **SMOKE_TEST**: Set to `True` for testing with first chunk only

## 📁 Output Files

The pipeline generates three output files:

### 1. `sampled_queries.parquet`

Detailed dataset with all classified queries including:

- `session_id`: Unique session identifier
- `query`: Original user message
- `intent`: Classified intent (enum)
- `funnel_stage`: Customer journey stage (enum)
- `brand_mentioned`: Detected brand or "none"
- `is_support`: Boolean support flag
- `session_length`: Total messages in session
- `num_user_messages`: User messages in session

### 2. `pipeline_summary.json`

High-level statistics including:

- Total sessions and queries processed
- Intent and funnel stage breakdowns
- Top 20 brand mentions
- Support query statistics
- Session-level metrics (averages, medians)

### 3. `pipeline_output.txt`

Detailed execution logs with:

- Processing progress by chunk
- Sample queries and classifications
- Distribution summaries
- Error messages and warnings

## 🔧 Customization

### Adding New Brands

Edit the `BRANDS` list in `sample_pipeline.py`:

```python
BRANDS = sorted([
    # Your Category
    "your_brand_1", "your_brand_2",
    # ... existing brands
], key=len, reverse=True)
```

### Modifying Intent Classification

Update the `classify_intent()` function with new keywords or patterns:

```python
def classify_intent(query: str) -> Intent:
    # Add your custom logic here
    pass
```

### Adjusting Funnel Logic

Modify the `classify_funnel()` function to change funnel stage assignments:

```python
def classify_funnel(query: str, intent: Intent) -> FunnelStage:
    # Add your custom funnel logic here
    pass
```

## 📈 Performance

- **Memory Efficient**: Processes data in configurable chunks
- **Fast Classification**: Pre-compiled regex patterns for intent detection
- **Scalable**: Handles millions of sessions with 1% sampling
- **Reproducible**: Fixed random seed for consistent sampling

## 🛠️ Development

### Project Structure

```
analysis/
├── sample_pipeline.py          # Main pipeline script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
├── chat_sessions_dec2024.json  # Input data (not in repo)
├── sampled_queries.parquet     # Output data (not in repo)
├── pipeline_summary.json       # Output summary (not in repo)
└── pipeline_output.txt         # Output logs (not in repo)
```

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=sample_pipeline --cov-report=html

# Smoke test (first chunk only)
python sample_pipeline.py

# Full run
# Edit SMOKE_TEST = False in sample_pipeline.py
python sample_pipeline.py
```

## 📊 Output Format

The pipeline generates structured outputs that include:

### Intent Breakdown

- Distribution of queries across 6 intent categories
- Percentage breakdown of each intent type
- Total count of classified queries

### Funnel Stage Breakdown

- Distribution across 4 funnel stages (awareness, consideration, decision, retention)
- Percentage breakdown of each stage
- Total count of funnel-classified queries

### Brand Analysis

- Top 20 most mentioned brands
- Brand mention counts and frequencies
- "none" category for queries without brand mentions

### Support Query Analysis

- Count and percentage of support-related queries
- Support query identification and flagging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For questions or issues:

1. Check the `pipeline_output.txt` for detailed error messages
2. Review the configuration settings
3. Ensure your input data format matches the expected JSONL structure
4. Open an issue on GitHub with sample data and error details

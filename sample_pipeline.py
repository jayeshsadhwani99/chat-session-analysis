import pandas as pd
import json
import re
import logging
from enum import Enum


# ─── CONFIG ────────────────────────────────────────────────────────────────
FILE_PATH    = "./chat_sessions_dec2024.json"  # your JSONL path
CHUNKSIZE    = 100_000                        # adjust for your RAM
SAMPLE_FRAC  = 0.01                           # 1% sampling
SMOKE_TEST   = False                         # set to True for testing with first chunk only
# ────────────────────────────────────────────────────────────────────────────


# ─── ENUMS & CONSTANTS ───────────────────────────────────────────────────────
class Intent(str, Enum):
    """Enumeration for query intents to improve code clarity and maintainability."""
    COMMERCIAL = "commercial"
    PARAPHRASE_EDIT = "paraphrase/edit"
    EDUCATIONAL_QUIZ = "educational/quiz"
    INFORMATIONAL = "informational"
    NAVIGATIONAL = "navigational"
    OTHER = "other"

    def __str__(self):
        return self.value


class FunnelStage(str, Enum):
    """Enumeration for funnel stages to prevent typos and improve consistency."""
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    DECISION = "decision"
    RETENTION = "retention"

    def __str__(self):
        return self.value


# ─── PRE-COMPILED PATTERNS ───────────────────────────────────────────────────
# Pre-compile regex patterns for better performance
QUIZ_PATTERNS = [
    re.compile(r'\b(A|B|C|D)\.', re.IGNORECASE),  # A. B. C. D. options
    re.compile(r'select the correct answer', re.IGNORECASE),
    re.compile(r'which of the following', re.IGNORECASE),
    re.compile(r'what is.*called', re.IGNORECASE),
    re.compile(r'definition of', re.IGNORECASE),
    re.compile(r'what does.*mean', re.IGNORECASE),
    re.compile(r'explain.*concept', re.IGNORECASE),
    re.compile(r'how does.*work', re.IGNORECASE),
    re.compile(r'what is the difference between', re.IGNORECASE)
]

INFO_PATTERNS = [
    re.compile(r'^(how to|how do|how does)\s+', re.IGNORECASE),
    re.compile(r'^(what is|what are|what was|what were)\s+', re.IGNORECASE),
    re.compile(r'^(who is|who are)\s+', re.IGNORECASE),
    re.compile(r'^why\s+', re.IGNORECASE),
    re.compile(r'^where\s+', re.IGNORECASE),
    re.compile(r'^when\s+', re.IGNORECASE),
    re.compile(r'^can you\s+', re.IGNORECASE),
    re.compile(r'^(tell me|give me|show me) about', re.IGNORECASE)
]


# ─── INTENT CLASSIFIER ───────────────────────────────────────────────────────
def classify_intent(query: str) -> Intent:
    """
    Classifies query intent into predefined categories.
    
    Buckets:
      - commercial
      - paraphrase/edit
      - educational/quiz
      - informational
      - navigational
      - other
    """
    if not query or not isinstance(query, str):
        return Intent.OTHER
    
    q = query.lower().strip()

    # Navigational: finding a specific site/page
    navigational_kw = ["go to", "open", "find my", "login", "log in", "dashboard", "account", "settings", "profile"]
    if any(kw in q for kw in navigational_kw):
        return Intent.NAVIGATIONAL

    # commercial
    commercial_kw = ["buy", "purchase", "price", "discount", "deal", "cost", "subscription", "pricing", "upgrade", "license"]
    if any(kw in q for kw in commercial_kw):
        return Intent.COMMERCIAL

    # paraphrase/edit
    paraphrase_triggers = ["reword", "rewrite", "paraphrase", "summarize", "edit", "improve", "make it better", "proofread", "check grammar", "translate"]
    if any(trigger in q for trigger in paraphrase_triggers):
        return Intent.PARAPHRASE_EDIT

    # educational/quiz - using pre-compiled patterns
    if any(pattern.search(q) for pattern in QUIZ_PATTERNS):
        return Intent.EDUCATIONAL_QUIZ

    # informational - using pre-compiled patterns
    if any(pattern.search(q) for pattern in INFO_PATTERNS):
        return Intent.INFORMATIONAL

    # fallback
    return Intent.OTHER

# ─── FUNNEL STAGE ────────────────────────────────────────────────────────────
def classify_funnel(query: str, intent: Intent) -> FunnelStage:
    """
    Maps each query+intent into funnel stages:
      - awareness
      - consideration
      - decision
      - retention
    """
    if not query or not isinstance(query, str):
        return FunnelStage.AWARENESS
    
    q = query.lower()

    # decision: any commercial intent
    if intent == Intent.COMMERCIAL:
        return FunnelStage.DECISION

    # retention: support/troubleshooting keywords or navigational
    if intent == Intent.NAVIGATIONAL:
        return FunnelStage.RETENTION
    support_kw = ["reset", "error", "fix", "help", "forgot", "issue", "problem", "trouble", "broken", "not working"]
    if any(kw in q for kw in support_kw):
        return FunnelStage.RETENTION

    # consideration: comparison or feature research
    compare_kw = [" vs ", "compare", "pros", "cons", "features", "difference", "better", "best", "alternative", "review", "recommendation"]
    if any(kw in q for kw in compare_kw):
        return FunnelStage.CONSIDERATION

    # awareness: for informational and educational queries
    if intent in [Intent.INFORMATIONAL, Intent.EDUCATIONAL_QUIZ]:
        return FunnelStage.AWARENESS

    # default to awareness
    return FunnelStage.AWARENESS

# ─── BRAND/CATEGORY EXTRACTION ───────────────────────────────────────────────
# NOTE: Sorted by length descending to match longer names first (e.g., "google cloud" before "google")
BRANDS = sorted([
    # Global Tech
    "adgent", "google", "microsoft", "apple", "amazon", "facebook", "meta", "twitter", "x", "intel", "samsung", "sony", "ibm", "oracle", "cisco", "dell", "hp", "lenovo", "huawei", "xiaomi", "nvidia", "amd", "arm", "palantir",
    # SaaS & Cloud
    "openai", "chatgpt", "anthropic", "claude", "bard", "slack", "asana", "zoom", "dropbox", "box", "figma", "notion", "monday", "airtable", "shopify", "stripe", "zendesk", "hubspot", "mailchimp", "salesforce", "adobe", "canva", "atlassian", "jira", "confluence", "trello", "datadog", "snowflake", "twilio", "okta", "workday", "service now", "splunk", "tableau", "segment", "intercom", "freshdesk", "zapier", "clickup", "miro", "lucidchart", "github", "gitlab", "bitbucket", "docker", "kubernetes", "heroku", "netlify", "vercel", "aws", "azure", "gcp", "google cloud", "amazon web services",
    # Ecommerce & D2C
    "nike", "tesla", "uber", "airbnb", "netflix", "spotify", "instacart", "doordash", "lyft", "shein", "temu", "alibaba", "aliexpress", "ebay", "walmart", "target", "costco", "best buy", "wayfair", "etsy", "sephora", "glossier", "allbirds", "warby parker", "casper", "peloton", "patagonia", "uniqlo", "zara", "hm", "lulu", "lululemon", "gap", "old navy", "banana republic", "adidas", "reebok", "under armour", "the north face", "columbia",
    # Automotive
    "ford", "toyota", "honda", "bmw", "mercedes", "audi", "volkswagen",
    # Travel & Hospitality
    "expedia", "booking.com", "tripadvisor", "kayak",
    # Food & Beverage
    "mcdonalds", "starbucks", "burger king", "wendys", "kfc", "dominos", "pizza hut", "pepsi", "coca-cola",
    # Media & Entertainment
    "disney", "warner bros", "comcast", "verizon", "at&t", "t-mobile",
    # Financial Services
    "bank of america", "jpmorgan chase", "wells fargo", "citigroup", "goldman sachs", "morgan stanley",
    # Niche/Other
    "duckduckgo", "brave", "vimeo", "soundcloud", "substack", "medium", "quora", "reddit", "pinterest", "tiktok", "snapchat", "discord", "twitch", "kickstarter", "indiegogo", "coursera", "udemy", "khan academy", "duolingo", "robinhood", "coinbase", "binance", "square", "block", "sofi", "chime", "wise", "revolut", "monzo", "n26", "transferwise", "mint", "intuit", "quickbooks", "freshbooks",
], key=len, reverse=True)


def extract_brand(query: str) -> str:
    if not query or not isinstance(query, str):
        return "none"
    
    q = query.lower()
    for b in BRANDS:
        if b in q:
            return b
    return "none"

# ─── SUPPORT FLAG ─────────────────────────────────────────────────────────────
def classify_support(query: str) -> bool:
    """
    True if the query appears to be a support/troubleshooting request.
    """
    if not query or not isinstance(query, str):
        return False
    
    q = query.lower()
    support_kw = ["reset", "error", "fix", "help", "forgot", "issue", "problem", "trouble", "broken", "not working", "support"]
    return any(kw in q for kw in support_kw)

# ─── MAIN PIPELINE ────────────────────────────────────────────────────────────
def main():
    """
    This pipeline samples ~1% of user messages from a JSONL of sessions and classifies them
    by intent, funnel stage, brand mentions, and support flags. It outputs both detailed
    Parquet data and summary statistics.
    """
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('pipeline_output.txt'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    total_sessions = 0
    sampled_chunks = []

    logger.info("Starting pipeline...")
    logger.info(f"Reading from: {FILE_PATH}")
    logger.info(f"Chunk size: {CHUNKSIZE:,}")
    logger.info(f"Sample fraction: {SAMPLE_FRAC*100}%")
    logger.info(f"Smoke test mode: {SMOKE_TEST}")
    logger.info("-" * 50)

    try:
        reader = pd.read_json(FILE_PATH, lines=True, chunksize=CHUNKSIZE)
        for i, sess_chunk in enumerate(reader, start=1):
            total_sessions += len(sess_chunk)

            # Add session-level metadata before exploding
            sess_chunk["session_length"] = sess_chunk["messages"].str.len()
            
            # Count user messages per session
            sess_chunk["num_user_messages"] = sess_chunk["messages"].apply(
                lambda msgs: sum(1 for msg in msgs if msg.get("role") == "user")
            )

            # explode nested messages array
            exploded = sess_chunk.explode("messages")

            # normalize the dicts in 'messages' into columns
            msg_df = pd.json_normalize(exploded["messages"])

            # bring session metadata into the same frame
            msg_df["session_id"] = exploded["id"].values
            msg_df["session_length"] = exploded["session_length"].values
            msg_df["num_user_messages"] = exploded["num_user_messages"].values

            # filter only user messages and rename content→query
            user_df = msg_df[msg_df["role"] == "user"].copy()
            if len(user_df) == 0:
                logger.info(f"--- Chunk {i}: sessions={len(sess_chunk)}, user_msgs=0, sampled=0")
                continue
                
            user_df.rename(columns={"content": "query"}, inplace=True)

            # sample ~1% of user queries
            sampled = user_df.sample(frac=SAMPLE_FRAC, random_state=42)
            logger.info(f"--- Chunk {i}: sessions={len(sess_chunk)}, user_msgs={len(user_df)}, sampled={len(sampled)}")
            
            # Include session metadata in the sampled output
            sampled_chunks.append(sampled[["session_id", "query", "session_length", "num_user_messages"]])

            # smoke-test only first chunk if enabled
            if SMOKE_TEST:
                logger.info("Smoke test mode: stopping after first chunk")
                break

        # concatenate all sampled bits
        if not sampled_chunks:
            logger.error("No data found!")
            return
            
        sample_df = pd.concat(sampled_chunks, ignore_index=True)
        logger.info(f"\nTotal sessions scanned: {total_sessions:,}")
        logger.info(f"Total user queries sampled (~1%): {len(sample_df):,}\n")

        # classify intent
        logger.info("Classifying intents...")
        sample_df["intent"] = sample_df["query"].apply(classify_intent)

        # classify funnel stage
        logger.info("Classifying funnel stages...")
        sample_df["funnel_stage"] = sample_df.apply(
            lambda row: classify_funnel(row["query"], row["intent"]), axis=1
        )

        # extract brand/category mentions
        logger.info("Extracting brand mentions...")
        sample_df["brand_mentioned"] = sample_df["query"].apply(extract_brand)

        # flag support queries
        logger.info("Flagging support queries...")
        sample_df["is_support"] = sample_df["query"].apply(classify_support)

        # show a few examples
        logger.info("\nSample queries (first 5):")
        logger.info(sample_df[["query", "intent", "funnel_stage", "brand_mentioned", "is_support", "session_length", "num_user_messages"]]
              .head().to_string(index=False, max_colwidth=100))

        # show distributions
        logger.info("\nIntent breakdown:")
        intent_counts = sample_df["intent"].value_counts()
        logger.info(intent_counts.to_string())
        logger.info(f"Total: {len(sample_df):,}")

        logger.info("\nFunnel stage breakdown:")
        funnel_counts = sample_df["funnel_stage"].value_counts()
        logger.info(funnel_counts.to_string())
        logger.info(f"Total: {len(sample_df):,}")

        logger.info("\nTop brands mentioned:")
        brand_counts = sample_df["brand_mentioned"].value_counts()
        logger.info(brand_counts.head(10).to_string())
        logger.info(f"Total: {len(sample_df):,}")

        support_count = sample_df['is_support'].sum()
        support_pct = support_count / len(sample_df) * 100
        logger.info(f"\nSupport queries count: {support_count:,} ({support_pct:.1f}%)")

        # save for deeper analysis
        sample_df.to_parquet("sampled_queries.parquet", index=False)
        logger.info("\n➡️ Written sampled_queries.parquet (with session metadata)")
        
        # Save summary statistics
        summary = {
            "total_sessions_scanned": int(total_sessions),
            "total_queries_sampled": int(len(sample_df)),
            "intent_breakdown": {str(k): int(v) for k, v in intent_counts.to_dict().items()},
            "funnel_breakdown": {str(k): int(v) for k, v in funnel_counts.to_dict().items()},
            "brand_breakdown": {k: int(v) for k, v in brand_counts.head(20).to_dict().items()},
            "support_count": int(support_count),
            "support_percentage": round(support_pct, 2),
            "session_metrics": {
                "avg_session_length": float(sample_df["session_length"].mean()),
                "avg_user_messages_per_session": float(sample_df["num_user_messages"].mean()),
                "median_session_length": float(sample_df["session_length"].median()),
                "median_user_messages_per_session": float(sample_df["num_user_messages"].median())
            }
        }
        
        with open("pipeline_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        logger.info("➡️ Written pipeline_summary.json")

    except Exception as e:
        logger.error(f"Error processing data: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()

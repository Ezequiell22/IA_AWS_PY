from typing import List

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def summarize(text: str, sentences: int = 3) -> str:
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary: List[str] = [str(s) for s in summarizer(parser.document, sentences)]
    return "\n".join(summary)
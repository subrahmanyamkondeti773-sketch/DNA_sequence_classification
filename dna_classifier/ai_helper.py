"""
AI Helper - OpenAI Integration for DNA Explanations and Suggestions.
"""
import os
import time
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_openai_client():
    """Create and return an OpenAI client."""
    try:
        from openai import OpenAI
        api_key = settings.OPENAI_API_KEY or os.getenv('OPENAI_API_KEY', '')
        if not api_key:
            return None
        return OpenAI(api_key=api_key)
    except ImportError:
        logger.warning("OpenAI package not installed.")
        return None


def get_ai_explanation(sequence: str, predicted_class: str) -> str:
    """
    Generate a detailed biological explanation for a DNA classification result
    using OpenAI GPT-4o-mini.

    Returns:
        Explanation string (or fallback message if API unavailable)
    """
    client = _get_openai_client()
    if not client:
        return _fallback_explanation(predicted_class)

    short_seq = sequence[:200] + '...' if len(sequence) > 200 else sequence
    prompt = f"""You are a senior molecular biologist and genomics expert.

Analyze this DNA classification result and provide a comprehensive explanation:

DNA Sequence (first 200 chars): {short_seq}
Sequence Length: {len(sequence)} base pairs
Predicted Class: {predicted_class}

Please explain:
1. **Biological Meaning** - What does this DNA class represent biologically?
2. **Possible Gene Type** - What type of gene or regulatory element could this be?
3. **Real-World Significance** - Why does this matter in biology / medicine?
4. **Research Relevance** - How is this used in current genomic research?
5. **Health Implications** - Are there any known health connections?

Keep the explanation scientific yet accessible. Use markdown formatting."""

    try:
        start = time.time()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a molecular biology expert specializing in genomics and DNA analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7,
        )
        elapsed = time.time() - start
        _log_api_call('OpenAI/explanation', 'success', elapsed)
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"OpenAI explanation error: {e}")
        _log_api_call('OpenAI/explanation', 'error', 0, str(e))
        return _fallback_explanation(predicted_class)


def get_ai_suggestions(sequence: str, predicted_class: str) -> str:
    """
    Generate AI suggestions for a classified DNA sequence.

    Returns:
        Suggestions string (or fallback if API unavailable)
    """
    client = _get_openai_client()
    if not client:
        return _fallback_suggestions(predicted_class)

    short_seq = sequence[:200] + '...' if len(sequence) > 200 else sequence
    prompt = f"""As a genomics expert, provide actionable insights for this DNA sequence:

DNA Sequence (first 200 chars): {short_seq}
Predicted Class: {predicted_class}

Provide:
1. **Mutation Insights** - Common mutation sites in this sequence type
2. **Similar Sequences** - What similar sequences exist in genomic databases?
3. **Research Directions** - Suggested next steps for studying this sequence
4. **Clinical Relevance** - Potential diagnostic or therapeutic applications
5. **Experimental Suggestions** - Wet lab experiments that could validate this classification

Use markdown formatting with clear headings."""

    try:
        start = time.time()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a genomics research expert providing scientific recommendations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.7,
        )
        elapsed = time.time() - start
        _log_api_call('OpenAI/suggestions', 'success', elapsed)
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"OpenAI suggestions error: {e}")
        _log_api_call('OpenAI/suggestions', 'error', 0, str(e))
        return _fallback_suggestions(predicted_class)


def _fallback_explanation(predicted_class: str) -> str:
    return f"""## DNA Classification: {predicted_class}

**Note:** AI explanation service is currently unavailable. Here is a general overview:

### Biological Meaning
The sequence has been classified as **{predicted_class}** based on its nucleotide composition and pattern analysis using machine learning models trained on genomic datasets.

### General Information
- DNA sequences are classified based on patterns in their nucleotide arrangement
- The classification reflects the sequence's similarity to known genomic regions
- Further analysis with specialized bioinformatics tools is recommended

### Recommendations
- Cross-reference with NCBI GenBank or Ensembl databases
- Use BLAST alignment to find similar known sequences
- Consult a genomics specialist for clinical interpretation
"""


def _fallback_suggestions(predicted_class: str) -> str:
    return f"""## Research Suggestions for {predicted_class}

**Note:** AI suggestion service is currently unavailable. General recommendations:

### Suggested Actions
1. **Database Search** - Query NCBI, Ensembl, or UCSC Genome Browser
2. **BLAST Analysis** - Run BLASTN to find homologous sequences
3. **Functional Annotation** - Use tools like InterPro or Pfam
4. **Variant Analysis** - Check ClinVar for known variants in this region
5. **Literature Search** - Search PubMed for related genomic studies
"""


def _log_api_call(endpoint: str, status: str, response_time: float, error_msg: str = ''):
    """Log API call to database."""
    try:
        from dna_classifier.models import APILog
        APILog.objects.create(
            endpoint=endpoint,
            status=status,
            response_time=response_time,
            error_message=error_msg
        )
    except Exception as e:
        logger.warning(f"Could not log API call: {e}")

"""
DNA Sequence Predictor - ML Model Loader & Inference Engine.
Loads models once at startup for efficiency (singleton pattern).
"""
import os
import numpy as np
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Global model cache (loaded once)
_PREDICTOR_INSTANCE = None


class DNAPredictor:
    """
    Singleton predictor that loads ML models once and reuses them.
    Converts sequences to k-mers before vectorizing (to match training format).
    """

    def __init__(self):
        self.vectorizer = None
        self.classifier = None
        self.label_encoder = None
        self._loaded = False
        self.kmer_size = 6   # default; auto-detected from vocab
        self._load_models()

    def _load_models(self):
        """Load all three ML models from disk."""
        import joblib
        models_dir = settings.ML_MODELS_DIR

        try:
            vectorizer_path = os.path.join(models_dir, 'vectorizer.pkl')
            classifier_path = os.path.join(models_dir, 'dna_classifier.pkl')
            encoder_path = os.path.join(models_dir, 'label_encoder.pkl')

            self.vectorizer = joblib.load(vectorizer_path)
            self.classifier = joblib.load(classifier_path)
            self.label_encoder = joblib.load(encoder_path)
            self._loaded = True

            # Auto-detect k-mer size from vocabulary keys
            if hasattr(self.vectorizer, 'vocabulary_'):
                sample_key = next(iter(self.vectorizer.vocabulary_.keys()))
                self.kmer_size = len(sample_key)
                logger.info(f"✅ DNA ML models loaded. Detected k-mer size: {self.kmer_size}")
            else:
                logger.info("✅ DNA ML models loaded. Using default k-mer size: 6")

        except FileNotFoundError as e:
            logger.error(f"❌ Model file not found: {e}")
        except Exception as e:
            logger.error(f"❌ Failed to load ML models: {e}")

    def _sequence_to_kmers(self, sequence: str) -> str:
        """
        Convert a DNA sequence to a string of space-separated lowercase k-mers.

        This matches exactly how the TfidfVectorizer was trained.
        Example (k=6):  'ATGCAT' -> 'atgcat tgcata gcatag ...'
        """
        seq = sequence.lower()
        k = self.kmer_size
        if len(seq) < k:
            return seq
        kmers = [seq[i:i+k] for i in range(len(seq) - k + 1)]
        return ' '.join(kmers)

    def predict(self, sequence: str) -> dict:
        """
        Predict the class of a DNA sequence.

        Args:
            sequence: Clean ATGC string (already validated & uppercase)

        Returns:
            dict with keys: label, confidence, probabilities
        """
        if not self._loaded:
            raise RuntimeError("ML models are not loaded. Check model files in the models/ directory.")

        try:
            # ── KEY FIX: convert to lowercase space-separated k-mers ──
            kmer_string = self._sequence_to_kmers(sequence)

            # Vectorize using TfidfVectorizer (trained on kmer strings)
            features = self.vectorizer.transform([kmer_string])

            # Predict class
            prediction = self.classifier.predict(features)
            label = self.label_encoder.inverse_transform(prediction)[0]

            # Confidence probabilities
            if hasattr(self.classifier, 'predict_proba'):
                probabilities = self.classifier.predict_proba(features)[0]
                confidence = float(np.max(probabilities))
                class_labels = self.label_encoder.classes_
                prob_dict = {
                    str(cls): float(prob)
                    for cls, prob in zip(class_labels, probabilities)
                }
            else:
                confidence = 1.0
                prob_dict = {str(label): 1.0}

            return {
                'label': str(label),
                'confidence': confidence,
                'probabilities': prob_dict,
            }

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise


def get_predictor() -> DNAPredictor:
    """Return singleton predictor instance (loaded once, reused)."""
    global _PREDICTOR_INSTANCE
    if _PREDICTOR_INSTANCE is None:
        _PREDICTOR_INSTANCE = DNAPredictor()
    return _PREDICTOR_INSTANCE

import os, sys, warnings
warnings.filterwarnings('ignore')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dna_classification_project.settings'
import django; django.setup()
from dna_classifier.predictor import get_predictor

def run_accuracy_check():
    predictor = get_predictor()
    
    # Test sequences with known labels
    # Using real genomic fragments for verification
    test_data = [
        ("ATGTTTTGCCAACTGGCCAAGACCTGCCCTGTGCAGCTGTGGGTTGATTCCACACCCCCGCCCGGCACCCGCGTCCGCGCCATGGCCATCTACAAGCAGTCACAGCACATGACGGAGGTTGTGAGGCGCTGCCCCCACCATGAGCGCTGCTCAGATAGCGATGGTCTGGCCCCTCCTCAGCATCTTATCCGAGTGGAAGGAAATTTGCGTGTGGAGTATTTGGATGACAGAAACACTTTTCGACATAGTGTGGTGGTGCCCTATGAGCCGCCTGAGGTTGGCTCTGACTGTACCACCATCCACTACAACTACATGTGTAACAGTTCCTGCATGGGCGGCATGAACCGGAGGCCCATCCTCACCATCATCACACTGGAAGACTCCAGTGGTAATCTACTGGGACGGAACAGCTTTGAGGTGCGTGTTTGTGCCTGTCCTGGGAGAGACCGGCGCACAGAGGAAGAGAATCTCCGCAAGAAAGGGGAGCCTCACCACGAGCTGCCCCCAGGGAGCACTAAGCGAGCACTGCCCAACAACACCAGCTCCTCTCCCCAGCCAAAGAAGAAACCACTGGATGGAGAATATTTCACCCTTCAGATCCGTGGGCGTGAGCGCTTCGAGATGTTCCGAGAGCTGAATGAGGCCTTGGAACTCAAGCCGTACTCCCCGGACGAT", "human"),
        ("ATGCAGCAGCCCCGGCAGCAGCAGCAGCAGCAAAGCAAGATCAGCAGCAACAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAG", "chimpanzee"),
        ("ATGGGAATCCCAGAAGGAAAGTCAGCTTGCAAATGGAATGGATTTCCAGCAGTAGCAGCCCAGCCCCCGGAGCCACAGCCCCCAGCCCCAGCCCCAGCACCCAGCACCCGGCCGCAGCACCCGGAGAGCAGCAGAGCCCAGCAAGGCAGCAGCAGCAGCAGCAGATCAAGAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAG", "dog"),
    ]
    
    correct = 0
    total = len(test_data)
    
    print("\n" + "="*60)
    print("          DNA CLASSIFICATION MODEL ACCURACY REPORT")
    print("="*60 + "\n")
    sys.stdout.flush()
    
    for seq, expected in test_data:
        try:
            result = predictor.predict(seq.upper())
            predicted = result['label']
            confidence = result['confidence']
            
            is_correct = predicted.lower() == expected.lower()
            if is_correct:
                correct += 1
                status = "✅ PASS"
            else:
                status = "❌ FAIL"
                
            print(f"Sequence Type: {expected:12s} | Prediction: {predicted:12s} | Conf: {confidence:.4f} | Status: {status}")
            sys.stdout.flush()
        except Exception as e:
            print(f"Error predicting {expected}: {e}")
            sys.stdout.flush()

    accuracy = (correct / total) * 100 if total > 0 else 0
    print("\n" + "-"*60)
    print(f"SUMMARY PERFORMANCE")
    print(f"  Total Verified:  {total}")
    print(f"  Correct:         {correct}")
    print(f"  Accuracy:        {accuracy:.1f}%")
    print("-"*60 + "\n")
    sys.stdout.flush()

if __name__ == "__main__":
    run_accuracy_check()

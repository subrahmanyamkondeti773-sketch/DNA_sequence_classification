import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, ScrollView, Alert, ActivityIndicator } from 'react-native';
import { dnaApi } from '../api';

export default function ClassifyScreen({ navigation }) {
  const [sequence, setSequence] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleClassify = async () => {
    if (!sequence || sequence.trim().length < 10) {
      Alert.alert('Error', 'Please enter a valid DNA sequence (min 10 characters)');
      return;
    }

    setLoading(true);
    setResult(null);
    try {
      const data = await dnaApi.classify(sequence.trim());
      setResult(data);
    } catch (error) {
      console.error(error);
      Alert.alert('Analysis Failed', error.response?.data?.error || 'Server error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>DNA <Text style={styles.primary}>Analyzer</Text></Text>
      <Text style={styles.subtitle}>Enter a sequence to identify its origin</Text>

      <TextInput
        style={styles.input}
        placeholder="Paste DNA sequence (A, T, C, G)..."
        placeholderTextColor="#64748b"
        multiline
        numberOfLines={6}
        value={sequence}
        onChangeText={setSequence}
        autoCapitalize="characters"
      />

      <TouchableOpacity 
        style={styles.button} 
        onPress={handleClassify}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Run ML Analytics</Text>
        )}
      </TouchableOpacity>

      {result && (
        <View style={styles.resultCard}>
          <Text style={styles.resultTitle}>Classification Result</Text>
          <View style={styles.badge}>
            <Text style={styles.badgeText}>{result.prediction.toUpperCase()}</Text>
          </View>
          <Text style={styles.confidence}>Confidence: {result.confidence_percent}</Text>
          
          <Text style={styles.aiTitle}>AI Explanation</Text>
          <Text style={styles.aiText}>{result.ai_explanation}</Text>
          
          <TouchableOpacity 
            style={styles.historyButton}
            onPress={() => navigation.navigate('History')}
          >
            <Text style={styles.historyButtonText}>View in History</Text>
          </TouchableOpacity>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0f1e',
  },
  content: {
    padding: 25,
    paddingTop: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: '800',
    color: '#fff',
  },
  primary: {
    color: '#3b82f6',
  },
  subtitle: {
    fontSize: 15,
    color: '#94a3b8',
    marginTop: 5,
    marginBottom: 30,
  },
  input: {
    backgroundColor: 'rgba(255,255,255,0.05)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.1)',
    borderRadius: 16,
    padding: 15,
    color: '#fff',
    fontSize: 16,
    height: 150,
    textAlignVertical: 'top',
    marginBottom: 20,
    fontFamily: 'monospace',
  },
  button: {
    backgroundColor: '#3b82f6',
    borderRadius: 12,
    padding: 18,
    alignItems: 'center',
    marginBottom: 30,
  },
  buttonText: {
    color: '#fff',
    fontSize: 17,
    fontWeight: '700',
  },
  resultCard: {
    backgroundColor: 'rgba(59, 130, 246, 0.1)',
    borderRadius: 20,
    padding: 25,
    borderWidth: 1,
    borderColor: 'rgba(59, 130, 246, 0.2)',
  },
  resultTitle: {
    color: '#fff',
    fontSize: 20,
    fontWeight: '700',
    marginBottom: 15,
  },
  badge: {
    backgroundColor: '#3b82f6',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 30,
    alignSelf: 'flex-start',
    marginBottom: 10,
  },
  badgeText: {
    color: '#fff',
    fontWeight: '800',
    fontSize: 14,
  },
  confidence: {
    color: '#94a3b8',
    fontSize: 14,
    marginBottom: 20,
  },
  aiTitle: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '700',
    marginTop: 10,
    marginBottom: 10,
  },
  aiText: {
    color: '#cbd5e1',
    lineHeight: 22,
    fontSize: 14,
  },
  historyButton: {
    marginTop: 25,
    borderTopWidth: 1,
    borderTopColor: 'rgba(255,255,255,0.1)',
    paddingTop: 15,
    alignItems: 'center',
  },
  historyButtonText: {
    color: '#3b82f6',
    fontWeight: '600',
  },
});

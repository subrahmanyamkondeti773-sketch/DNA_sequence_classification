import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, RefreshControl, TouchableOpacity, ActivityIndicator } from 'react-native';
import { dnaApi } from '../api';

export default function DashboardScreen({ navigation }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchStats = async () => {
    try {
      const data = await dnaApi.getStats();
      setStats(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchStats();
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#3b82f6" />
      </View>
    );
  }

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#3b82f6" />}
    >
      <View style={styles.header}>
        <Text style={styles.greeting}>Welcome Back! 👋</Text>
        <Text style={styles.subtitle}>DNA Analytics Overview</Text>
      </View>

      <View style={styles.statsRow}>
        <View style={[styles.statCard, { backgroundColor: '#1e3a8a' }]}>
          <Text style={styles.statLabel}>Total</Text>
          <Text style={styles.statValue}>{stats?.total_predictions || 0}</Text>
        </View>
        <View style={[styles.statCard, { backgroundColor: '#065f46' }]}>
          <Text style={styles.statLabel}>Today</Text>
          <Text style={styles.statValue}>{stats?.today_predictions || 0}</Text>
        </View>
      </View>

      <Text style={styles.sectionTitle}>Recent Activity</Text>
      
      {stats?.class_distribution?.length > 0 ? (
        <View style={styles.distributionCard}>
          {stats.class_distribution.map((item, index) => (
            <View key={index} style={styles.distRow}>
              <Text style={styles.distLabel}>{item.prediction}</Text>
              <View style={styles.distBarContainer}>
                <View style={[styles.distBar, { width: `${(item.count / stats.total_predictions) * 100}%` }]} />
              </View>
              <Text style={styles.distCount}>{item.count}</Text>
            </View>
          ))}
        </View>
      ) : (
        <View style={styles.emptyCard}>
          <Text style={styles.emptyText}>No predictions yet. Try classifying a sequence!</Text>
        </View>
      )}

      <TouchableOpacity 
        style={styles.classifyButton}
        onPress={() => navigation.navigate('Classify')}
      >
        <Text style={styles.classifyButtonText}>New Classification 🧬</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0f1e',
    padding: 20,
  },
  center: {
    flex: 1,
    backgroundColor: '#0a0f1e',
    alignItems: 'center',
    justifyContent: 'center',
  },
  header: {
    marginTop: 20,
    marginBottom: 30,
  },
  greeting: {
    fontSize: 28,
    fontWeight: '800',
    color: '#fff',
  },
  subtitle: {
    fontSize: 16,
    color: '#94a3b8',
    marginTop: 5,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 30,
  },
  statCard: {
    width: '48%',
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 5,
    elevation: 5,
  },
  statLabel: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 5,
  },
  statValue: {
    color: '#fff',
    fontSize: 32,
    fontWeight: '800',
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 20,
  },
  distributionCard: {
    backgroundColor: 'rgba(255,255,255,0.05)',
    borderRadius: 16,
    padding: 20,
    marginBottom: 30,
  },
  distRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  distLabel: {
    width: 90,
    color: '#e2e8f0',
    fontSize: 13,
  },
  distBarContainer: {
    flex: 1,
    height: 8,
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: 4,
    marginHorizontal: 10,
  },
  distBar: {
    height: '100%',
    backgroundColor: '#3b82f6',
    borderRadius: 4,
  },
  distCount: {
    color: '#94a3b8',
    fontSize: 13,
    width: 20,
    textAlign: 'right',
  },
  emptyCard: {
    padding: 40,
    alignItems: 'center',
  },
  emptyText: {
    color: '#64748b',
    textAlign: 'center',
    fontSize: 16,
  },
  classifyButton: {
    backgroundColor: '#3b82f6',
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    marginBottom: 50,
  },
  classifyButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '700',
  },
});

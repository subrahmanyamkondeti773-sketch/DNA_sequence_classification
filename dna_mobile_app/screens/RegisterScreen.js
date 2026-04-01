import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, Alert, ActivityIndicator, ScrollView } from 'react-native';
import { authApi } from '../api';

export default function RegisterScreen({ navigation, onRegister }) {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    team_name: '',
  });
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    const { username, email, password, team_name } = formData;
    if (!username || !email || !password || !team_name) {
      Alert.alert('Error', 'Please fill in all required fields (Username, Email, Password, Team Name)');
      return;
    }

    setLoading(true);
    try {
      const data = await authApi.register(formData);
      onRegister(data);
    } catch (error) {
      console.error(error);
      const errorMsg = error.response?.data?.username?.[0] || error.response?.data?.error || 'Registration failed. Please try again.';
      Alert.alert('Registration Failed', errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Create <Text style={styles.primary}>Account</Text></Text>
      <Text style={styles.subtitle}>Join a DNA Team today</Text>

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Username *"
          placeholderTextColor="#94a3b8"
          value={formData.username}
          onChangeText={(val) => setFormData({...formData, username: val})}
          autoCapitalize="none"
        />
        <TextInput
          style={styles.input}
          placeholder="Email *"
          placeholderTextColor="#94a3b8"
          value={formData.email}
          onChangeText={(val) => setFormData({...formData, email: val})}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        <TextInput
          style={styles.input}
          placeholder="Team Name * (e.g., DNA Team A)"
          placeholderTextColor="#94a3b8"
          value={formData.team_name}
          onChangeText={(val) => setFormData({...formData, team_name: val})}
        />
        <View style={styles.row}>
            <TextInput
            style={[styles.input, { flex: 1, marginRight: 10 }]}
            placeholder="First Name"
            placeholderTextColor="#94a3b8"
            value={formData.first_name}
            onChangeText={(val) => setFormData({...formData, first_name: val})}
            />
            <TextInput
            style={[styles.input, { flex: 1 }]}
            placeholder="Last Name"
            placeholderTextColor="#94a3b8"
            value={formData.last_name}
            onChangeText={(val) => setFormData({...formData, last_name: val})}
            />
        </View>
        <TextInput
          style={styles.input}
          placeholder="Password *"
          placeholderTextColor="#94a3b8"
          value={formData.password}
          onChangeText={(val) => setFormData({...formData, password: val})}
          secureTextEntry
        />
      </View>

      <TouchableOpacity 
        style={styles.button} 
        onPress={handleRegister}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Register Now</Text>
        )}
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate('Login')}>
        <Text style={styles.linkText}>Already have an account? <Text style={styles.linkHighlight}>Login</Text></Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0f1e',
  },
  content: {
    padding: 30,
    paddingTop: 60,
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: '800',
    color: '#fff',
  },
  primary: {
    color: '#3b82f6',
  },
  subtitle: {
    fontSize: 16,
    color: '#94a3b8',
    marginBottom: 40,
  },
  inputContainer: {
    width: '100%',
    marginBottom: 20,
  },
  input: {
    width: '100%',
    backgroundColor: 'rgba(255,255,255,0.05)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.1)',
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
    color: '#fff',
    fontSize: 16,
  },
  row: {
    flexDirection: 'row',
    width: '100%',
  },
  button: {
    width: '100%',
    backgroundColor: '#3b82f6',
    borderRadius: 12,
    padding: 18,
    alignItems: 'center',
    marginBottom: 20,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '700',
  },
  linkText: {
    color: '#94a3b8',
    marginTop: 10,
    marginBottom: 50,
  },
  linkHighlight: {
    color: '#3b82f6',
    fontWeight: '600',
  },
});

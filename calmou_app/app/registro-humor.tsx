// app/registro-humor.tsx

import React, { useState } from 'react';
import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity, TextInput, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import LottieView from 'lottie-react-native';

// ===== CAMINHO CORRIGIDO AQUI (../ em vez de ../../) =====
const HUMOR_OPTIONS = [
  { level: 1, animation: require('../assets/animations/stressed.json'), label: 'Estressado' },
  { level: 2, animation: require('../assets/animations/sad.json'), label: 'Mal' },
  { level: 3, animation: require('../assets/animations/neutral.json'), label: 'Normal' },
  { level: 4, animation: require('../assets/animations/happy.json'), label: 'Bem' },
  { level: 5, animation: require('../assets/animations/very-happy.json'), label: 'Ótimo' },
];
// =======================================================

export default function RegistroHumorScreen() {
  // (O resto do código continua o mesmo, não precisa mudar nada)
  const router = useRouter();
  const [humorSelecionado, setHumorSelecionado] = useState<number | null>(null);
  const [notas, setNotas] = useState('');

  const handleSalvar = () => {
    if (humorSelecionado === null) {
      Alert.alert("Atenção", "Por favor, selecione como você está se sentindo.");
      return;
    }
    console.log({ humor: humorSelecionado, notas });
    Alert.alert("Salvo!", "Seu humor foi registrado com sucesso.", [
        { text: "OK", onPress: () => router.back() }
    ]);
  };

  return (
    <SafeAreaView style={styles.container}>
      <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
        <Ionicons name="arrow-back" size={24} color="#333" />
      </TouchableOpacity>

      <Text style={styles.title}>Como você está se sentindo agora?</Text>

      <View style={styles.humorContainer}>
        {HUMOR_OPTIONS.map((option) => {
          const isSelected = humorSelecionado === option.level;
          return (
            <TouchableOpacity 
              key={option.level} 
              style={[styles.emojiButton, isSelected && styles.emojiButtonSelected]}
              onPress={() => setHumorSelecionado(option.level)}
            >
              <LottieView
                source={option.animation}
                autoPlay={isSelected}
                loop={isSelected}
                style={styles.lottieAnimation}
              />
              <Text style={[styles.emojiLabel, isSelected && styles.emojiLabelSelected]}>{option.label}</Text>
            </TouchableOpacity>
          );
        })}
      </View>

      <Text style={styles.notasTitle}>Notas sobre seu dia (opcional)</Text>
      <TextInput
        style={styles.textInput}
        multiline
        placeholder="O que aconteceu hoje? Como isso te afetou?"
        value={notas}
        onChangeText={setNotas}
      />

      <TouchableOpacity style={styles.saveButton} onPress={handleSalvar}>
        <Text style={styles.saveButtonText}>Salvar Registro</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

// (Os estilos são os mesmos)
const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f5f5f5', padding: 20, paddingTop: 60 },
    backButton: { position: 'absolute', top: 50, left: 20, zIndex: 1, },
    title: { fontSize: 26, fontWeight: 'bold', textAlign: 'center', marginBottom: 30 },
    humorContainer: { flexDirection: 'row', justifyContent: 'space-around', alignItems: 'flex-start', marginBottom: 40 },
    emojiButton: { alignItems: 'center', padding: 5, borderRadius: 15, borderWidth: 2, borderColor: 'transparent', width: 70, },
    emojiButtonSelected: { backgroundColor: '#0a7ea420', borderColor: '#0a7ea4' },
    lottieAnimation: { width: 60, height: 60, },
    emojiLabel: { marginTop: 8, color: 'gray', fontSize: 12, fontWeight: '500' },
    emojiLabelSelected: { color: '#0a7ea4', fontWeight: 'bold' },
    notasTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
    textInput: { backgroundColor: 'white', height: 120, borderRadius: 10, padding: 15, textAlignVertical: 'top', fontSize: 16, marginBottom: 30, elevation: 2, shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 5, },
    saveButton: { backgroundColor: '#0a7ea4', padding: 20, borderRadius: 10, alignItems: 'center', elevation: 3, shadowColor: '#000', shadowOpacity: 0.1, shadowRadius: 10, },
    saveButtonText: { color: 'white', fontSize: 18, fontWeight: 'bold' },
});
// app/(tabs)/avaliacoes.tsx --- VERSÃO CORRIGIDA

import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity, FlatList } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router'; // 1. IMPORTE O useRouter

const MOCK_AVALIACOES = [
  { id: 'stress', titulo: 'Teste de Nível de Estresse', descricao: 'Avalie seus níveis de estresse com este questionário rápido.', cor: '#FF6347', icone: 'pulse-outline', },
  { id: 'burnout', titulo: 'Questionário de Prevenção ao Burnout', descricao: 'Identifique sinais precoces de esgotamento profissional.', cor: '#4682B4', icone: 'flame-outline', },
  { id: 'ansiedade', titulo: 'Escala de Ansiedade (GAD-7)', descricao: 'Um questionário validado para medir seus sintomas de ansiedade.', cor: '#32CD32', icone: 'help-buoy-outline', },
];

const AvaliacaoCard = ({ item }) => {
    const router = useRouter(); // 2. PEGUE A FUNÇÃO DE NAVEGAÇÃO

    return (
        // 3. USE UM TouchableOpacity NORMAL e chame a navegação no onPress
        <TouchableOpacity 
            style={[styles.card, { borderLeftColor: item.cor }]}
            onPress={() => router.push(`/avaliacao/${item.id}`)}
        >
            <View style={styles.iconContainer}>
                <Ionicons name={item.icone} size={32} color={item.cor} />
            </View>
            <View style={styles.textContainer}>
                <Text style={styles.cardTitle}>{item.titulo}</Text>
                <Text style={styles.cardDescription}>{item.descricao}</Text>
            </View>
        </TouchableOpacity>
    );
};

export default function AvaliacoesScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Autoavaliação</Text>
      <Text style={styles.subtitle}>Ferramentas para entender seu bem-estar</Text>
      <FlatList
        data={MOCK_AVALIACOES}
        renderItem={({ item }) => <AvaliacaoCard item={item} />}
        keyExtractor={(item) => item.id}
        contentContainerStyle={{ paddingHorizontal: 20, paddingTop: 20 }}
      />
    </SafeAreaView>
  );
}

// (Os estilos continuam os mesmos)
const styles = StyleSheet.create({ container: { flex: 1, backgroundColor: '#f5f5f5', }, title: { fontSize: 28, fontWeight: 'bold', textAlign: 'center', marginTop: 40, marginBottom: 10, }, subtitle: { fontSize: 16, color: 'gray', textAlign: 'center', marginBottom: 20, paddingHorizontal: 40, }, card: { backgroundColor: '#fff', borderRadius: 10, padding: 20, marginBottom: 20, flexDirection: 'row', alignItems: 'center', borderLeftWidth: 5, shadowColor: "#000", shadowOffset: { width: 0, height: 2, }, shadowOpacity: 0.1, shadowRadius: 3.84, elevation: 5, }, iconContainer: { marginRight: 20, }, textContainer: { flex: 1, }, cardTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 5, }, cardDescription: { fontSize: 14, color: '#666', lineHeight: 20, }, });
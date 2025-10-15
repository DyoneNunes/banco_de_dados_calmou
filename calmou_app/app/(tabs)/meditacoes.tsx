// app/(tabs)/meditacoes.tsx --- VERSÃO CORRIGIDA

import React from 'react';
import { View, Text, FlatList, StyleSheet, SafeAreaView, TouchableOpacity, Image } from 'react-native';
import { useRouter } from 'expo-router'; // 1. IMPORTE O useRouter

const MOCK_MEDITACOES = [
    { id: 1, titulo: 'Respiração para Foco', categoria: 'Respiração', duracao_minutos: 5, imagem_capa: 'https://images.pexels.com/photos/3998365/pexels-photo-3998365.png' },
    { id: 2, titulo: 'Meditação para Dormir', categoria: 'Sono', duracao_minutos: 15, imagem_capa: 'https://images.pexels.com/photos/7194915/pexels-photo-7194915.jpeg' },
    { id: 3, titulo: 'Atenção Plena para Iniciantes', categoria: 'Mindfulness', duracao_minutos: 10, imagem_capa: 'https://images.pexels.com/photos/3094215/pexels-photo-3094215.jpeg' },
    { id: 4, titulo: 'Relaxamento Profundo', categoria: 'Relaxamento', duracao_minutos: 20, imagem_capa: 'https://images.pexels.com/photos/1051838/pexels-photo-1051838.jpeg' },
];

const MeditacaoCard = ({ item }) => {
    const router = useRouter(); // 2. PEGUE A FUNÇÃO DE NAVEGAÇÃO

    return (
        // 3. USE UM TouchableOpacity NORMAL e chame a navegação no onPress
        <TouchableOpacity 
            style={styles.card} 
            onPress={() => router.push(`/meditacao/${item.id}`)}
        >
            <Image source={{ uri: item.imagem_capa }} style={styles.cardImage} />
            <View style={styles.cardContent}>
                <Text style={styles.cardTitle}>{item.titulo}</Text>
                <Text style={styles.cardSubtitle}>{item.categoria} • {item.duracao_minutos} min</Text>
            </View>
        </TouchableOpacity>
    );
};

export default function MeditacoesScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Meditar</Text>
      <FlatList
        data={MOCK_MEDITACOES}
        renderItem={({ item }) => <MeditacaoCard item={item} />}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={{ paddingHorizontal: 20 }}
      />
    </SafeAreaView>
  );
}

// (Os estilos continuam os mesmos)
const styles = StyleSheet.create({ container: { flex: 1, backgroundColor: '#f5f5f5' }, title: { fontSize: 28, fontWeight: 'bold', marginVertical: 20, textAlign: 'center', paddingTop: 20, }, card: { backgroundColor: '#fff', borderRadius: 12, marginBottom: 20, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 8, elevation: 5, }, cardImage: { width: '100%', height: 150, borderTopLeftRadius: 12, borderTopRightRadius: 12, }, cardContent: { padding: 15 }, cardTitle: { fontSize: 18, fontWeight: 'bold' }, cardSubtitle: { fontSize: 14, color: 'gray', marginTop: 5 }, });
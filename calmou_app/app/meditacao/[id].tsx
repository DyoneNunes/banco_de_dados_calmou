// app/meditacao/[id].tsx

import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, Image, TouchableOpacity, ScrollView } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

const MOCK_MEDITACOES = [
    { id: 1, titulo: 'Respiração para Foco', categoria: 'Respiração', duracao_minutos: 5, imagem_capa: 'https://images.pexels.com/photos/3998365/pexels-photo-3998365.png' },
    { id: 2, titulo: 'Meditação para Dormir', categoria: 'Sono', duracao_minutos: 15, imagem_capa: 'https://images.pexels.com/photos/7194915/pexels-photo-7194915.jpeg' },
    { id: 3, titulo: 'Atenção Plena para Iniciantes', categoria: 'Mindfulness', duracao_minutos: 10, imagem_capa: 'https://images.pexels.com/photos/3094215/pexels-photo-3094215.jpeg' },
    { id: 4, titulo: 'Relaxamento Profundo', categoria: 'Relaxamento', duracao_minutos: 20, imagem_capa: 'https://images.pexels.com/photos/1051838/pexels-photo-1051838.jpeg' },
];

export default function MeditacaoDetalheScreen() {
    const { id } = useLocalSearchParams(); // Pega o 'id' da URL
    const router = useRouter();

    const meditacao = MOCK_MEDITACOES.find(m => m.id.toString() === id);

    if (!meditacao) {
        return (
            <SafeAreaView style={styles.container}><Text>Meditação não encontrada</Text></SafeAreaView>
        );
    }

    return (
        <View style={styles.container}>
            <ScrollView>
                <Image source={{ uri: meditacao.imagem_capa }} style={styles.headerImage} />

                <View style={styles.content}>
                    <Text style={styles.title}>{meditacao.titulo}</Text>
                    <Text style={styles.subtitle}>{meditacao.categoria} • {meditacao.duracao_minutos} min</Text>
                    <Text style={styles.description}>
                        Relaxe e encontre a calma com esta sessão guiada. Prepare-se para uma jornada de autoconhecimento e paz interior. Feche os olhos, respire fundo e permita-se estar presente no momento.
                        {"\n\n"}
                        Esta prática é ideal para reduzir o estresse e a ansiedade, melhorando sua concentração e bem-estar geral.
                    </Text>
                </View>
            </ScrollView>

            <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
                <Ionicons name="arrow-back" size={24} color="white" />
            </TouchableOpacity>

            <TouchableOpacity style={styles.playButton}>
                <Ionicons name="play" size={32} color="white" />
            </TouchableOpacity>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f5f5f5' },
    headerImage: { width: '100%', height: 300, },
    backButton: { position: 'absolute', top: 50, left: 20, backgroundColor: 'rgba(0, 0, 0, 0.5)', padding: 8, borderRadius: 20, },
    content: { padding: 20, marginTop: -30, backgroundColor: '#f5f5f5', borderTopLeftRadius: 30, borderTopRightRadius: 30, },
    title: { fontSize: 28, fontWeight: 'bold', marginBottom: 8, },
    subtitle: { fontSize: 16, color: 'gray', marginBottom: 20, },
    description: { fontSize: 16, lineHeight: 24, color: '#333', },
    playButton: { position: 'absolute', bottom: 40, right: 30, backgroundColor: '#0a7ea4', width: 70, height: 70, borderRadius: 35, justifyContent: 'center', alignItems: 'center', elevation: 8, shadowColor: '#000', shadowOpacity: 0.3, shadowRadius: 8, },
});
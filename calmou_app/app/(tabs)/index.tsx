// app/(tabs)/index.tsx

import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity, ScrollView, Image } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Link } from 'expo-router';

// Dados de mentira para as sugestões
const MOCK_SUGESTOES = [
    { id: 1, titulo: 'Respiração para Foco', categoria: 'Respiração', imagem_capa: 'https://images.pexels.com/photos/3998365/pexels-photo-3998365.png' },
    { id: 3, titulo: 'Atenção Plena', categoria: 'Mindfulness', imagem_capa: 'https://images.pexels.com/photos/3094215/pexels-photo-3094215.jpeg' },
    { id: 4, titulo: 'Relaxamento Profundo', categoria: 'Relaxamento', imagem_capa: 'https://images.pexels.com/photos/1051838/pexels-photo-1051838.jpeg' },
];

export default function DashboardScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        {/* Saudação */}
        <View style={styles.header}>
          <Text style={styles.saudacao}>Olá, Dyone 👋</Text>
          <Text style={styles.subsaudacao}>Como você está se sentindo hoje?</Text>
        </View>

        {/* Card Principal - Registro de Humor */}
        <Link href="/registro-humor" asChild>
          <TouchableOpacity style={styles.cardPrincipal}>
            <View>
              <Text style={styles.cardPrincipalTitulo}>Registro Diário</Text>
              <Text style={styles.cardPrincipalTexto}>Toque aqui para registrar seu humor e suas emoções do dia.</Text>
            </View>
            <Ionicons name="arrow-forward-circle" size={32} color="#0a7ea4" />
          </TouchableOpacity>
        </Link>

        {/* Gráfico Semanal (Placeholder) */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Sua Jornada Semanal</Text>
          <View style={styles.graficoPlaceholder}>
            <Text style={styles.graficoTexto}>Gráfico de Humor da Semana</Text>
          </View>
        </View>

        {/* Sugestões */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Sugestões para Você</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            {MOCK_SUGESTOES.map((item) => (
              <Link key={item.id} href={`/meditacao/${item.id}`} asChild>
                <TouchableOpacity style={styles.sugestaoCard}>
                  <Image source={{ uri: item.imagem_capa }} style={styles.sugestaoImagem} />
                  <Text style={styles.sugestaoTitulo}>{item.titulo}</Text>
                </TouchableOpacity>
              </Link>
            ))}
          </ScrollView>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  header: { paddingHorizontal: 20, paddingTop: 40, paddingBottom: 20 },
  saudacao: { fontSize: 28, fontWeight: 'bold' },
  subsaudacao: { fontSize: 16, color: 'gray', marginTop: 4 },
  cardPrincipal: {
    backgroundColor: '#e0f7fa',
    marginHorizontal: 20,
    borderRadius: 15,
    padding: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 10,
  },
  cardPrincipalTitulo: { fontSize: 18, fontWeight: 'bold', color: '#004d40' },
  cardPrincipalTexto: { fontSize: 14, color: '#00796b', marginTop: 4, marginRight: 10 },
  section: { marginTop: 30, paddingLeft: 20 },
  sectionTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 15 },
  graficoPlaceholder: { height: 150, backgroundColor: 'white', marginRight: 20, borderRadius: 10, justifyContent: 'center', alignItems: 'center', elevation: 2 },
  graficoTexto: { color: '#ccc', fontSize: 16 },
  sugestaoCard: { backgroundColor: 'white', borderRadius: 10, width: 150, marginRight: 15, elevation: 2, shadowColor: '#000', shadowOpacity: 0.05, shadowRadius: 5, },
  sugestaoImagem: { width: '100%', height: 100, borderTopLeftRadius: 10, borderTopRightRadius: 10 },
  sugestaoTitulo: { padding: 10, fontWeight: 'bold' },
});
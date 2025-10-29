// app/(tabs)/historico.tsx

import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from 'expo-router';
import React, { useCallback, useState } from 'react';
import { ActivityIndicator, FlatList, SafeAreaView, StyleSheet, Text, View } from 'react-native';
import { useAuth } from '../../src/context/AuthContext';
import api from '../../src/services/api';

// --- CORREÇÃO DE TIPAGEM ---

// 1. Pega o tipo exato dos nomes de ícones do Ionicons
type IoniconName = React.ComponentProps<typeof Ionicons>['name'];

// 2. Define a "forma" dos dados que virão da API
type Avaliacao = {
  tipo: string; // O tipo que vem do backend
  score: number;
  resultado: string;
  data: string;
};

// 3. Define um tipo para nosso objeto de ícones
type AvaliacaoIconMap = {
  [key: string]: {
    icone: IoniconName; // Garante que o ícone é um nome válido
    cor: string;
  };
};

// 4. Cria o objeto de mapeamento
const AVALIACAO_ICONS: AvaliacaoIconMap = {
  'Avaliação de Estresse': { icone: 'pulse-outline', cor: '#FF6347' },
  'Questionário de Burnout': { icone: 'flame-outline', cor: '#4682B4' },
  'Escala de Ansiedade': { icone: 'help-buoy-outline', cor: '#32CD32' },
};

// --- FIM DA CORREÇÃO ---


export default function HistoricoScreen() {
  const { authState } = useAuth();
  const [historico, setHistorico] = useState<Avaliacao[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchHistorico = () => {
    if (authState.user?.id) {
      setLoading(true);
      // O endpoint requer JWT e não precisa do ID na URL
      api.get('/avaliacoes/historico')
        .then(response => {
          setHistorico(response.data);
        })
        .catch(err => {
          console.error("Erro ao buscar histórico:", err);
        })
        .finally(() => {
          setLoading(false);
        });
    }
  };

  useFocusEffect(
    useCallback(() => {
      fetchHistorico();
    }, [authState.user])
  );

  if (loading) {
    return <ActivityIndicator size="large" style={styles.container} />;
  }

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Histórico de Avaliações</Text>
      {historico.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyText}>Você ainda não completou nenhuma avaliação.</Text>
        </View>
      ) : (
        <FlatList
          data={historico}
          keyExtractor={(item, index) => `${item.tipo}-${index}`}
          renderItem={({ item }) => {
            const iconInfo = AVALIACAO_ICONS[item.tipo] || { icone: 'help-circle-outline', cor: '#ccc' };
            return (
                <View style={styles.card}>
                <Ionicons name={iconInfo.icone} size={24} color={iconInfo.cor} />
                <View style={styles.cardContent}>
                    <Text style={styles.cardTitle}>{item.tipo}</Text>
                    <Text style={styles.cardSubtitle}>Resultado: {item.resultado} (Pontuação: {item.score})</Text>
                </View>
                <Text style={styles.cardDate}>{item.data}</Text>
                </View>
            );
          }}
          contentContainerStyle={{ paddingHorizontal: 20 }}
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5', justifyContent: 'center' },
  title: { fontSize: 28, fontWeight: 'bold', textAlign: 'center', marginTop: 40, marginBottom: 20 },
  emptyContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  emptyText: { fontSize: 16, color: 'gray' },
  card: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 20,
    marginBottom: 15,
    flexDirection: 'row',
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  cardContent: { flex: 1, marginLeft: 15 },
  cardTitle: { fontSize: 16, fontWeight: 'bold' },
  cardSubtitle: { fontSize: 14, color: '#666', marginTop: 4 },
  cardDate: { fontSize: 12, color: 'gray' },
});

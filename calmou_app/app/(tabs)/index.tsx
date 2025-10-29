import { Ionicons } from '@expo/vector-icons';
import { Link, useFocusEffect } from 'expo-router';
import React, { useCallback, useState } from 'react';
import {
  ActivityIndicator,
  Image,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import GraficoHumor from '../../src/components/GraficoHumor';
import { useAuth } from '../../src/context/AuthContext';
import api from '../../src/services/api';

type Sugestao = {
  id: number;
  titulo: string;
  categoria: string;
  imagem_capa: string;
};

type RelatorioHumorItem = {
  data: string;
  nivel: number;
};

type DadosGrafico = {
  labels: string[];
  datasets: { data: number[] }[];
};

export default function DashboardScreen() {
  const { authState } = useAuth();
  const [sugestoes, setSugestoes] = useState<Sugestao[]>([]);
  const [dadosGrafico, setDadosGrafico] = useState<DadosGrafico | null>(null);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useFocusEffect(
    useCallback(() => {
      let isMounted = true;

      const fetchData = async () => {
        if (!isMounted) return;
        
        setLoading(true);
        setErro(null);
        
        try {
          // Buscar sugestões
          const sugestoesResponse = await api.get('/meditacoes');
          if (isMounted) {
            setSugestoes(sugestoesResponse.data);
          }

          // Buscar dados do gráfico apenas se houver usuário
          if (authState.user?.id) {
            // O endpoint requer JWT e não precisa do ID na URL
            const graficoResponse = await api.get('/humor/relatorio-semanal');
            
            if (isMounted) {
              if (graficoResponse.data && graficoResponse.data.length > 0) {
                const labels = graficoResponse.data.map(
                  (item: RelatorioHumorItem) => item.data
                );
                const dataPoints = graficoResponse.data.map(
                  (item: RelatorioHumorItem) => item.nivel
                );
                
                setDadosGrafico({
                  labels,
                  datasets: [{ data: dataPoints }],
                });
              } else {
                setDadosGrafico({ labels: [], datasets: [{ data: [] }] });
              }
            }
          } else {
            if (isMounted) {
              setDadosGrafico({ labels: [], datasets: [{ data: [] }] });
            }
          }
        } catch (error) {
          console.error("Erro ao buscar dados do dashboard:", error);
          if (isMounted) {
            setErro("Não foi possível carregar os dados. Tente novamente.");
            setDadosGrafico({ labels: [], datasets: [{ data: [] }] });
          }
        } finally {
          if (isMounted) {
            setLoading(false);
          }
        }
      };

      fetchData();

      // Cleanup
      return () => {
        isMounted = false;
      };
    }, [authState.user?.id])
  );

  const handleRetry = () => {
    setLoading(true);
    setErro(null);
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Saudação Dinâmica */}
        <View style={styles.header}>
          <Text style={styles.saudacao}>
            Olá, {authState.user?.nome?.split(' ')[0] || 'Visitante'} 👋
          </Text>
          <Text style={styles.subsaudacao}>
            Como você está se sentindo hoje?
          </Text>
        </View>

        {/* Card Principal - Registro de Humor */}
        <Link href="/registro-humor" asChild>
          <TouchableOpacity 
            style={styles.cardPrincipal}
            accessibilityLabel="Registrar humor diário"
            accessibilityRole="button"
            activeOpacity={0.7}
          >
            <View style={styles.cardPrincipalContent}>
              <Text style={styles.cardPrincipalTitulo}>Registro Diário</Text>
              <Text style={styles.cardPrincipalTexto}>
                Toque aqui para registrar seu humor e suas emoções do dia.
              </Text>
            </View>
            <Ionicons name="arrow-forward-circle" size={32} color="#0a7ea4" />
          </TouchableOpacity>
        </Link>

        {/* Mensagem de Erro Global */}
        {erro && (
          <View style={styles.erroContainer}>
            <View style={styles.erroContent}>
              <Ionicons name="alert-circle" size={24} color="#c62828" />
              <Text style={styles.erroTexto}>{erro}</Text>
            </View>
            <TouchableOpacity 
              style={styles.retryButton}
              onPress={handleRetry}
            >
              <Text style={styles.retryButtonText}>Tentar Novamente</Text>
            </TouchableOpacity>
          </View>
        )}

        {/* Gráfico Semanal */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Sua Jornada Semanal</Text>
          {loading ? (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="#0a7ea4" />
              <Text style={styles.loadingText}>Carregando...</Text>
            </View>
          ) : dadosGrafico && dadosGrafico.labels.length > 0 ? (
            <GraficoHumor data={dadosGrafico} />
          ) : (
            <View style={styles.emptyState}>
              <Ionicons name="bar-chart-outline" size={48} color="#ccc" />
              <Text style={styles.emptyStateTitle}>
                Comece sua jornada
              </Text>
              <Text style={styles.emptyStateTexto}>
                Registre seu humor diariamente para visualizar seu progresso
              </Text>
            </View>
          )}
        </View>

        {/* Sugestões */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Sugestões para Você</Text>
            {sugestoes.length > 0 && (
              <Text style={styles.sectionSubtitle}>
                {sugestoes.length} {sugestoes.length === 1 ? 'item' : 'itens'}
              </Text>
            )}
          </View>
          
          {loading ? (
            <View style={styles.loadingContainerSmall}>
              <ActivityIndicator size="small" color="#0a7ea4" />
            </View>
          ) : sugestoes.length > 0 ? (
            <ScrollView 
              horizontal 
              showsHorizontalScrollIndicator={false}
              contentContainerStyle={styles.sugestoesContainer}
            >
              {sugestoes.map((item) => (
                <Link key={item.id} href={`/meditacao/${item.id}`} asChild>
                  <TouchableOpacity 
                    style={styles.sugestaoCard}
                    accessibilityLabel={`Meditação: ${item.titulo}`}
                    activeOpacity={0.8}
                  >
                    <Image 
                      source={{ uri: item.imagem_capa }} 
                      style={styles.sugestaoImagem}
                      accessibilityRole="image"
                      resizeMode="cover"
                    />
                    <View style={styles.sugestaoContent}>
                      <Text 
                        style={styles.sugestaoTitulo}
                        numberOfLines={2}
                      >
                        {item.titulo}
                      </Text>
                      <View style={styles.sugestaoBadge}>
                        <Text style={styles.sugestaoBadgeText}>
                          {item.categoria}
                        </Text>
                      </View>
                    </View>
                  </TouchableOpacity>
                </Link>
              ))}
            </ScrollView>
          ) : (
            <View style={styles.emptyState}>
              <Ionicons name="headset-outline" size={48} color="#ccc" />
              <Text style={styles.emptyStateTexto}>
                Nenhuma sugestão disponível no momento
              </Text>
            </View>
          )}
        </View>

        {/* Espaçamento inferior */}
        <View style={styles.bottomSpacer} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    backgroundColor: '#f5f5f5' 
  },
  header: { 
    paddingHorizontal: 20, 
    paddingTop: 20, 
    paddingBottom: 20 
  },
  saudacao: { 
    fontSize: 28, 
    fontWeight: 'bold',
    color: '#1a1a1a'
  },
  subsaudacao: { 
    fontSize: 16, 
    color: '#666', 
    marginTop: 4 
  },
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
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  cardPrincipalContent: {
    flex: 1,
    marginRight: 12
  },
  cardPrincipalTitulo: { 
    fontSize: 18, 
    fontWeight: 'bold', 
    color: '#004d40' 
  },
  cardPrincipalTexto: { 
    fontSize: 14, 
    color: '#00796b', 
    marginTop: 4,
    lineHeight: 20
  },
  section: { 
    marginTop: 30, 
    paddingLeft: 20 
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingRight: 20,
    marginBottom: 15
  },
  sectionTitle: { 
    fontSize: 20, 
    fontWeight: 'bold',
    color: '#1a1a1a'
  },
  sectionSubtitle: {
    fontSize: 14,
    color: '#666'
  },
  sugestoesContainer: {
    paddingRight: 20
  },
  sugestaoCard: { 
    backgroundColor: 'white', 
    borderRadius: 12, 
    width: 160, 
    marginRight: 15, 
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    overflow: 'hidden'
  },
  sugestaoImagem: { 
    width: '100%', 
    height: 120,
    backgroundColor: '#e0e0e0'
  },
  sugestaoContent: {
    padding: 12
  },
  sugestaoTitulo: { 
    fontWeight: 'bold',
    fontSize: 14,
    color: '#1a1a1a',
    lineHeight: 18
  },
  sugestaoBadge: {
    marginTop: 8,
    paddingHorizontal: 8,
    paddingVertical: 4,
    backgroundColor: '#e3f2fd',
    borderRadius: 6,
    alignSelf: 'flex-start'
  },
  sugestaoBadgeText: {
    fontSize: 11,
    color: '#0a7ea4',
    fontWeight: '600'
  },
  erroContainer: { 
    backgroundColor: '#ffebee', 
    marginHorizontal: 20, 
    marginTop: 15, 
    padding: 16, 
    borderRadius: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#c62828'
  },
  erroContent: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12
  },
  erroTexto: { 
    color: '#c62828', 
    fontSize: 14,
    marginLeft: 12,
    flex: 1,
    lineHeight: 20
  },
  retryButton: {
    backgroundColor: '#c62828',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
    alignSelf: 'flex-start'
  },
  retryButtonText: {
    color: 'white',
    fontWeight: '600',
    fontSize: 14
  },
  emptyState: { 
    padding: 30, 
    backgroundColor: 'white', 
    marginRight: 20, 
    borderRadius: 12, 
    alignItems: 'center',
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
  },
  emptyStateTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginTop: 12,
    marginBottom: 4
  },
  emptyStateTexto: { 
    color: '#666', 
    textAlign: 'center', 
    fontSize: 14,
    lineHeight: 20
  },
  loadingContainer: {
    height: 200,
    backgroundColor: 'white',
    marginRight: 20,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center'
  },
  loadingContainerSmall: {
    height: 100,
    justifyContent: 'center',
    alignItems: 'center'
  },
  loadingText: {
    marginTop: 12,
    color: '#666',
    fontSize: 14
  },
  bottomSpacer: {
    height: 30
  }
});
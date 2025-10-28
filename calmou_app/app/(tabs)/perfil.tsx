import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect, useRouter } from 'expo-router';
import React, { useCallback, useState } from 'react';
import { ActivityIndicator, Image, SafeAreaView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useAuth } from '../../src/context/AuthContext';
import api from '../../src/services/api';

interface PerfilData {
    nome: string;
    email: string;
    data_nascimento: string;
    tipo_sanguineo?: string;
    alergias?: string;
    foto_perfil?: string | null;
}

// Função para calcular a idade
const calcularIdade = (dataNasc: string): number => {
    if (!dataNasc) return 0;
    const hoje = new Date();
    const nascimento = new Date(dataNasc);
    let idade = hoje.getFullYear() - nascimento.getFullYear();
    const m = hoje.getMonth() - nascimento.getMonth();
    if (m < 0 || (m === 0 && hoje.getDate() < nascimento.getDate())) {
        idade--;
    }
    return idade;
};

export default function PerfilScreen() {
    const { authState, signOut } = useAuth();
    const router = useRouter();
    const [perfil, setPerfil] = useState<PerfilData | null>(null);
    const [loading, setLoading] = useState(true);

    const fetchProfile = () => {
        if (authState.user?.id) {
            setLoading(true);
            api.get(`/usuarios/${authState.user.id}`)
                .then(response => {
                    console.log('✅ Perfil carregado:', response.data);
                    console.log('📸 Foto do perfil:', response.data.foto_perfil ? 'Presente' : 'Ausente');
                    if (response.data.foto_perfil) {
                        console.log('📸 Tamanho da foto:', response.data.foto_perfil.length);
                    }
                    setPerfil(response.data);
                })
                .catch(err => {
                    console.error("❌ Erro ao carregar perfil:", err);
                    console.error("Detalhes:", err.response?.data);
                })
                .finally(() => setLoading(false));
        }
    };

    useFocusEffect(useCallback(() => { 
        fetchProfile(); 
    }, [authState.user]));

    if (loading) {
        return (
            <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color="#0a7ea4" />
            </View>
        );
    }

    if (!perfil) {
        return (
            <View style={styles.loadingContainer}>
                <Text style={styles.errorText}>Erro ao carregar perfil</Text>
                <TouchableOpacity style={styles.retryButton} onPress={fetchProfile}>
                    <Text style={styles.retryButtonText}>Tentar Novamente</Text>
                </TouchableOpacity>
            </View>
        );
    }

    const idade = calcularIdade(perfil.data_nascimento);

    // Usar foto do perfil salva no banco OU avatar padrão
    const avatarUri = perfil.foto_perfil 
        ? perfil.foto_perfil 
        : `https://ui-avatars.com/api/?name=${encodeURIComponent(perfil.nome)}&size=200&background=0a7ea4&color=fff`;

    console.log('🖼️ Avatar URI:', avatarUri.substring(0, 100));

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <Image 
                    source={{ uri: avatarUri }} 
                    style={styles.avatar}
                    onError={(e) => console.error('❌ Erro ao carregar imagem:', e.nativeEvent.error)}
                    onLoad={() => console.log('✅ Imagem carregada com sucesso')}
                />
                <Text style={styles.nome}>{perfil.nome}</Text>
                <Text style={styles.email}>{perfil.email}</Text>
            </View>

            {/* Seção de Informações Pessoais */}
            <View style={styles.infoSection}>
                <View style={styles.infoItem}>
                    <Text style={styles.infoLabel}>Idade</Text>
                    <Text style={styles.infoValue}>{idade ? `${idade} anos` : 'Não informado'}</Text>
                </View>
                <View style={styles.infoItem}>
                    <Text style={styles.infoLabel}>Tipo Sanguíneo</Text>
                    <Text style={styles.infoValue}>{perfil.tipo_sanguineo || 'Não informado'}</Text>
                </View>
                <View style={styles.infoItemFull}>
                    <Text style={styles.infoLabel}>Alergias</Text>
                    <Text style={styles.infoValue}>{perfil.alergias || 'Nenhuma informada'}</Text>
                </View>
            </View>

            <View style={styles.menu}>
                <TouchableOpacity style={styles.menuItem} onPress={() => router.push('/edit-profile')}>
                    <Ionicons name="person-outline" size={24} color="#333" />
                    <Text style={styles.menuItemText}>Editar Perfil</Text>
                    <Ionicons name="chevron-forward-outline" size={24} color="gray" />
                </TouchableOpacity>
            </View>

            <TouchableOpacity style={styles.logoutButton} onPress={signOut}>
                <Text style={styles.logoutButtonText}>Sair</Text>
            </TouchableOpacity>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f5f5f5' },
    loadingContainer: { 
        flex: 1, 
        justifyContent: 'center', 
        alignItems: 'center',
        backgroundColor: '#f5f5f5' 
    },
    errorText: {
        fontSize: 16,
        color: '#666',
        marginBottom: 20,
    },
    retryButton: {
        backgroundColor: '#0a7ea4',
        paddingHorizontal: 30,
        paddingVertical: 12,
        borderRadius: 8,
    },
    retryButtonText: {
        color: '#fff',
        fontSize: 16,
        fontWeight: '600',
    },
    header: { alignItems: 'center', marginTop: 60, paddingHorizontal: 20 },
    avatar: { 
        width: 120, 
        height: 120, 
        borderRadius: 60, 
        marginBottom: 20, 
        borderWidth: 3, 
        borderColor: '#0a7ea4',
        backgroundColor: '#e0e0e0'
    },
    nome: { fontSize: 24, fontWeight: 'bold' },
    email: { fontSize: 16, color: 'gray', marginTop: 4 },
    infoSection: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        marginTop: 20,
        marginHorizontal: 20,
        padding: 20,
        backgroundColor: 'white',
        borderRadius: 10,
        elevation: 2,
    },
    infoItem: { width: '48%', marginBottom: 15 },
    infoItemFull: { width: '100%' },
    infoLabel: { color: 'gray', fontSize: 14 },
    infoValue: { fontSize: 16, fontWeight: 'bold', marginTop: 4 },
    menu: { marginTop: 20, paddingHorizontal: 20, flex: 1 },
    menuItem: { 
        flexDirection: 'row', 
        alignItems: 'center', 
        backgroundColor: 'white', 
        padding: 20, 
        borderRadius: 10, 
        marginBottom: 10, 
        elevation: 2 
    },
    menuItemText: { fontSize: 18, marginLeft: 15, flex: 1 },
    logoutButton: { 
        margin: 20, 
        backgroundColor: '#FF634720', 
        padding: 15, 
        borderRadius: 10, 
        alignItems: 'center' 
    },
    logoutButtonText: { color: '#FF6347', fontSize: 18, fontWeight: 'bold' },
});
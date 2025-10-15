// app/avaliacao/[id].tsx

import React, { useState } from 'react';
import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity, Alert } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

// --- NOSSOS DADOS DE MENTIRA ---

const MOCK_AVALIACOES = {
    stress: { 
        id: 'stress', 
        titulo: 'Teste de Nível de Estresse', 
        cor: '#FF6347', 
        icone: 'pulse',
        perguntas: [
            { id: 1, texto: "Com que frequência você se sentiu nervoso ou estressado na última semana?", opcoes: ["Nunca", "Quase Nunca", "Às Vezes", "Quase Sempre", "Sempre"] },
            { id: 2, texto: "Com que frequência você se sentiu incapaz de controlar as coisas importantes na sua vida?", opcoes: ["Nunca", "Quase Nunca", "Às Vezes", "Quase Sempre", "Sempre"] },
            { id: 3, texto: "Com que frequência você sentiu que as dificuldades estavam se acumulando tanto que você não conseguiria superá-las?", opcoes: ["Nunca", "Quase Nunca", "Às Vezes", "Quase Sempre", "Sempre"] },
        ]
    },
    // Adicionaríamos os outros testes aqui (burnout, ansiedade)...
};

export default function AvaliacaoScreen() {
    const { id } = useLocalSearchParams();
    const router = useRouter();

    // --- CONTROLES DE ESTADO DO QUESTIONÁRIO ---
    const [iniciado, setIniciado] = useState(false);
    const [perguntaAtualIndex, setPerguntaAtualIndex] = useState(0);
    const [respostas, setRespostas] = useState({});

    const avaliacao = MOCK_AVALIACOES[id as string];

    if (!avaliacao) {
        return <SafeAreaView style={styles.container}><Text>Avaliação não encontrada.</Text></SafeAreaView>;
    }

    const perguntaAtual = avaliacao.perguntas[perguntaAtualIndex];

    // --- FUNÇÕES DE LÓGICA ---
    const handleResponder = (opcao: string) => {
        setRespostas({ ...respostas, [perguntaAtual.id]: opcao });
    };

    const proximaPergunta = () => {
        if (perguntaAtualIndex < avaliacao.perguntas.length - 1) {
            setPerguntaAtualIndex(perguntaAtualIndex + 1);
        } else {
            // Chegou na última pergunta
            Alert.alert("Fim do Teste", "Você respondeu todas as perguntas! O próximo passo seria mostrar o resultado.", [
                { text: "OK", onPress: () => router.back() }
            ]);
        }
    };

    // --- RENDERIZAÇÃO ---
    if (!iniciado) {
        // TELA DE INTRODUÇÃO
        return (
            <SafeAreaView style={[styles.container, { backgroundColor: avaliacao.cor }]}>
                <TouchableOpacity onPress={() => router.back()} style={styles.backButton}><Ionicons name="close" size={30} color="white" /></TouchableOpacity>
                <View style={styles.content}>
                    <Ionicons name={avaliacao.icone} size={60} color="white" style={{ marginBottom: 20 }} />
                    <Text style={styles.title}>{avaliacao.titulo}</Text>
                    <Text style={styles.instructions}>Este questionário é uma ferramenta de autoavaliação e não substitui um diagnóstico profissional.</Text>
                </View>
                <TouchableOpacity style={styles.startButton} onPress={() => setIniciado(true)}><Text style={styles.startButtonText}>Começar</Text></TouchableOpacity>
            </SafeAreaView>
        );
    }

    // TELA DO QUESTIONÁRIO
    return (
        <SafeAreaView style={styles.containerQuestionario}>
            <Text style={styles.progressText}>Pergunta {perguntaAtualIndex + 1} de {avaliacao.perguntas.length}</Text>
            <View style={styles.questionContainer}>
                <Text style={styles.questionText}>{perguntaAtual.texto}</Text>
            </View>
            <View>
                {perguntaAtual.opcoes.map((opcao) => (
                    <TouchableOpacity 
                        key={opcao} 
                        style={[styles.optionButton, respostas[perguntaAtual.id] === opcao && styles.optionSelected]}
                        onPress={() => handleResponder(opcao)}
                    >
                        <Text style={[styles.optionText, respostas[perguntaAtual.id] === opcao && styles.optionTextSelected]}>{opcao}</Text>
                    </TouchableOpacity>
                ))}
            </View>
            <TouchableOpacity style={styles.nextButton} onPress={proximaPergunta}>
                <Text style={styles.nextButtonText}>{perguntaAtualIndex === avaliacao.perguntas.length - 1 ? 'Finalizar' : 'Próxima'}</Text>
            </TouchableOpacity>
        </SafeAreaView>
    );
}

// --- ESTILOS ---
const styles = StyleSheet.create({
    // Estilos da tela de introdução
    container: { flex: 1, justifyContent: 'space-between', alignItems: 'center', padding: 20 },
    backButton: { position: 'absolute', top: 50, left: 20 },
    content: { flex: 1, justifyContent: 'center', alignItems: 'center', paddingHorizontal: 20 },
    title: { fontSize: 28, fontWeight: 'bold', color: 'white', textAlign: 'center', marginBottom: 20 },
    instructions: { fontSize: 16, color: 'white', textAlign: 'center', lineHeight: 24 },
    startButton: { backgroundColor: 'white', paddingVertical: 15, paddingHorizontal: 80, borderRadius: 30, marginBottom: 40 },
    startButtonText: { fontSize: 18, fontWeight: 'bold', color: '#333' },
    // Estilos da tela do questionário
    containerQuestionario: { flex: 1, backgroundColor: '#f5f5f5', padding: 20, justifyContent: 'space-between' },
    progressText: { fontSize: 16, color: 'gray', textAlign: 'center', marginTop: 30 },
    questionContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
    questionText: { fontSize: 22, fontWeight: 'bold', textAlign: 'center', },
    optionButton: { backgroundColor: '#fff', padding: 20, borderRadius: 10, marginBottom: 10, borderWidth: 1, borderColor: '#ddd' },
    optionSelected: { backgroundColor: '#0a7ea4', borderColor: '#0a7ea4' },
    optionText: { fontSize: 16, color: '#333' },
    optionTextSelected: { color: 'white', fontWeight: 'bold' },
    nextButton: { backgroundColor: '#0a7ea4', padding: 20, borderRadius: 10, alignItems: 'center', marginBottom: 20 },
    nextButtonText: { color: 'white', fontSize: 18, fontWeight: 'bold' },
});
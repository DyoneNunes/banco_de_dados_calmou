// app/avaliacao/[id].tsx

import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams, useRouter } from 'expo-router';
import React, { useState } from 'react';
import { Alert, SafeAreaView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';

// --- NOSSOS DADOS DE MENTIRA ---

// app/avaliacao/[id].tsx --- VERSÃO FINAL E CONECTADA

import { useAuth } from '../../src/context/AuthContext';
import api from '../../src/services/api';

// --- BANCO DE DADOS DE PERGUNTAS E LÓGICAS ---

const OPCOES_FREQUENCIA = [
    { texto: 'Nunca', valor: 0 },
    { texto: 'Quase Nunca', valor: 1 },
    { texto: 'Às Vezes', valor: 2 },
    { texto: 'Quase Sempre', valor: 3 },
    { texto: 'Sempre', valor: 4 },
];

// Define the keys for AVALIACOES
type AvaliacaoKey = 'stress' | 'burnout' | 'ansiedade';

const AVALIACOES = {
    stress: { 
        id: 'stress', 
        titulo: 'Teste de Nível de Estresse',
        tipoApi: 'Avaliação de Estresse',
        cor: '#FF6347', 
        icone: 'pulse' as keyof typeof Ionicons.glyphMap,
        perguntas: [
            { id: 'q1', texto: "Com que frequência você se sentiu nervoso ou estressado na última semana?" },
            { id: 'q2', texto: "Com que frequência você sentiu que as coisas não estavam indo do seu jeito?" },
            { id: 'q3', texto: "Com que frequência você sentiu que as dificuldades estavam se acumulando tanto que você não conseguiria superá-las?" },
        ],
        opcoes: OPCOES_FREQUENCIA,
        calcularResultado: (respostas: { [key: string]: number }) => {
            const score = Object.values(respostas).reduce((acc, valor) => acc + valor, 0);
            let texto = 'Nível de Estresse Baixo';
            if (score > 4 && score <= 8) texto = 'Nível de Estresse Moderado';
            else if (score > 8) texto = 'Nível de Estresse Alto';
            return { score, texto };
        }
    },
    burnout: { 
        id: 'burnout', 
        titulo: 'Questionário de Prevenção ao Burnout',
        tipoApi: 'Questionário de Burnout',
        cor: '#4682B4', 
        icone: 'flame' as keyof typeof Ionicons.glyphMap,
        perguntas: [
            { id: 'q1', texto: "Você se sentiu emocionalmente esgotado pelo seu trabalho?" },
            { id: 'q2', texto: "Você se tornou mais cínico ou distante em relação ao seu trabalho?" },
            { id: 'q3', texto: "Você sentiu uma diminuição na sua sensação de realização profissional?" },
        ],
        opcoes: OPCOES_FREQUENCIA,
        calcularResultado: (respostas: { [key: string]: number }) => {
            const score = Object.values(respostas).reduce((acc, valor) => acc + valor, 0);
            let texto = 'Baixo Risco de Burnout';
            if (score > 4 && score <= 8) texto = 'Risco Moderado de Burnout';
            else if (score > 8) texto = 'Alto Risco de Burnout';
            return { score, texto };
        }
    },
    ansiedade: {
        id: 'ansiedade',
        titulo: 'Escala de Ansiedade (GAD-7)',
        tipoApi: 'ansiedade',
        cor: '#32CD32', 
        icone: 'help-buoy' as keyof typeof Ionicons.glyphMap,
        perguntas: [
            { id: 'q1', texto: "Sentir-se nervoso, ansioso ou muito tenso?" },
            { id: 'q2', texto: "Não ser capaz de impedir ou controlar as preocupações?" },
            { id: 'q3', texto: "Preocupar-se muito com diversas coisas?" },
        ],
        opcoes: [
            { texto: 'Nenhuma vez', valor: 0 },
            { texto: 'Vários dias', valor: 1 },
            { texto: 'Mais da metade dos dias', valor: 2 },
            { texto: 'Quase todos os dias', valor: 3 },
        ],
        calcularResultado: (respostas: { [key: string]: number }) => {
            const score = Object.values(respostas).reduce((acc, valor) => acc + valor, 0);
            let texto = 'Nível de Ansiedade Mínimo';
            if (score > 2 && score <= 4) texto = 'Nível de Ansiedade Leve';
            else if (score > 4 && score <= 6) texto = 'Nível de Ansiedade Moderado';
            else if (score > 6) texto = 'Nível de Ansiedade Grave';
            return { score, texto };
        }
    },
} as const;

export default function AvaliacaoScreen() {
    const { id } = useLocalSearchParams();
    const router = useRouter();
    const { authState } = useAuth();

    const [iniciado, setIniciado] = useState(false);
    const avaliacao = AVALIACOES[(id as AvaliacaoKey)];
    const [respostas, setRespostas] = useState<{ [key: string]: number }>({});
    const [perguntaAtualIndex, setPerguntaAtualIndex] = useState(0);

    if (!avaliacao) {
        return <SafeAreaView style={styles.container}><Text>Avaliação não encontrada.</Text></SafeAreaView>;
    }

    const perguntaAtual = avaliacao.perguntas[perguntaAtualIndex];

    const handleResponder = (valor: number) => {
        setRespostas({ ...respostas, [perguntaAtual.id]: valor });
    };

    const handleFinalizar = async () => {
        const { score, texto } = avaliacao.calcularResultado(respostas);

        const payload = {
            usuario_id: authState.user?.id,
            tipo: avaliacao.tipoApi,
            respostas: respostas, // Schema espera Dict (objeto)
            resultado_score: score,
            resultado_texto: texto
        };

        console.log('📊 [Avaliação] Enviando resultado:', payload);

        try {
            const response = await api.post('/avaliacoes', payload);
            console.log('✅ [Avaliação] Salva com sucesso:', response.data);
            Alert.alert("Avaliação Concluída", `Seu resultado: ${texto} (Pontuação: ${score})`, [
                { text: "OK", onPress: () => router.back() }
            ]);
        } catch (error: any) {
            console.error("❌ [Avaliação] Erro ao salvar:", error.response?.data || error.message);
            const mensagem = error.response?.data?.mensagem || "Não foi possível salvar sua avaliação.";
            Alert.alert("Erro", mensagem);
        }
    };

    const proximaPergunta = () => {
        if (respostas[perguntaAtual.id] === undefined) {
            Alert.alert("Atenção", "Por favor, selecione uma opção.");
            return;
        }

        if (perguntaAtualIndex < avaliacao.perguntas.length - 1) {
            setPerguntaAtualIndex(perguntaAtualIndex + 1);
        } else {
            handleFinalizar();
        }
    };

    if (!iniciado) {
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

    return (
        <SafeAreaView style={styles.containerQuestionario}>
            <Text style={styles.progressText}>Pergunta {perguntaAtualIndex + 1} de {avaliacao.perguntas.length}</Text>
            <View style={styles.questionContainer}>
                <Text style={styles.questionText}>{perguntaAtual.texto}</Text>
            </View>
            <View>
                {avaliacao.opcoes.map((opcao) => (
                    <TouchableOpacity 
                        key={opcao.valor} 
                        style={[styles.optionButton, respostas[perguntaAtual.id] === opcao.valor && styles.optionSelected]}
                        onPress={() => handleResponder(opcao.valor)}
                    >
                        <Text style={[styles.optionText, respostas[perguntaAtual.id] === opcao.valor && styles.optionTextSelected]}>{opcao.texto}</Text>
                    </TouchableOpacity>
                ))}
            </View>
            <TouchableOpacity style={styles.nextButton} onPress={proximaPergunta}>
                <Text style={styles.nextButtonText}>{perguntaAtualIndex === avaliacao.perguntas.length - 1 ? 'Finalizar' : 'Próxima'}</Text>
            </TouchableOpacity>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: 'space-between', alignItems: 'center', padding: 20 },
    backButton: { position: 'absolute', top: 50, left: 20, zIndex: 10 },
    content: { flex: 1, justifyContent: 'center', alignItems: 'center', paddingHorizontal: 20 },
    title: { fontSize: 28, fontWeight: 'bold', color: 'white', textAlign: 'center', marginBottom: 20 },
    instructions: { fontSize: 16, color: 'white', textAlign: 'center', lineHeight: 24 },
    startButton: { backgroundColor: 'white', paddingVertical: 15, paddingHorizontal: 80, borderRadius: 30, marginBottom: 40 },
    startButtonText: { fontSize: 18, fontWeight: 'bold', color: '#333' },
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


/* (removed duplicate AvaliacaoScreen implementation and duplicate styles) */
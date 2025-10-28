import { Ionicons } from '@expo/vector-icons';
import { Audio, AVPlaybackStatus } from 'expo-av';
import { useLocalSearchParams, useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { ActivityIndicator, Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import api from '../../src/services/api';

type Meditacao = {
  id: number;
  titulo: string;
  descricao: string;
  categoria: string;
  duracao_minutos: number;
  imagem_capa: string;
  url_audio: string;
};

// Função para formatar o tempo de segundos para MM:SS
const formatTime = (millis: number) => {
  if (!millis) return '00:00';
  const totalSeconds = Math.floor(millis / 1000);
  const seconds = totalSeconds % 60;
  const minutes = Math.floor(totalSeconds / 60);
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
};

export default function MeditacaoDetalheScreen() {
    const { id } = useLocalSearchParams();
    const router = useRouter();

    const [meditacao, setMeditacao] = useState<Meditacao | null>(null);
    const [sound, setSound] = useState<Audio.Sound | null>(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [loading, setLoading] = useState(true);
    const [playbackStatus, setPlaybackStatus] = useState<AVPlaybackStatus | null>(null);

    useEffect(() => {
        if (id) {
            api.get(`/meditacoes/${id}`)
                .then(response => {
                    // Console.log adicionado para debug
                    console.log("Dados recebidos na tela do player:", JSON.stringify(response.data, null, 2));
                    setMeditacao(response.data);
                })
                .catch(err => {
                    console.error("Erro ao buscar detalhes da meditação:", err);
                })
                .finally(() => setLoading(false));
        }
    }, [id]);

    const playPauseSound = async () => {
        if (!meditacao?.url_audio) return;
        if (sound) {
            isPlaying ? await sound.pauseAsync() : await sound.playAsync();
        } else {
            try {
                await Audio.setAudioModeAsync({ playsInSilentModeIOS: true });
                const { sound: newSound } = await Audio.Sound.createAsync(
                    { uri: meditacao.url_audio },
                    { shouldPlay: true },
                    (status) => setPlaybackStatus(status)
                );
                setSound(newSound);
            } catch (error) {
                console.error("Erro ao carregar áudio:", error);
            }
        }
    };

    useEffect(() => {
        if (playbackStatus?.isLoaded) {
            setIsPlaying(playbackStatus.isPlaying);
        }
    }, [playbackStatus]);

    useEffect(() => {
        return sound ? () => { sound.unloadAsync(); } : undefined;
    }, [sound]);

    if (loading) {
        return <ActivityIndicator size="large" style={styles.container} />;
    }
    if (!meditacao) {
        return <View style={styles.container}><Text>Meditação não encontrada</Text></View>;
    }

    const progress = playbackStatus?.isLoaded && playbackStatus.durationMillis
        ? (playbackStatus.positionMillis / playbackStatus.durationMillis) * 100
        : 0;

    return (
        <View style={styles.container}>
            <Image source={{ uri: meditacao.imagem_capa }} style={styles.headerImage} blurRadius={20} />
            <View style={styles.overlay} />

            <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
                <Ionicons name="arrow-back" size={24} color="white" />
            </TouchableOpacity>

            <View style={styles.content}>
                <Text style={styles.title}>{meditacao.titulo}</Text>
                <Text style={styles.description}>{meditacao.descricao}</Text>

                <View style={styles.playerContainer}>
                    <TouchableOpacity style={styles.playButton} onPress={playPauseSound}>
                        <Ionicons name={isPlaying ? 'pause' : 'play'} size={48} color="#004d40" />
                    </TouchableOpacity>
                    <View style={styles.progressContainer}>
                        <Text style={styles.timeText}>{formatTime(playbackStatus?.isLoaded ? playbackStatus.positionMillis ?? 0 : 0)}</Text>
                        <View style={styles.progressBarBackground}>
                            <View style={[styles.progressBarForeground, { width: `${progress}%` }]} />
                        </View>
                        <Text style={styles.timeText}>{formatTime(playbackStatus?.isLoaded ? playbackStatus.durationMillis ?? 0 : 0)}</Text>
                    </View>
                </View>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#004d40', justifyContent: 'center' },
    headerImage: { width: '100%', height: '100%', position: 'absolute' },
    overlay: { ...StyleSheet.absoluteFillObject, backgroundColor: 'rgba(0, 77, 64, 0.7)' },
    backButton: { position: 'absolute', top: 60, left: 20, zIndex: 10 },
    content: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
    title: { fontSize: 32, fontWeight: 'bold', color: 'white', textAlign: 'center', marginBottom: 16 },
    description: { fontSize: 18, color: '#B2DFDB', textAlign: 'center', lineHeight: 26 },
    playerContainer: { position: 'absolute', bottom: 60, left: 20, right: 20 },
    playButton: { backgroundColor: 'white', width: 80, height: 80, borderRadius: 40, justifyContent: 'center', alignItems: 'center', alignSelf: 'center', marginBottom: 30, elevation: 10, shadowColor: '#000', shadowOpacity: 0.3, shadowRadius: 10, },
    progressContainer: { flexDirection: 'row', alignItems: 'center' },
    timeText: { color: '#B2DFDB', width: 50, textAlign: 'center' },
    progressBarBackground: { flex: 1, height: 6, backgroundColor: 'rgba(255, 255, 255, 0.3)', borderRadius: 3, marginHorizontal: 10, },
    progressBarForeground: { height: '100%', backgroundColor: 'white', borderRadius: 3, },
});
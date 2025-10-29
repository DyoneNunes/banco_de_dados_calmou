import { useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { ActivityIndicator, Alert, ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import ProfilePhotoPicker from '../components/ProfilePhotoPicker';
import { useAuth } from '../src/context/AuthContext';
import api from '../src/services/api';

export default function EditProfileScreen() {
  const { authState } = useAuth();
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  
  const [formData, setFormData] = useState({
    nome: '',
    cpf: '',
    data_nascimento: '',
    tipo_sanguineo: '',
    alergias: '',
    foto_perfil: null as string | null,
  });

  // Carregar dados do usuário
  useEffect(() => {
    if (authState.user?.id) {
      loadUserData();
    }
  }, [authState.user]);

  const loadUserData = async () => {
    if (!authState.user?.id) {
      Alert.alert('Erro', 'Usuário não identificado');
      return;
    }

    try {
      setLoading(true);
      const response = await api.get(`/usuarios/${authState.user.id}`);
      console.log('✅ Dados carregados:', response.data);
      
      setFormData({
        nome: response.data.nome || '',
        cpf: response.data.cpf || '',
        data_nascimento: response.data.data_nascimento || '',
        tipo_sanguineo: response.data.tipo_sanguineo || '',
        alergias: response.data.alergias || '',
        foto_perfil: response.data.foto_perfil || null,
      });
    } catch (error: any) {
      console.error('❌ Erro ao carregar dados:', error);
      Alert.alert(
        'Erro', 
        error.response?.data?.mensagem || 'Não foi possível carregar os dados do perfil'
      );
    } finally {
      setLoading(false);
    }
  };

  // Atualizar foto
  const handlePhotoChange = (base64Photo: string | null): void => {
    setFormData({ ...formData, foto_perfil: base64Photo });
  };

  // Formatar data para ISO (YYYY-MM-DD)
  const formatarDataParaISO = (data: string): string | null => {
    if (!data) return null;

    // Remove caracteres não numéricos
    const numeros = data.replace(/\D/g, '');

    // Verifica se tem 8 dígitos (DDMMAAAA ou AAAAMMDD)
    if (numeros.length !== 8) return data; // Retorna como está se não tiver 8 dígitos

    // Tenta interpretar como DD/MM/AAAA (formato brasileiro)
    const dia = parseInt(numeros.substring(0, 2));
    const mes = parseInt(numeros.substring(2, 4));
    const ano = parseInt(numeros.substring(4, 8));

    // Valida se é uma data válida
    if (dia >= 1 && dia <= 31 && mes >= 1 && mes <= 12 && ano >= 1900 && ano <= 2100) {
      return `${ano}-${mes.toString().padStart(2, '0')}-${dia.toString().padStart(2, '0')}`;
    }

    // Se não for válido, retorna como está
    return data;
  };

  // Salvar perfil
  const handleSave = async () => {
    if (!authState.user?.id) {
      Alert.alert('Erro', 'Usuário não identificado');
      return;
    }

    // Formatar data de nascimento
    const dataFormatada = formatarDataParaISO(formData.data_nascimento);

    try {
      setLoading(true);
      const response = await api.put('/perfil', {
        id: authState.user.id,
        nome: formData.nome,
        cpf: formData.cpf,
        data_nascimento: dataFormatada,
        tipo_sanguineo: formData.tipo_sanguineo,
        alergias: formData.alergias,
        foto_perfil: formData.foto_perfil,
      });

      console.log('✅ Perfil salvo:', response.data);
      Alert.alert('Sucesso', 'Perfil atualizado com sucesso!', [
        { text: 'OK', onPress: () => router.back() }
      ]);
    } catch (error: any) {
      console.error('❌ Erro ao salvar perfil:', error);
      Alert.alert(
        'Erro', 
        error.response?.data?.mensagem || 'Não foi possível salvar o perfil'
      );
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#6C47FF" />
        <Text style={styles.loadingText}>Carregando...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* Componente de Foto de Perfil */}
      <ProfilePhotoPicker 
        currentPhoto={formData.foto_perfil}
        onPhotoChange={handlePhotoChange}
      />

      {/* Campos do formulário */}
      <View style={styles.form}>
        <Text style={styles.label}>Nome Completo</Text>
        <TextInput
          style={styles.input}
          value={formData.nome}
          onChangeText={(text) => setFormData({ ...formData, nome: text })}
          placeholder="Digite seu nome"
          editable={!loading}
        />

        <Text style={styles.label}>CPF</Text>
        <TextInput
          style={styles.input}
          value={formData.cpf}
          onChangeText={(text) => setFormData({ ...formData, cpf: text })}
          placeholder="000.000.000-00"
          keyboardType="numeric"
          maxLength={14}
          editable={!loading}
        />

        <Text style={styles.label}>Data de Nascimento</Text>
        <TextInput
          style={styles.input}
          value={formData.data_nascimento}
          onChangeText={(text) => {
            // Permite apenas números e traços/barras
            const cleaned = text.replace(/[^0-9/-]/g, '');
            setFormData({ ...formData, data_nascimento: cleaned });
          }}
          placeholder="DD/MM/AAAA ou AAAA-MM-DD"
          keyboardType="numeric"
          maxLength={10}
          editable={!loading}
        />
        <Text style={styles.hint}>Ex: 29/05/1998 ou 1998-05-29</Text>

        <Text style={styles.label}>Tipo Sanguíneo</Text>
        <TextInput
          style={styles.input}
          value={formData.tipo_sanguineo}
          onChangeText={(text) => setFormData({ ...formData, tipo_sanguineo: text })}
          placeholder="A+, B-, O+, etc."
          maxLength={3}
          editable={!loading}
        />

        <Text style={styles.label}>Alergias</Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          value={formData.alergias}
          onChangeText={(text) => setFormData({ ...formData, alergias: text })}
          placeholder="Liste suas alergias"
          multiline
          numberOfLines={4}
          editable={!loading}
        />

        <TouchableOpacity 
          style={[styles.saveButton, loading && styles.saveButtonDisabled]} 
          onPress={handleSave}
          disabled={loading}
        >
          <Text style={styles.saveButtonText}>
            {loading ? 'Salvando...' : 'Salvar Alterações'}
          </Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  form: {
    padding: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
    marginTop: 16,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    backgroundColor: '#f9f9f9',
  },
  hint: {
    fontSize: 12,
    color: '#999',
    marginTop: 4,
    fontStyle: 'italic',
  },
  textArea: {
    minHeight: 100,
    textAlignVertical: 'top',
  },
  saveButton: {
    backgroundColor: '#6C47FF',
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 30,
    marginBottom: 40,
  },
  saveButtonDisabled: {
    backgroundColor: '#999',
  },
  saveButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
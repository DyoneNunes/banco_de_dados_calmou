import React, { useEffect, useState } from 'react';
import { ActivityIndicator, Alert, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import api from '../../src/services/api';
// Hooks para pegar o ID da URL e para navegar
import { useLocalSearchParams, useRouter } from 'expo-router';

export default function EditUserScreen() {
  // Pega o ID da URL, ex: /edit-user/1 -> id = '1'
  const { id } = useLocalSearchParams();
  const router = useRouter();

  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState(''); // Idealmente, não carregaríamos a senha
  const [loading, setLoading] = useState(true);

  // Busca os dados atuais do usuário quando a tela carrega
  useEffect(() => {
    if (id) {
      // Precisamos de uma rota GET /usuarios/id no backend
      api.get(`/usuarios/${id}`)
        .then(response => {
          const user = response.data;
          setNome(user.nome);
          setEmail(user.email);
          // Não preenchemos o campo senha por segurança
        })
        .catch(err => {
          console.error("Erro ao buscar dados do usuário", err);
          Alert.alert("Erro", "Não foi possível carregar os dados do usuário.");
        })
        .finally(() => setLoading(false));
    }
  }, [id]);

  const handleUpdateUser = () => {
    if (!nome || !email) {
      Alert.alert('Erro', 'Nome e Email são obrigatórios.');
      return;
    }
    const userData = {
      nome,
      email,
      senha_hash: senha || 'senha_nao_alterada' // Lógica de senha simplificada
    };

    api.put(`/usuarios/${id}`, userData)
      .then(() => {
        Alert.alert('Sucesso', 'Usuário atualizado!');
        router.back(); // Volta para a lista
      })
      .catch(err => {
        console.error("Erro ao atualizar usuário", err);
        Alert.alert('Erro', 'Não foi possível atualizar o usuário.');
      });
  };
  
  if (loading) {
    return <ActivityIndicator size="large" style={{ flex: 1 }} />;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Editar Usuário (ID: {id})</Text>
      <TextInput style={styles.input} placeholder="Nome Completo" value={nome} onChangeText={setNome} />
      <TextInput style={styles.input} placeholder="Email" value={email} onChangeText={setEmail} keyboardType="email-address" />
      <TextInput style={styles.input} placeholder="Nova Senha (deixe em branco para não alterar)" onChangeText={setSenha} secureTextEntry />
      <TouchableOpacity style={styles.button} onPress={handleUpdateUser}>
        <Text style={styles.buttonText}>Salvar Alterações</Text>
      </TouchableOpacity>
    </View>
  );
}

// (Os estilos podem ser os mesmos do add-user.tsx)
const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#f5f5f5' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  input: { backgroundColor: '#fff', height: 50, borderColor: '#ddd', borderWidth: 1, borderRadius: 8, marginBottom: 15, paddingHorizontal: 15, fontSize: 16 },
  button: { backgroundColor: '#28a745', padding: 15, borderRadius: 8, alignItems: 'center' },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' }
});
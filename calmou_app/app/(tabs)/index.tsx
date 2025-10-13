// NOVO: Importe o useFocusEffect e o useCallback
import { Link, useFocusEffect } from 'expo-router'; // Mude aqui
import React, { useCallback, useState } from 'react';
import { ActivityIndicator, FlatList, SafeAreaView, StatusBar, StyleSheet, Text, View } from 'react-native';
import api from '../../src/services/api';

type User = {
  id: number;
  nome: string;
  email: string;
  data_cadastro: string;
};

export default function HomeScreen() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  // Criamos uma função separada para buscar os usuários
  const fetchUsers = () => {
    setLoading(true); // Mostra o indicador de carregamento
    api.get('/usuarios')
      .then(response => {
        setUsers(response.data);
      })
      .catch(error => {
        console.error("Erro ao buscar usuários!", error);
      })
      .finally(() => {
        setLoading(false); // Esconde o indicador de carregamento
      });
  };

  // SUBSTITUÍMOS O useEffect PELO useFocusEffect
  useFocusEffect(
    useCallback(() => {
      // Esta função será chamada toda vez que a tela ganhar foco
      fetchUsers();
    }, [])
  );

  return (
    <SafeAreaView style={styles.container}>
      {/* (O resto do seu JSX (a parte visual) continua exatamente o mesmo) */}
      <StatusBar barStyle="dark-content" />
      <View style={styles.header}>
        <Text style={styles.title}>Usuários do Calmou</Text>
        <Link href="/add-user" style={styles.addButton}>
          <Text style={styles.addButtonText}>+</Text>
        </Link>
      </View>

      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : (
        <FlatList
          data={users}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <View style={styles.userItem}>
              <Text style={styles.userName}>Nome: {item.nome}</Text>
              <Text>Email: {item.email}</Text>
            </View>
          )}
        />
      )}
    </SafeAreaView>
  );
}

// (Seus estilos continuam os mesmos)
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    paddingHorizontal: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginVertical: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  addButton: {
    backgroundColor: '#007BFF',
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  addButtonText: {
    color: '#fff',
    fontSize: 24,
    lineHeight: 28,
  },
  userItem: {
    backgroundColor: '#fff',
    marginBottom: 15,
    padding: 15,
    borderRadius: 8,
    elevation: 3,
  },
  userName: {
    fontWeight: 'bold',
  }
});
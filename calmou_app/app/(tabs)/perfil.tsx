import { Ionicons } from '@expo/vector-icons';
import React from 'react';
import { Image, SafeAreaView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { useAuth } from '../../src/context/AuthContext'; // 1. IMPORTE O useAuth

export default function PerfilScreen() {
  const { signOut } = useAuth(); // 2. PEGUE A FUNÇÃO signOut

  const usuario = {
    nome: "Dyone Nunes",
    email: "dyone.nunes@calmou.app",
    avatarUrl: "https://github.com/DyoneNunes.png",
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Image source={{ uri: usuario.avatarUrl }} style={styles.avatar} />
        <Text style={styles.nome}>{usuario.nome}</Text>
        <Text style={styles.email}>{usuario.email}</Text>
      </View>

      <View style={styles.menu}>
        {/* Itens do Menu */}
        <TouchableOpacity style={styles.menuItem}>
          <Ionicons name="person-outline" size={24} color="#333" />
          <Text style={styles.menuItemText}>Editar Perfil</Text>
          <Ionicons name="chevron-forward-outline" size={24} color="gray" />
        </TouchableOpacity>
        {/* ... outros itens ... */}
      </View>

      {/* 3. ADICIONE O onPress NO BOTÃO DE LOGOUT */}
      <TouchableOpacity style={styles.logoutButton} onPress={signOut}>
        <Text style={styles.logoutButtonText}>Sair</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

// (Seus estilos continuam os mesmos)
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  header: { alignItems: 'center', marginTop: 60, paddingHorizontal: 20 },
  avatar: { width: 120, height: 120, borderRadius: 60, marginBottom: 20, borderWidth: 3, borderColor: '#0a7ea4' },
  nome: { fontSize: 24, fontWeight: 'bold' },
  email: { fontSize: 16, color: 'gray', marginTop: 4 },
  menu: { marginTop: 40, paddingHorizontal: 20, flex: 1 },
  menuItem: { 
    flexDirection: 'row', 
    alignItems: 'center', 
    backgroundColor: 'white', 
    paddingVertical: 15,
    paddingHorizontal: 20, 
    borderRadius: 10, 
    marginBottom: 10,
    elevation: 2,
  },
  menuItemText: { fontSize: 18, marginLeft: 15, flex: 1 },
  logoutButton: { margin: 20, backgroundColor: '#FF634720', padding: 15, borderRadius: 10, alignItems: 'center' },
  logoutButtonText: { color: '#FF6347', fontSize: 18, fontWeight: 'bold' },
});
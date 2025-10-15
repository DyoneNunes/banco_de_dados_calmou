// app/(tabs)/perfil.tsx

import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity, Image } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function PerfilScreen() {
  // Dados de mentira para o perfil. O Dyone do futuro conecta isso.
  const usuario = {
    nome: "Dyone Nunes",
    email: "dyone.nunes@calmou.app",
    avatarUrl: "https://github.com/DyoneNunes.png", // Usando o avatar do GitHub como exemplo
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Image source={{ uri: usuario.avatarUrl }} style={styles.avatar} />
        <Text style={styles.nome}>{usuario.nome}</Text>
        <Text style={styles.email}>{usuario.email}</Text>
      </View>

      <View style={styles.menu}>
        <TouchableOpacity style={styles.menuItem}>
          <Ionicons name="person-outline" size={24} color="#333" />
          <Text style={styles.menuItemText}>Editar Perfil</Text>
          <Ionicons name="chevron-forward-outline" size={24} color="gray" />
        </TouchableOpacity>
        <TouchableOpacity style={styles.menuItem}>
          <Ionicons name="notifications-outline" size={24} color="#333" />
          <Text style={styles.menuItemText}>Notificações</Text>
          <Ionicons name="chevron-forward-outline" size={24} color="gray" />
        </TouchableOpacity>
        <TouchableOpacity style={styles.menuItem}>
          <Ionicons name="lock-closed-outline" size={24} color="#333" />
          <Text style={styles.menuItemText}>Segurança</Text>
          <Ionicons name="chevron-forward-outline" size={24} color="gray" />
        </TouchableOpacity>
      </View>

      <TouchableOpacity style={styles.logoutButton}>
        <Text style={styles.logoutButtonText}>Sair</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

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
    shadowColor: '#000',
    shadowOpacity: 0.05,
    shadowRadius: 5,
  },
  menuItemText: { fontSize: 18, marginLeft: 15, flex: 1 }, // flex: 1 empurra a seta para a direita
  logoutButton: { margin: 20, backgroundColor: '#FF634720', padding: 15, borderRadius: 10, alignItems: 'center' },
  logoutButtonText: { color: '#FF6347', fontSize: 18, fontWeight: 'bold' },
});
import { Link } from 'expo-router';
import React, { useState } from 'react';
import { Alert, Platform, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import { useAuth } from '../../src/context/AuthContext';

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { signIn } = useAuth();

  const handleSignIn = async () => {
    // --- DEPURAÇÃO ---
    // Vamos imprimir os valores no terminal para ver o que está sendo enviado.
    console.log('Tentando fazer login com:');
    console.log('Email:', email);
    console.log('Senha:', password);
    // --- FIM DA DEPURAÇÃO ---

    // A verificação do frontend (pode remover se quiser, mas é uma boa prática)
    if (!email || !password) {
        Alert.alert('Atenção', 'Por favor, preencha todos os campos.');
        return;
    }
    
    // Chama a função de login do nosso contexto
    const result = await signIn(email, password);

    // Se o backend retornar um erro, ele será exibido aqui
    if (result && result.error) {
      Alert.alert('Erro no Login', result.msg);
    }
  };

  return (
    <View style={styles.container}>
      {/* <Image source={require('../../assets/images/logo-calmou.png')} style={styles.logo} /> */}
      <Text style={styles.title}>Entrar</Text>
      
      <TextInput 
        style={styles.input} 
        placeholder="Email*" 
        value={email} 
        onChangeText={setEmail} 
        keyboardType="email-address" 
        autoCapitalize="none" 
      />
      <TextInput 
        style={styles.input} 
        placeholder="Senha*" 
        value={password} 
        onChangeText={setPassword} 
        secureTextEntry 
      />
      
      <TouchableOpacity style={styles.button} onPress={handleSignIn}>
        <Text style={styles.buttonText}>Acessar</Text>
      </TouchableOpacity>

      <Text style={styles.footerText}>Não possui conta?{' '}
        <Link href="/(auth)/signup">
          <Text style={styles.linkText}>Cadastre-se aqui</Text>
        </Link>
      </Text>
    </View>
  );
}

// (Os estilos continuam os mesmos)
const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: 'center', padding: 20, backgroundColor: Platform.OS === 'ios' ? '#FFFBF5' : '#FFFBF5' },
    logo: { width: 100, height: 100, alignSelf: 'center', marginBottom: 40 },
    title: { fontSize: 32, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
    input: { backgroundColor: '#fff', height: 50, borderColor: '#ddd', borderWidth: 1, borderRadius: 8, marginBottom: 15, paddingHorizontal: 15, fontSize: 16 },
    button: { backgroundColor: '#004d40', padding: 15, borderRadius: 8, alignItems: 'center', marginTop: 10 },
    buttonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
    footerText: { textAlign: 'center', marginTop: 20, color: 'gray' },
    linkText: { color: '#00796b', fontWeight: 'bold' },
});
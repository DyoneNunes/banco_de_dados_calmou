import { Link, useRouter } from 'expo-router';
import React, { useState } from 'react';
import { Alert, Platform, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import { useAuth } from '../../src/context/AuthContext';

export default function SignUpScreen() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { signUp } = useAuth();
  const router = useRouter();

  const handleSignUp = async () => {
    if (!nome || !email || !password) {
      Alert.alert('Atenção', 'Por favor, preencha todos os campos.');
      return;
    }
    const result = await signUp(nome, email, password);
    if (result && result.error) {
      Alert.alert('Erro no Cadastro', result.msg);
    } else {
      Alert.alert('Sucesso', 'Conta criada! Por favor, faça o login.');
      router.replace('/(auth)/login');
    }
  };

  return (
    <View style={styles.container}>
      {/* <Image source={require('../../assets/images/logo-calmou.png')} style={styles.logo} /> */}
      <Text style={styles.title}>Cadastrar</Text>

      <TextInput style={styles.input} placeholder="Nome*" value={nome} onChangeText={setNome} />
      <TextInput style={styles.input} placeholder="Email*" value={email} onChangeText={setEmail} keyboardType="email-address" autoCapitalize="none" />
      <TextInput style={styles.input} placeholder="Senha*" value={password} onChangeText={setPassword} secureTextEntry />
      
      <TouchableOpacity style={styles.button} onPress={handleSignUp}>
        <Text style={styles.buttonText}>Cadastrar</Text>
      </TouchableOpacity>

      <Text style={styles.footerText}>Já possui conta?{' '}
        <Link href="/(auth)/login">
          <Text style={styles.linkText}>Entrar</Text>
        </Link>
      </Text>
    </View>
  );
}

// MESMOS ESTILOS DA TELA DE LOGIN
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
import * as SecureStore from 'expo-secure-store';
import React, { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { DeviceEventEmitter } from 'react-native';
import api from '../services/api';

// --- Tipagem para o objeto do usuário ---
interface User {
  id: number;
  nome: string;
  email: string;
}

interface AuthContextData {
  authState: { user: User | null; authenticated: boolean };
  loading: boolean;
  signIn: (email: string, password: string) => Promise<any>;
  signUp: (nome: string, email: string, password: string) => Promise<any>;
  signOut: () => void;
}

const AuthContext = createContext<AuthContextData>({} as AuthContextData);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [authState, setAuthState] = useState<{ user: User | null; authenticated: boolean }>({
    user: null,
    authenticated: false,
  });
  const [loading, setLoading] = useState(true);

  // Função signOut precisa ser definida antes dos useEffects
  const signOut = useCallback(async () => {
    await SecureStore.deleteItemAsync('user');
    await SecureStore.deleteItemAsync('access_token');
    setAuthState({ user: null, authenticated: false });
    console.log('👋 [AuthContext] Logout realizado');
  }, []);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const userJson = await SecureStore.getItemAsync('user');
        const token = await SecureStore.getItemAsync('access_token');

        if (userJson && token) {
          setAuthState({ user: JSON.parse(userJson), authenticated: true });
          console.log('✅ [AuthContext] Sessão restaurada com sucesso');
        } else if (userJson && !token) {
          // Usuário salvo mas sem token - fazer logout
          await SecureStore.deleteItemAsync('user');
          console.log('⚠️ [AuthContext] Token expirado - sessão encerrada');
        }
      } catch (e) {
        console.error("❌ [AuthContext] Erro ao carregar usuário:", e);
      } finally {
        setLoading(false);
      }
    };
    loadUser();
  }, []);

  // useEffect separado para o listener de token expirado
  useEffect(() => {
    const handleTokenExpired = () => {
      console.warn('🔓 [AuthContext] Token expirado detectado - fazendo logout');
      signOut();
    };

    // Adiciona listener usando DeviceEventEmitter do React Native
    const subscription = DeviceEventEmitter.addListener('token-expired', handleTokenExpired);

    // Cleanup - remove listener quando o componente desmontar
    return () => {
      subscription.remove();
    };
  }, [signOut]);

  const signIn = async (email: string, password: string) => {
    try {
      console.log('🔐 [AuthContext] Iniciando login...');
      console.log('📧 Email:', email);
      console.log('🔗 URL da API:', api.defaults.baseURL);

      const response = await api.post('/login', { email, password });

      console.log('✅ [AuthContext] Resposta do servidor:', response.status);
      console.log('📦 [AuthContext] Dados recebidos:', JSON.stringify(response.data));

      const { usuario, access_token } = response.data;

      if (!usuario) {
        console.error('❌ [AuthContext] Usuário não encontrado na resposta');
        return { error: true, msg: 'Resposta inválida do servidor' };
      }

      // Salva o token JWT
      if (access_token) {
        await SecureStore.setItemAsync('access_token', access_token);
        console.log('🔑 [AuthContext] Token JWT salvo');
      }

      setAuthState({ user: usuario, authenticated: true });
      await SecureStore.setItemAsync('user', JSON.stringify(usuario));

      console.log('✅ [AuthContext] Login realizado com sucesso!');
      return response.data;
    } catch (error: any) {
      console.error('❌ [AuthContext] Erro no login:', error.message);
      if (error.response) {
        console.error('📡 Status:', error.response.status);
        console.error('📦 Dados do erro:', error.response.data);
        console.error('🔑 Mensagem:', error.response.data?.mensagem);
      } else if (error.request) {
        console.error('🌐 Erro de rede - Sem resposta do servidor');
        console.error('Request:', error.request);
        return { error: true, msg: 'Não foi possível conectar ao servidor. Verifique sua conexão e o IP do backend.' };
      } else {
        console.error('⚠️ Erro:', error.message);
      }
      return { error: true, msg: error.response?.data?.mensagem || 'Erro no login' };
    }
  };

  const signUp = async (nome: string, email: string, password: string) => {
    try {
      console.log('📝 [AuthContext] Iniciando cadastro...');
      console.log('👤 Nome:', nome);
      console.log('📧 Email:', email);
      console.log('🔑 Tamanho da senha:', password.length);

      // Validação de senha no frontend
      if (password.length < 8) {
        console.error('❌ [AuthContext] Senha muito curta');
        return { error: true, msg: 'A senha deve ter no mínimo 8 caracteres' };
      }

      if (password.length > 100) {
        console.error('❌ [AuthContext] Senha muito longa');
        return { error: true, msg: 'A senha deve ter no máximo 100 caracteres' };
      }

      // CORREÇÃO: Endpoint correto é /register
      const response = await api.post('/register', { nome, email, password });

      console.log('✅ [AuthContext] Cadastro realizado com sucesso!');
      console.log('📦 [AuthContext] Resposta:', JSON.stringify(response.data));

      // Salva o token JWT se retornado
      if (response.data.access_token) {
        await SecureStore.setItemAsync('access_token', response.data.access_token);
        console.log('🔑 [AuthContext] Token JWT salvo após cadastro');
      }

      return response.data;
    } catch (error: any) {
      console.error('❌ [AuthContext] Erro no cadastro:', error.message);

      if (error.response) {
        console.error('📡 Status:', error.response.status);
        console.error('📦 Dados do erro:', error.response.data);

        // Se houver erros de validação, formata melhor a mensagem
        if (error.response.data?.erros) {
          const erros = error.response.data.erros;
          const mensagensErro = Object.entries(erros)
            .map(([campo, msgs]: [string, any]) => `${campo}: ${msgs.join(', ')}`)
            .join('\n');
          return { error: true, msg: mensagensErro };
        }
      }

      return { error: true, msg: error.response?.data?.mensagem || 'Erro no cadastro' };
    }
  };

  return (
    <AuthContext.Provider value={{ authState, loading, signIn, signUp, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};

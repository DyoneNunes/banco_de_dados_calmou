import * as SecureStore from 'expo-secure-store';
import React, { createContext, useContext, useEffect, useState } from 'react';
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
  signIn: (email, password) => Promise<any>;
  signUp: (nome, email, password) => Promise<any>;
  signOut: () => void;
}

const AuthContext = createContext<AuthContextData>({} as AuthContextData);

export const AuthProvider = ({ children }) => {
  const [authState, setAuthState] = useState<{ user: User | null; authenticated: boolean }>({
    user: null,
    authenticated: false,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const userJson = await SecureStore.getItemAsync('user');
        if (userJson) {
          setAuthState({ user: JSON.parse(userJson), authenticated: true });
        }
      } catch (e) {
        console.error("Erro ao carregar usuário:", e);
      } finally {
        setLoading(false);
      }
    };
    loadUser();
  }, []);

  const signIn = async (email, password) => {
    try {
      const response = await api.post('/login', { email, password });
      const { usuario } = response.data;
      setAuthState({ user: usuario, authenticated: true });
      await SecureStore.setItemAsync('user', JSON.stringify(usuario));
      return response.data;
    } catch (error) {
      return { error: true, msg: error.response?.data?.mensagem || 'Erro no login' };
    }
  };

  const signUp = async (nome, email, password) => {
    try {
      // CORREÇÃO APLICADA AQUI:
      // Trocamos 'senha_hash' por 'password', que é o que o backend espera.
      const response = await api.post('/usuarios', { nome, email, password: password });
      return response.data;
    } catch (error) {
      return { error: true, msg: error.response?.data?.mensagem || 'Erro no cadastro' };
    }
  };

  const signOut = async () => {
    await SecureStore.deleteItemAsync('user');
    setAuthState({ user: null, authenticated: false });
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

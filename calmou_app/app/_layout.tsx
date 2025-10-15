// app/_layout.tsx --- VERSÃO FINAL SEM FONTE CUSTOMIZADA

import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { Stack } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import 'react-native-reanimated';

// Importando o hook que a gente já sabe que existe
import { useColorScheme } from '@/hooks/use-color-scheme';

// Mantém a splash screen visível
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const colorScheme = useColorScheme();

  // Esconde a splash screen
  SplashScreen.hideAsync();

  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <Stack>
        {/* A única tela que o layout principal precisa saber é a de abas */}
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="+not-found" />
      </Stack>
    </ThemeProvider>
  );
}
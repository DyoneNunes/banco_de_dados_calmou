import { useColorScheme } from '@/hooks/use-color-scheme';
import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { Stack, useRouter, useSegments } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { useEffect } from 'react';
import 'react-native-reanimated';
import { AuthProvider, useAuth } from '../src/context/AuthContext';

SplashScreen.preventAutoHideAsync();

function InitialLayout() {
  const colorScheme = useColorScheme();
  const { authState, loading } = useAuth();
  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      SplashScreen.hideAsync();
    }
  }, [loading]);

  useEffect(() => {
    if (loading) return;

    const inAuthGroup = segments[0] === '(auth)';

    if (authState.authenticated && inAuthGroup) {
      router.replace('/(tabs)');
    } else if (!authState.authenticated && !inAuthGroup) {
      router.replace('/(auth)/login');
    }
  }, [authState.authenticated, loading, segments]);

  if (loading) {
    return null;
  }

  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="(auth)/login" options={{ headerShown: false }} />
        <Stack.Screen name="(auth)/signup" options={{ headerShown: false }} />
        <Stack.Screen name="add-user" options={{ headerShown: false }} />
        <Stack.Screen name="edit-user/[id]" options={{ headerShown: false }} />
        <Stack.Screen name="edit-profile" options={{ headerShown: false }} />
        <Stack.Screen name="registro-humor" options={{ headerShown: false }} />
        <Stack.Screen name="meditacao/[id]" options={{ headerShown: false }} />
        <Stack.Screen name="avaliacao/[id]" options={{ headerShown: false }} />
        <Stack.Screen name="modal" options={{ headerShown: false, presentation: 'modal' }} />
      </Stack>
    </ThemeProvider>
  );
}

export default function RootLayout() {
  return (
    <AuthProvider>
      <InitialLayout />
    </AuthProvider>
  );
}
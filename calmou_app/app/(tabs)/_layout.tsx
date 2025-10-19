// app/(tabs)/_layout.tsx

import { Tabs } from 'expo-router';
import React from 'react';

import { TabBarIcon } from '../../components/navigation/TabBarIcon';
import { Colors } from '../../constants/theme';
import { useColorScheme } from '../../hooks/use-color-scheme';

export default function TabLayout() {
  const colorScheme = useColorScheme();

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: Colors[colorScheme ?? 'light'].tint,
        headerShown: false,
      }}>
      <Tabs.Screen
        name="index"
        options={{ title: 'Início', tabBarIcon: ({ color, focused }) => <TabBarIcon name={focused ? 'home' : 'home-outline'} color={color} /> }}
      />
      <Tabs.Screen
        name="meditacoes"
        options={{ title: 'Meditar', tabBarIcon: ({ color, focused }) => <TabBarIcon name={focused ? 'leaf' : 'leaf-outline'} color={color} /> }}
      />
      <Tabs.Screen
        name="avaliacoes"
        options={{ title: 'Avaliações', tabBarIcon: ({ color, focused }) => <TabBarIcon name={focused ? 'clipboard' : 'clipboard-outline'} color={color} /> }}
      />

      {/* ===== ABA "EXPLORE" TROCADA PELA "PERFIL" ===== */}
      <Tabs.Screen
        name="historico" // Nome do arquivo que acabamos de renomear
        options={{
          title: 'Histórico',
          tabBarIcon: ({ color, focused }) => (
            <TabBarIcon name={focused ? 'archive' : 'archive-outline'} color={color} />
          ),
        }}
      />
      {/* ============================================== */}
    </Tabs>
  );
}
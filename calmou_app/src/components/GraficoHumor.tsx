import React from 'react';
import { Dimensions, StyleSheet, Text, View } from 'react-native';
import { LineChart } from 'react-native-chart-kit';

type GraficoHumorProps = {
  data: {
    labels: string[];
    datasets: { data: number[] }[];
  };
};

const GraficoHumor = ({ data }: GraficoHumorProps) => {
  if (!data || data.labels.length === 0) {
    return (
      <View style={styles.placeholder}>
        <Text style={styles.placeholderText}>Sem dados de humor na última semana.</Text>
      </View>
    );
  }

  return (
    <View>
      <LineChart
        data={data}
        width={Dimensions.get('window').width - 40}
        height={220}
        chartConfig={{
          backgroundColor: '#ffffff',
          backgroundGradientFrom: '#ffffff',
          backgroundGradientTo: '#ffffff',
          decimalPlaces: 0,
          color: (opacity = 1) => `rgba(10, 126, 164, ${opacity})`,
          labelColor: (opacity = 1) => `rgba(100, 100, 100, ${opacity})`,
          style: { borderRadius: 16 },
          propsForDots: { r: '6', strokeWidth: '2', stroke: '#0a7ea4' },
        }}
        bezier
        style={{ marginVertical: 8, borderRadius: 16, marginRight: 20 }}
      />
    </View>
  );
};

const styles = StyleSheet.create({
    placeholder: { 
        height: 150, 
        justifyContent: 'center', 
        alignItems: 'center', 
        backgroundColor: 'white', 
        marginRight: 20, 
        borderRadius: 10, 
    },
    placeholderText: { 
        color: '#ccc', 
        fontSize: 16 
    },
});

export default GraficoHumor;
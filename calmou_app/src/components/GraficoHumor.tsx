import React from 'react';
import { Dimensions, StyleSheet, Text, View } from 'react-native';
import Svg, { Circle, Defs, Line, LinearGradient, Path, Stop, Text as SvgText } from 'react-native-svg';

type GraficoHumorProps = {
  data: {
    labels: string[];
    datasets: { data: number[] }[];
  };
};

// Função para retornar cor baseada no nível de humor (1-5)
const getColorForMood = (nivel: number): string => {
  if (nivel === 1) return '#EF4444'; // Vermelho - Muito baixo
  if (nivel === 2) return '#F97316'; // Laranja - Baixo
  if (nivel === 3) return '#EAB308'; // Amarelo - Neutro
  if (nivel === 4) return '#84CC16'; // Verde claro - Bom
  return '#22C55E'; // Verde escuro - Excelente (nível 5)
};

const GraficoHumor = ({ data }: GraficoHumorProps) => {
  if (!data || data.labels.length === 0) {
    return (
      <View style={styles.placeholder}>
        <Text style={styles.placeholderText}>Sem dados de humor na última semana.</Text>
      </View>
    );
  }

  const dataPoints = data.datasets[0]?.data || [];
  const labels = data.labels;

  const width = Dimensions.get('window').width - 60;
  const height = 240;
  const padding = { top: 20, right: 20, bottom: 40, left: 40 };
  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;

  // Calcular posições dos pontos
  const maxValue = 5; // Máximo valor de humor
  const minValue = 1; // Mínimo valor de humor
  const stepX = chartWidth / (dataPoints.length - 1 || 1);

  const points = dataPoints.map((value, index) => {
    const x = padding.left + index * stepX;
    const y = padding.top + chartHeight - ((value - minValue) / (maxValue - minValue)) * chartHeight;
    return { x, y, value };
  });

  // Criar path suave (curva Bezier)
  const createSmoothPath = () => {
    if (points.length === 0) return '';

    let path = `M ${points[0].x} ${points[0].y}`;

    for (let i = 0; i < points.length - 1; i++) {
      const current = points[i];
      const next = points[i + 1];
      const midX = (current.x + next.x) / 2;

      path += ` Q ${current.x} ${current.y}, ${midX} ${(current.y + next.y) / 2}`;
      path += ` Q ${next.x} ${next.y}, ${next.x} ${next.y}`;
    }

    return path;
  };

  return (
    <View style={styles.container}>
      <View style={styles.chartCard}>
        <Svg width={width} height={height}>
          <Defs>
            {/* Definir gradientes para cada segmento */}
            {points.map((point, index) => {
              if (index === points.length - 1) return null;
              const nextPoint = points[index + 1];
              return (
                <LinearGradient
                  key={`gradient-${index}`}
                  id={`gradient-${index}`}
                  x1="0%"
                  y1="0%"
                  x2="100%"
                  y2="0%"
                >
                  <Stop offset="0%" stopColor={getColorForMood(point.value)} stopOpacity="1" />
                  <Stop offset="100%" stopColor={getColorForMood(nextPoint.value)} stopOpacity="1" />
                </LinearGradient>
              );
            })}
          </Defs>

          {/* Linhas de fundo horizontais */}
          {[1, 2, 3, 4, 5].map((value) => {
            const y = padding.top + chartHeight - ((value - minValue) / (maxValue - minValue)) * chartHeight;
            return (
              <React.Fragment key={`grid-${value}`}>
                <Line
                  x1={padding.left}
                  y1={y}
                  x2={padding.left + chartWidth}
                  y2={y}
                  stroke="#e2e8f0"
                  strokeWidth="1"
                />
                <SvgText
                  x={padding.left - 10}
                  y={y + 4}
                  fontSize="12"
                  fill="#64748b"
                  textAnchor="end"
                >
                  {value}
                </SvgText>
              </React.Fragment>
            );
          })}

          {/* Desenhar linha com gradiente suave */}
          <Path
            d={createSmoothPath()}
            stroke="url(#gradient-0)"
            strokeWidth="3"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
          />

          {/* Desenhar segmentos coloridos individuais */}
          {points.map((point, index) => {
            if (index === points.length - 1) return null;
            const nextPoint = points[index + 1];
            return (
              <Line
                key={`segment-${index}`}
                x1={point.x}
                y1={point.y}
                x2={nextPoint.x}
                y2={nextPoint.y}
                stroke={`url(#gradient-${index})`}
                strokeWidth="4"
                strokeLinecap="round"
              />
            );
          })}

          {/* Desenhar pontos */}
          {points.map((point, index) => (
            <Circle
              key={`point-${index}`}
              cx={point.x}
              cy={point.y}
              r="10"
              fill={getColorForMood(point.value)}
              stroke="#ffffff"
              strokeWidth="3"
            />
          ))}

          {/* Labels do eixo X */}
          {labels.map((label, index) => {
            const x = padding.left + index * stepX;
            return (
              <SvgText
                key={`label-${index}`}
                x={x}
                y={height - 10}
                fontSize="11"
                fill="#64748b"
                textAnchor="middle"
              >
                {label}
              </SvgText>
            );
          })}
        </Svg>
      </View>

      {/* Legenda de cores */}
      <View style={styles.legendContainer}>
        <Text style={styles.legendTitle}>Escala de Humor:</Text>
        <View style={styles.legendItems}>
          <View style={styles.legendItem}>
            <View style={[styles.legendDot, { backgroundColor: '#EF4444' }]} />
            <Text style={styles.legendText}>1</Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendDot, { backgroundColor: '#F97316' }]} />
            <Text style={styles.legendText}>2</Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendDot, { backgroundColor: '#EAB308' }]} />
            <Text style={styles.legendText}>3</Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendDot, { backgroundColor: '#84CC16' }]} />
            <Text style={styles.legendText}>4</Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendDot, { backgroundColor: '#22C55E' }]} />
            <Text style={styles.legendText}>5</Text>
          </View>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginRight: 20,
  },
  chartCard: {
    backgroundColor: '#ffffff',
    borderRadius: 20,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 8,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  legendContainer: {
    backgroundColor: '#f8fafc',
    borderRadius: 16,
    padding: 16,
    marginTop: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.05,
    shadowRadius: 6,
    elevation: 3,
  },
  legendTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#475569',
    marginBottom: 12,
    textAlign: 'center',
  },
  legendItems: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
  },
  legendItem: {
    alignItems: 'center',
    gap: 6,
  },
  legendDot: {
    width: 16,
    height: 16,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: '#ffffff',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 2,
  },
  legendText: {
    fontSize: 11,
    fontWeight: '600',
    color: '#64748b',
  },
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
<template>
  <div class="stock-chart">
    <h3>📈 주가 차트</h3>
    
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.value"
        :class="{ active: selectedPeriod === tab.value }"
        @click="changePeriod(tab.value)"
      >
        {{ tab.label }}
      </button>
    </div>

    <div v-if="loading" class="loading">차트 로딩 중...</div>
    <canvas v-else ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, defineProps } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const props = defineProps({
  stockCode: String,
  stockName: String
});

const emit = defineEmits(['periodChange']);

const chartCanvas = ref(null);
const selectedPeriod = ref('D');
const loading = ref(false);
let chartInstance = null;

const tabs = [
  { label: '1개월', value: 'D' },
  { label: '3개월', value: 'W' },
  { label: '1년', value: 'M' },
  { label: '3년', value: 'Y' }
];

const changePeriod = (period) => {
  selectedPeriod.value = period;
  emit('periodChange', period);
};

const drawChart = (chartData) => {
  if (!chartCanvas.value) return;

  if (chartInstance) {
    chartInstance.destroy();
  }

  const ctx = chartCanvas.value.getContext('2d');
  
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: chartData.labels,
      datasets: [{
        label: '종가',
        data: chartData.prices,
        borderColor: '#4CAF50',
        backgroundColor: 'rgba(76, 175, 80, 0.1)',
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true
        }
      },
      scales: {
        y: {
          beginAtZero: false
        }
      }
    }
  });
};

defineExpose({ drawChart });
</script>

<style scoped>
.stock-chart {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 10px;
}

.tabs {
  display: flex;
  gap: 10px;
  margin: 20px 0;
}

.tabs button {
  padding: 10px 20px;
  background: #2d2d2d;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.tabs button.active {
  background: #4CAF50;
}

.loading {
  text-align: center;
  padding: 50px;
  color: #888;
}

canvas {
  max-height: 400px;
}
</style>

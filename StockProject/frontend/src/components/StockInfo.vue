<template>
  <div v-if="stockData" class="stock-info">
    <h2>📊 {{ stockName }} ({{ stockCode }})</h2>
    <p class="sector">업종: {{ stockData.bstp_kor_isnm }}</p>

    <div class="metrics">
      <div class="metric-card">
        <h3>현재가</h3>
        <p class="price">{{ formatNumber(stockData.stck_prpr) }}원</p>
      </div>

      <div class="metric-card">
        <h3>전일대비</h3>
        <p :class="changeClass">
          {{ formatChange(stockData.prdy_vrss) }}원
          ({{ formatChange(stockData.prdy_ctrt) }}%)
        </p>
      </div>

      <div class="metric-card">
        <h3>시가</h3>
        <p>{{ formatNumber(stockData.stck_oprc) }}원</p>
      </div>

      <div class="metric-card">
        <h3>거래량</h3>
        <p>{{ formatNumber(stockData.acml_vol) }}주</p>
      </div>
    </div>

    <div class="details">
      <h3>상세 정보</h3>
      <div class="detail-grid">
        <div>고가: <strong>{{ formatNumber(stockData.stck_hgpr) }}원</strong></div>
        <div>저가: <strong>{{ formatNumber(stockData.stck_lwpr) }}원</strong></div>
        <div>52주 최고가: <strong>{{ formatNumber(stockData.w52_hgpr) }}원</strong></div>
        <div>52주 최저가: <strong>{{ formatNumber(stockData.w52_lwpr) }}원</strong></div>
      </div>
    </div>

    <div class="indicators">
      <h3>투자지표</h3>
      <div class="indicator-grid">
        <div>PER: <strong>{{ stockData.per }}</strong></div>
        <div>PBR: <strong>{{ stockData.pbr }}</strong></div>
        <div>EPS: <strong>{{ formatNumber(stockData.eps) }}원</strong></div>
        <div>BPS: <strong>{{ formatNumber(stockData.bps) }}원</strong></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps } from 'vue';

const props = defineProps({
  stockData: Object,
  stockCode: String,
  stockName: String
});

const changeClass = computed(() => {
  const change = parseInt(props.stockData?.prdy_vrss || 0);
  return change > 0 ? 'positive' : change < 0 ? 'negative' : '';
});

const formatNumber = (num) => {
  return parseInt(num).toLocaleString();
};

const formatChange = (num) => {
  const value = parseFloat(num);
  return value > 0 ? `+${value.toLocaleString()}` : value.toLocaleString();
};
</script>

<style scoped>
.stock-info {
  background: #1e1e1e;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.sector {
  color: #888;
  margin-bottom: 20px;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin: 20px 0;
}

.metric-card {
  background: #2d2d2d;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.metric-card h3 {
  font-size: 14px;
  color: #888;
  margin-bottom: 10px;
}

.price {
  font-size: 24px;
  font-weight: bold;
  color: white;
}

.positive {
  color: #f44336;
}

.negative {
  color: #2196F3;
}

.details, .indicators {
  margin-top: 30px;
}

.detail-grid, .indicator-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.detail-grid div, .indicator-grid div {
  padding: 10px;
  background: #2d2d2d;
  border-radius: 5px;
}
</style>

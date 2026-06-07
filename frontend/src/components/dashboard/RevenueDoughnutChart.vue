<script setup lang="ts">
import { Chart } from 'chart.js'
import { onMounted, onUnmounted, useTemplateRef, watch } from 'vue'

import type { ServiceRevenue } from '@/api/types'

const props = defineProps<{ data: ServiceRevenue[] }>()

const canvas = useTemplateRef<HTMLCanvasElement>('canvas')
let chart: Chart | null = null

// Тёплая палитра в тон бронзовой темы.
const palette = ['#B8763C', '#D88D4C', '#8A6A45', '#C9A06A', '#6E4F30', '#E0A968']

function render() {
  if (!canvas.value) {
    return
  }
  chart?.destroy()
  chart = new Chart(canvas.value, {
    type: 'doughnut',
    data: {
      labels: props.data.map(d => d.service),
      datasets: [{
        data: props.data.map(d => d.revenue),
        backgroundColor: palette,
        borderColor: '#1A1816',
        borderWidth: 2,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { color: '#F2EBDD', boxWidth: 12, padding: 12 } },
      },
    },
  })
}

onMounted(render)
watch(() => props.data, render)
onUnmounted(() => chart?.destroy())
</script>

<template>
  <div class="chart-wrap">
    <canvas ref="canvas" />
  </div>
</template>

<style scoped>
.chart-wrap {
  position: relative;
  height: 320px;
}
</style>

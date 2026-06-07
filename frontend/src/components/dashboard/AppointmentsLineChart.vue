<script setup lang="ts">
import { Chart } from 'chart.js'
import { onMounted, onUnmounted, useTemplateRef, watch } from 'vue'

import type { DayCount } from '@/api/types'

const props = defineProps<{ data: DayCount[] }>()

const canvas = useTemplateRef<HTMLCanvasElement>('canvas')
let chart: Chart | null = null

function dayLabel(iso: string): string {
  const [, month, day] = iso.split('-')
  return `${day}.${month}`
}

function render() {
  if (!canvas.value) {
    return
  }
  chart?.destroy()
  chart = new Chart(canvas.value, {
    type: 'line',
    data: {
      labels: props.data.map(d => dayLabel(d.day)),
      datasets: [{
        label: 'Записей',
        data: props.data.map(d => d.count),
        borderColor: '#B8763C',
        backgroundColor: 'rgba(184, 118, 60, 0.15)',
        fill: true,
        tension: 0.35,
        pointRadius: 3,
        pointBackgroundColor: '#D88D4C',
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { precision: 0, color: '#8A8378' }, grid: { color: 'rgba(138, 131, 120, 0.12)' } },
        x: { ticks: { color: '#8A8378' }, grid: { display: false } },
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

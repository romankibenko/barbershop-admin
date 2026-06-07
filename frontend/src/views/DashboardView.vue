<script setup lang="ts">
import { onMounted } from 'vue'

import AppointmentsLineChart from '@/components/dashboard/AppointmentsLineChart.vue'
import KpiCards from '@/components/dashboard/KpiCards.vue'
import RevenueDoughnutChart from '@/components/dashboard/RevenueDoughnutChart.vue'
import { useStats } from '@/composables/useStats'

const { stats, loading, load } = useStats()

onMounted(load)
</script>

<template>
  <div>
    <h1 class="text-h4 mb-6">Дашборд</h1>

    <template v-if="stats">
      <KpiCards :kpi="stats.kpi" />

      <v-row class="mt-2">
        <v-col cols="12" md="7">
          <v-card class="pa-4" color="surface" height="100%">
            <div class="text-subtitle-1 mb-4">Записи за 14 дней</div>
            <AppointmentsLineChart :data="stats.by_day" />
          </v-card>
        </v-col>
        <v-col cols="12" md="5">
          <v-card class="pa-4" color="surface" height="100%">
            <div class="text-subtitle-1 mb-4">Выручка по услугам</div>
            <RevenueDoughnutChart :data="stats.by_service" />
          </v-card>
        </v-col>
      </v-row>
    </template>

    <v-progress-linear v-else-if="loading" indeterminate color="primary" />
  </div>
</template>

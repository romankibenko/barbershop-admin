<script setup lang="ts">
import { computed } from 'vue'

import type { StatsKpi } from '@/api/types'
import { formatPrice } from '@/utils/format'

const props = defineProps<{ kpi: StatsKpi }>()

const cards = computed(() => [
  { label: 'Записей сегодня', value: String(props.kpi.appointments_today), icon: 'mdi-calendar-today' },
  { label: 'Выручка за месяц', value: formatPrice(props.kpi.revenue_month), icon: 'mdi-cash-multiple' },
  { label: 'Новых клиентов', value: String(props.kpi.new_clients_month), icon: 'mdi-account-plus' },
  { label: 'Всего клиентов', value: String(props.kpi.total_clients), icon: 'mdi-account-group' },
])
</script>

<template>
  <v-row>
    <v-col v-for="card in cards" :key="card.label" cols="12" sm="6" md="3">
      <v-card class="pa-4" color="surface" height="100%">
        <div class="d-flex align-center mb-2">
          <v-icon :icon="card.icon" color="primary" size="28" class="mr-2" />
          <span class="text-medium-emphasis text-caption text-uppercase">{{ card.label }}</span>
        </div>
        <div class="text-h5 font-weight-bold">
          {{ card.value }}
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

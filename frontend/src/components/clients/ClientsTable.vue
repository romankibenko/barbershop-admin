<script setup lang="ts">
import type { Client } from '@/api/types'
import { formatDate } from '@/utils/format'

defineProps<{
  items: Client[]
  total: number
  loading: boolean
  search: string
}>()

const emit = defineEmits<{
  load: [options: { page: number, itemsPerPage: number }]
  edit: [client: Client]
  remove: [client: Client]
}>()

const headers = [
  { title: 'Имя', key: 'name' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Заметки', key: 'notes', sortable: false },
  { title: 'Создан', key: 'created_at' },
  { title: '', key: 'actions', sortable: false, align: 'end' as const },
]
</script>

<template>
  <v-data-table-server
    :headers="headers"
    :items="items"
    :items-length="total"
    :loading="loading"
    :search="search"
    :items-per-page="20"
    @update:options="emit('load', $event)"
  >
    <template #item.notes="{ item }">
      {{ item.notes || '—' }}
    </template>
    <template #item.created_at="{ item }">
      {{ formatDate(item.created_at) }}
    </template>
    <template #item.actions="{ item }">
      <v-btn icon="mdi-pencil" size="small" variant="text" @click="emit('edit', item)" />
      <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="emit('remove', item)" />
    </template>
  </v-data-table-server>
</template>

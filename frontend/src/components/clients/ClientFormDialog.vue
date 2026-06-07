<script setup lang="ts">
import { computed, ref, watch } from 'vue'

import type { Client } from '@/api/types'
import type { ClientPayload } from '@/composables/useClients'

const open = defineModel<boolean>({ required: true })

const props = defineProps<{ client: Client | null }>()

const emit = defineEmits<{
  save: [payload: ClientPayload]
}>()

const name = ref('')
const phone = ref('')
const notes = ref('')

const isEdit = computed(() => props.client !== null)
const valid = computed(() => name.value.trim().length >= 2 && phone.value.trim().length >= 5)

// Заполняем поля при открытии (создание — пусто, правка — данные клиента).
watch(open, (isOpen) => {
  if (isOpen) {
    name.value = props.client?.name ?? ''
    phone.value = props.client?.phone ?? ''
    notes.value = props.client?.notes ?? ''
  }
})

function submit() {
  emit('save', {
    name: name.value.trim(),
    phone: phone.value.trim(),
    notes: notes.value.trim() || null,
  })
}
</script>

<template>
  <v-dialog v-model="open" max-width="480">
    <v-card>
      <v-card-title>{{ isEdit ? 'Редактировать клиента' : 'Новый клиент' }}</v-card-title>
      <v-card-text>
        <v-text-field v-model="name" label="Имя" variant="outlined" class="mb-2" />
        <v-text-field v-model="phone" label="Телефон" variant="outlined" class="mb-2" />
        <v-textarea v-model="notes" label="Заметки" variant="outlined" rows="2" />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click="open = false">Отмена</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="submit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

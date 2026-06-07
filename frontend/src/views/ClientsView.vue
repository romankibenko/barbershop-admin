<script setup lang="ts">
import { ref, shallowRef } from 'vue'

import type { Client } from '@/api/types'
import ClientFormDialog from '@/components/clients/ClientFormDialog.vue'
import ClientsTable from '@/components/clients/ClientsTable.vue'
import type { ClientPayload } from '@/composables/useClients'
import { useClients } from '@/composables/useClients'

const { items, total, loading, load, create, update, remove } = useClients()

const search = shallowRef('')
const lastOptions = { page: 1, itemsPerPage: 20 }

const dialogOpen = ref(false)
const editing = shallowRef<Client | null>(null)

const confirmOpen = ref(false)
const removing = shallowRef<Client | null>(null)

function onLoad(options: { page: number, itemsPerPage: number }) {
  lastOptions.page = options.page
  lastOptions.itemsPerPage = options.itemsPerPage
  load({ ...options, search: search.value })
}

function reload() {
  load({ ...lastOptions, search: search.value })
}

function openCreate() {
  editing.value = null
  dialogOpen.value = true
}

function openEdit(client: Client) {
  editing.value = client
  dialogOpen.value = true
}

async function onSave(payload: ClientPayload) {
  if (editing.value) {
    await update(editing.value.id, payload)
  }
  else {
    await create(payload)
  }
  dialogOpen.value = false
  reload()
}

function askRemove(client: Client) {
  removing.value = client
  confirmOpen.value = true
}

async function confirmRemove() {
  if (removing.value) {
    await remove(removing.value.id)
  }
  confirmOpen.value = false
  reload()
}
</script>

<template>
  <div>
    <div class="d-flex align-center mb-6">
      <h1 class="text-h4">Клиенты</h1>
      <v-spacer />
      <v-btn color="primary" prepend-icon="mdi-plus" @click="openCreate">
        Добавить
      </v-btn>
    </div>

    <v-text-field
      v-model="search"
      label="Поиск по имени или телефону"
      prepend-inner-icon="mdi-magnify"
      variant="outlined"
      density="comfortable"
      clearable
      class="mb-4"
    />

    <v-card color="surface">
      <ClientsTable
        :items="items"
        :total="total"
        :loading="loading"
        :search="search"
        @load="onLoad"
        @edit="openEdit"
        @remove="askRemove"
      />
    </v-card>

    <ClientFormDialog v-model="dialogOpen" :client="editing" @save="onSave" />

    <v-dialog v-model="confirmOpen" max-width="400">
      <v-card>
        <v-card-title>Удалить клиента?</v-card-title>
        <v-card-text>
          {{ removing?.name }} — действие необратимо.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="confirmOpen = false">Отмена</v-btn>
          <v-btn color="error" @click="confirmRemove">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

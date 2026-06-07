<script setup lang="ts">
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const navItems = [
  { title: 'Дашборд', icon: 'mdi-view-dashboard', to: { name: 'dashboard' } },
  { title: 'Клиенты', icon: 'mdi-account-group', to: { name: 'clients' } },
  { title: 'Записи', icon: 'mdi-calendar-clock', to: { name: 'appointments' } },
]

function logout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <v-navigation-drawer permanent color="surface">
    <div class="brand">
      BRICK <span class="brand-accent">&amp;</span> RAZOR
    </div>
    <v-list nav density="comfortable">
      <v-list-item
        v-for="item in navItems"
        :key="item.title"
        :to="item.to"
        :prepend-icon="item.icon"
        :title="item.title"
      />
    </v-list>
  </v-navigation-drawer>

  <v-app-bar flat color="surface">
    <v-app-bar-title>Админ-панель</v-app-bar-title>
    <v-spacer />
    <v-btn variant="text" prepend-icon="mdi-logout" @click="logout">
      Выйти
    </v-btn>
  </v-app-bar>

  <v-main>
    <v-container fluid class="pa-6">
      <router-view />
    </v-container>
  </v-main>
</template>

<style scoped>
.brand {
  padding: 1.25rem 1.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: 0.2em;
}

.brand-accent {
  color: rgb(var(--v-theme-primary));
}
</style>

<script setup lang="ts">
import { shallowRef } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = shallowRef('')
const password = shallowRef('')
const loading = shallowRef(false)
const error = shallowRef('')

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    router.push({ name: 'dashboard' })
  }
  catch {
    error.value = 'Неверный логин или пароль'
  }
  finally {
    loading.value = false
  }
}
</script>

<template>
  <v-container class="fill-height justify-center">
    <v-card class="login-card pa-8" width="100%" max-width="420" elevation="8">
      <div class="brand text-center mb-2">
        BRICK <span class="brand-accent">&amp;</span> RAZOR
      </div>
      <p class="text-center text-medium-emphasis mb-6">
        Админ-панель
      </p>

      <v-form @submit.prevent="submit">
        <v-text-field
          v-model="username"
          label="Логин"
          prepend-inner-icon="mdi-account"
          variant="outlined"
          autocomplete="username"
          class="mb-2"
        />
        <v-text-field
          v-model="password"
          label="Пароль"
          type="password"
          prepend-inner-icon="mdi-lock"
          variant="outlined"
          autocomplete="current-password"
        />

        <v-alert
          v-if="error"
          type="error"
          variant="tonal"
          density="compact"
          class="mb-4"
        >
          {{ error }}
        </v-alert>

        <v-btn
          type="submit"
          color="primary"
          size="large"
          block
          :loading="loading"
        >
          Войти
        </v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<style scoped>
.brand {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: 0.2em;
}

.brand-accent {
  color: rgb(var(--v-theme-primary));
}
</style>

import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

import { createVuetify } from 'vuetify'

// Фирменная палитра Brick & Razor — синхрон с лендингом (src/style.css @theme).
const brickRazor = {
  dark: true,
  colors: {
    background: '#0F0E0C',
    surface: '#1A1816',
    'surface-bright': '#24211D',
    primary: '#B8763C',
    secondary: '#8A8378',
    error: '#E5484D',
    info: '#8A8378',
    success: '#46A758',
    warning: '#D88D4C',
    'on-background': '#F2EBDD',
    'on-surface': '#F2EBDD',
  },
}

export default createVuetify({
  theme: {
    defaultTheme: 'brickRazor',
    themes: { brickRazor },
  },
})

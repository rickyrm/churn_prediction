<template>
  <div class="max-w-md mx-auto bg-white shadow-xl rounded-2xl p-6 mt-10">
    <h1 class="text-2xl font-bold mb-4 text-center text-gray-700">
      Predicción de Fuga de Clientes
    </h1>

    <form @submit.prevent="enviarPrediccion" class="space-y-4">
      <div>
        <label class="block text-gray-600 mb-1">Edad</label>
        <input v-model.number="form.edad" type="number" class="w-full p-2 border rounded-md" required />
      </div>

      <div>
        <label class="block text-gray-600 mb-1">Ingresos</label>
        <input v-model.number="form.ingresos" type="number" class="w-full p-2 border rounded-md" required />
      </div>

      <div>
        <label class="block text-gray-600 mb-1">Antigüedad (meses)</label>
        <input v-model.number="form.antiguedad_meses" type="number" class="w-full p-2 border rounded-md" required />
      </div>

      <div>
        <label class="block text-gray-600 mb-1">Número de productos</label>
        <input v-model.number="form.num_productos" type="number" class="w-full p-2 border rounded-md" required />
      </div>

      <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition">
        Predecir
      </button>
    </form>

    <div v-if="resultado" class="mt-6 text-center">
      <p class="text-lg font-semibold">
        Resultado: <span :class="colorResultado">{{ resultado }}</span>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const form = ref({
  edad: null,
  ingresos: null,
  antiguedad_meses: null,
  num_productos: null
})

const resultado = ref(null)

const enviarPrediccion = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/predecir', form.value)
    resultado.value = response.data.resultado
  } catch (error) {
    resultado.value = 'Error en la conexión con el servidor'
    console.error(error)
  }
}

const colorResultado = computed(() =>
  resultado.value === 'Abandona' ? 'text-red-600' : 'text-green-600'
)
</script>

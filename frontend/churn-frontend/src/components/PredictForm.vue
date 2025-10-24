<template>
  <div class="container">
    <div class="header">
      <h2>Panel de Predicción de Churn</h2>
      <button class="logout-btn" @click="logout">Cerrar Sesión</button>
    </div>

    <form @submit.prevent="submitPrediction" class="form-card">
      <div class="form-group">
        <label>ID Cliente</label>
        <input type="text" v-model="customer_id" required />
      </div>

      <div class="form-group">
        <label>Edad</label>
        <input type="number" v-model="edad" required />
      </div>

      <div class="form-group">
        <label>Ingresos</label>
        <input type="number" v-model="ingresos" required />
      </div>

      <div class="form-group">
        <label>Antigüedad (meses)</label>
        <input type="number" v-model="antiguedad_meses" required />
      </div>

      <div class="form-group">
        <label>Nº Productos</label>
        <input type="number" v-model="num_productos" required />
      </div>

      <button class="btn-primary" type="submit">Predecir</button>
    </form>

    <!-- Tabla de registros -->
    <h3>Historial de Predicciones</h3>
    <table v-if="predictions.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Cliente</th>
          <th>Edad</th>
          <th>Ingresos</th>
          <th>Antigüedad</th>
          <th>Productos</th>
          <th>Churn</th>
          <th>Probabilidad</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in predictions" :key="p.id">
          <td>{{ p.id }}</td>
          <td>{{ p.customer_id }}</td>
          <td>{{ parseData(p).edad }}</td>
          <td>{{ parseData(p).ingresos }}</td>
          <td>{{ parseData(p).antiguedad_meses }}</td>
          <td>{{ parseData(p).num_productos }}</td>
          <td>{{ p.prediction }}</td>
          <td>{{ (p.probability * 100).toFixed(2) }}%</td>
          <td>
            <button @click="openEdit(p)">✏️</button>
            <button @click="deleteRecord(p.id)">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>No hay predicciones</p>

    <!-- MODAL -->
    <div v-if="editItem" class="modal">
      <div class="modal-content">
        <h3>Editar Cliente {{ editItem.customer_id }}</h3>

        <label>Edad</label>
        <input type="number" v-model="editItem.edad" />

        <label>Ingresos</label>
        <input type="number" v-model="editItem.ingresos" />

        <label>Antigüedad</label>
        <input type="number" v-model="editItem.antiguedad_meses" />

        <label>Productos</label>
        <input type="number" v-model="editItem.num_productos" />

        <button @click="updateRecord">Guardar</button>
        <button @click="editItem=null">Cancelar</button>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "../api/axios"
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"

export default {
  name: "PredictForm",
  setup() {
    const router = useRouter()

    const customer_id = ref("")
    const edad = ref("")
    const ingresos = ref("")
    const antiguedad_meses = ref("")
    const num_productos = ref("")
    const predictions = ref([])
    const editItem = ref(null)

    const parseData = (p) =>
      typeof p.input_data === "string"
        ? JSON.parse(p.input_data)
        : p.input_data

    const fetchPredictions = async () => {
      const token = localStorage.getItem("token")
      const { data } = await axios.get("/predicciones", {
        headers: { Authorization: `Bearer ${token}` }
      })
      predictions.value = data
    }

    const submitPrediction = async () => {
      const exists = predictions.value.find(p => p.customer_id === customer_id.value)
      if (exists) return alert("⚠️ Cliente ya registrado")

      const token = localStorage.getItem("token")
      await axios.post("/predecir/", {
        customer_id: customer_id.value,
        input_data: {
          edad: Number(edad.value),
          ingresos: Number(ingresos.value),
          antiguedad_meses: Number(antiguedad_meses.value),
          num_productos: Number(num_productos.value)
        }
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })

      await fetchPredictions()
      customer_id.value = edad.value = ingresos.value = antiguedad_meses.value = num_productos.value = ""
    }

    const openEdit = (p) => {
      const input = parseData(p)
      editItem.value = {
        id: p.id,
        customer_id: p.customer_id,
        edad: input.edad,
        ingresos: input.ingresos,
        antiguedad_meses: input.antiguedad_meses,
        num_productos: input.num_productos
      }
    }

    const updateRecord = async () => {
      const token = localStorage.getItem("token")
      await axios.put(`/predicciones/${editItem.value.id}`, {
        input_data: {
          edad: Number(editItem.value.edad),
          ingresos: Number(editItem.value.ingresos),
          antiguedad_meses: Number(editItem.value.antiguedad_meses),
          num_productos: Number(editItem.value.num_productos)
        }
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })

      editItem.value = null
      fetchPredictions()
    }

    const deleteRecord = async (id) => {
      const token = localStorage.getItem("token")
      await axios.delete(`/predicciones/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      fetchPredictions()
    }

    const logout = () => {
      localStorage.removeItem("token")
      router.push("/")
    }

    onMounted(fetchPredictions)

    return {
      customer_id, edad, ingresos, antiguedad_meses, num_productos,
      predictions, editItem,
      parseData,
      submitPrediction, updateRecord, deleteRecord,
      openEdit, logout
    }
  }
}
</script>


<style scoped>
.container {
  max-width: 900px;
  margin: 40px auto;
  background: #ffffff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logout-btn {
  background: #e74c3c;
  color: #fff;
  border: none;
  padding: 10px 14px;
  border-radius: 6px;
  cursor: pointer;
}

.logout-btn:hover {
  background: #c0392b;
}

h2,
h3 {
  color: #34495e;
}

.form-card {
  margin-bottom: 25px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 4px;
}

input {
  padding: 10px;
  border: 1px solid #ccd1d9;
  border-radius: 6px;
}

.btn-primary {
  grid-column: span 2;
  background: #3498db;
  color: #fff;
  padding: 12px;
  font-size: 15px;
  border-radius: 6px;
  cursor: pointer;
}

.btn-primary:hover {
  background: #2980b9;
}

.table-container {
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

thead {
  background-color: #ecf0f1;
}

th,
td {
  padding: 12px;
  border-bottom: 1px solid #dcdcdc;
}

.no-data {
  text-align: center;
  color: #7f8c8d;
  font-style: italic;
}
</style>

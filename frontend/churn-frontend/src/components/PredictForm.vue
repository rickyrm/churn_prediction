<template>
  <div class="container">
    <div class="header">
      <h2>Panel de Predicción de Churn</h2>
      <button class="logout-btn" @click="logout">Cerrar Sesión</button>
    </div>

    <!-- === PANEL DE MÉTRICAS === -->
    <div class="kpi-grid" v-if="stats.total > 0">
      <div class="kpi-card total">
        <h3>Total Predicciones</h3>
        <p>{{ stats.total }}</p>
      </div>
      <div class="kpi-card churn">
        <h3>Clientes que Abandonan</h3>
        <p>{{ stats.abandona }}</p>
      </div>
      <div class="kpi-card stay">
        <h3>Clientes que Permancen</h3>
        <p>{{ stats.permanece }}</p>
      </div>
    </div>

    <!-- === GRÁFICO === -->
    <div class="chart-container" v-if="stats.total > 0">
      <canvas id="churnChart"></canvas>
    </div>

    <!-- === FORMULARIO === -->
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

    <!-- === TABLA === -->
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
            <button @click="openEdit(p)" class="action-btn edit">✏️</button>
            <button @click="deleteRecord(p.id)" class="action-btn delete">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else class="no-data">No hay predicciones</p>

    <!-- === MODAL === -->
    <div v-if="editItem" class="modal">
      <div class="modal-content">
        <h3>Editar Cliente {{ editItem.customer_id }}</h3>

        <div class="form-group">
          <label>Edad</label>
          <input type="number" v-model="editItem.edad" />
        </div>

        <div class="form-group">
          <label>Ingresos</label>
          <input type="number" v-model="editItem.ingresos" />
        </div>

        <div class="form-group">
          <label>Antigüedad (meses)</label>
          <input type="number" v-model="editItem.antiguedad_meses" />
        </div>

        <div class="form-group">
          <label>Número de productos</label>
          <input type="number" v-model="editItem.num_productos" />
        </div>

        <div class="modal-actions">
          <button class="btn-primary" @click="updateRecord">Guardar</button>
          <button class="btn-secondary" @click="editItem = null">Cancelar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../api/axios"
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import Chart from "chart.js/auto"

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
    const stats = ref({ total: 0, abandona: 0, permanece: 0 })

    let chartInstance = null

    const parseData = (p) =>
      typeof p.input_data === "string"
        ? JSON.parse(p.input_data)
        : p.input_data

    const calculateStats = () => {
      const total = predictions.value.length
      const abandona = predictions.value.filter(p => p.prediction === "Abandona").length
      const permanece = predictions.value.filter(p => p.prediction === "Permanece").length
      stats.value = { total, abandona, permanece }
      renderChart()
    }

    const renderChart = () => {
      const ctx = document.getElementById("churnChart")
      if (!ctx) return

      if (chartInstance) chartInstance.destroy()

      chartInstance = new Chart(ctx, {
        type: "pie",
        data: {
          labels: ["Abandonan", "Permancen"],
          datasets: [{
            data: [stats.value.abandona, stats.value.permanece],
            backgroundColor: ["#e74c3c", "#2ecc71"]
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: "bottom" }
          }
        }
      })
    }

    const fetchPredictions = async () => {
      const token = localStorage.getItem("token")
      const { data } = await axios.get("/predicciones", {
        headers: { Authorization: `Bearer ${token}` }
      })
      predictions.value = data
      calculateStats()
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
      predictions, editItem, stats,
      parseData,
      submitPrediction, updateRecord, deleteRecord,
      openEdit, logout
    }
  }
}
</script>

<style scoped>
/* === Layout principal === */
.container {
  max-width: 1000px;
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
  transition: 0.3s;
}
.logout-btn:hover {
  background: #c0392b;
}

/* === KPI Dashboard === */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  margin: 20px 0;
}
.kpi-card {
  text-align: center;
  border-radius: 10px;
  padding: 20px;
  color: #fff;
  font-weight: bold;
}
.kpi-card.total { background-color: #3498db; }
.kpi-card.churn { background-color: #e74c3c; }
.kpi-card.stay { background-color: #2ecc71; }

.chart-container {
  margin: 20px auto;
  max-width: 400px;
}

/* === Formulario === */
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
.btn-primary:hover { background: #2980b9; }

/* === Tabla === */
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  margin-top: 10px;
}
thead { background-color: #ecf0f1; }
th, td {
  padding: 12px;
  border-bottom: 1px solid #dcdcdc;
  text-align: center;
}
.action-btn {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 16px;
}
.action-btn.edit:hover { color: #2980b9; }
.action-btn.delete:hover { color: #e74c3c; }

.no-data {
  text-align: center;
  color: #7f8c8d;
  font-style: italic;
  margin-top: 10px;
}

/* === Modal === */
.modal {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(52, 73, 94, 0.6);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}
.modal-content {
  background: #ffffff;
  padding: 30px 40px;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
  animation: fadeInUp 0.3s ease-out;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 25px;
}
.btn-secondary {
  background: #bdc3c7;
  color: #2c3e50;
  border: none;
  padding: 10px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
.btn-secondary:hover { background: #95a5a6; }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>


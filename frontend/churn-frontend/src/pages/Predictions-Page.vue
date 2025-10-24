<template>
  <div class="main-container">
    <h2>Registro de Predicciones</h2>

    <button class="logout-btn" @click="logout">Cerrar Sesión</button>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Cliente</th>
          <th>Resultado</th>
          <th>Probabilidad</th>
          <th>Datos</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in predictions" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.customer_id }}</td>
          <td>{{ item.prediction }}</td>
          <td>{{ (item.probability * 100).toFixed(2) }}%</td>
          <td>{{ item.input_data }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "../api/axios";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "Predictions-Page",
  setup() {
    const router = useRouter();
    const predictions = ref([]);

    const fetchData = async () => {
      try {
        const response = await axios.get("/predicciones");
        predictions.value = response.data;
      } catch  {
        alert("Autenticación requerida. Vuelva a iniciar sesión.");
        router.push("/");
      }
    };

    const logout = () => {
      localStorage.removeItem("token");
      router.push("/");
    };

    onMounted(() => {
      fetchData();
    });

    return { predictions, logout };
  }
};
</script>

<style scoped>
.main-container {
  padding: 20px;
}
table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}
thead {
  background-color: #f5f5f5;
}
th, td {
  padding: 10px;
  border: 1px solid #ccc;
}
.logout-btn {
  float: right;
  margin-bottom: 15px;
  background-color: #d9534f;
  color: #fff;
}
</style>

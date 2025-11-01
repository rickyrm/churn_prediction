## 🧠 **Sistema de Predicción de Churn**

### 📋 **Resumen del Proyecto**

El presente sistema permite **predecir la probabilidad de abandono de clientes (churn)** en base a características sociodemográficas y de comportamiento, como la edad, ingresos, antigüedad y número de productos contratados.

El objetivo es dotar al área de negocio de una herramienta visual, simple y escalable que permita:

* Realizar predicciones en tiempo real.
* Consultar y editar registros históricos.
* Analizar métricas agregadas mediante un panel visual de control.

El sistema está dividido en dos módulos:

1. **Backend (FastAPI + SQLModel)** → expone la API, gestiona autenticación, predicción y persistencia.
2. **Frontend (Vue 3 + Chart.js)** → interfaz web para captura, visualización y análisis de clientes.

---

### 🏗️ **Arquitectura General**

```
📦 churn-predictor
 ┣ 📂 backend/
 ┃ ┣ 📂 app/
 ┃ ┃ ┣ 📂 api/
 ┃ ┃ ┃ ┗ routes_predict.py
 ┃ ┃ ┣ 📂 core/
 ┃ ┃ ┣ 📂 database/
 ┃ ┃ ┣ 📂 models/
 ┃ ┃ ┣ 📂 services/
 ┃ ┃ ┗ main.py
 ┃ ┗ requirements.txt
 ┣ 📂 frontend/
 ┃ ┣ 📂 src/
 ┃ ┃ ┣ 📂 components/
 ┃ ┃ ┃ ┗ PredictForm.vue
 ┃ ┃ ┣ 📂 api/
 ┃ ┃ ┃ ┗ axios.js
 ┃ ┃ ┗ App.vue
 ┃ ┗ package.json
 ┗ README.md
```

---

### ⚙️ **Requisitos Previos**

#### 🧩 Backend:

* Python 3.10 o superior
* pip (administrador de paquetes)
* Base de datos SQLite (por defecto) o compatible con SQLModel
* FastAPI y librerías del entorno virtual

#### 💻 Frontend:

* Node.js ≥ 18
* npm o yarn

---

### 🚀 **Instalación y Ejecución**

#### 🧠 1. Clonar el proyecto

```bash
git clone https://github.com/tu-usuario/churn-predictor.git
cd churn-predictor
```

---

#### ⚙️ 2. Configurar y ejecutar el **Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Ejecutar el servidor FastAPI:

```bash
uvicorn app.main:app --reload
```

Por defecto se desplegará en:
📡 `http://127.0.0.1:8000`

Endpoints principales:

* `POST /predecir/` → realiza la predicción
* `GET /predicciones/` → consulta los registros
* `PUT /predicciones/{id}` → actualiza un cliente
* `DELETE /predicciones/{id}` → elimina un cliente

Documentación automática:

* Swagger UI → `http://127.0.0.1:8000/docs`
* Redoc → `http://127.0.0.1:8000/redoc`

---

#### 💻 3. Configurar y ejecutar el **Frontend**

```bash
cd ../frontend
npm install
npm run serve
```

Por defecto se desplegará en:
🌐 `http://localhost:5173/` (o el puerto que indique la consola)

> ⚠️ Importante: Asegúrese de que la URL base del backend esté configurada correctamente en
> `frontend/src/api/axios.js`

Ejemplo:

```js
import axios from "axios";
export default axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: { "Content-Type": "application/json" }
});
```

---

### 📊 **Características Principales**

| Funcionalidad                 | Descripción                                                       |
| ----------------------------- | ----------------------------------------------------------------- |
| 🔐 **Autenticación JWT**      | Seguridad de acceso a las rutas de predicción.                    |
| 🧾 **Formulario Inteligente** | Captura de datos cliente con validación.                          |
| 🧮 **Predicción Automática**  | Cálculo del riesgo de abandono mediante modelo ML.                |
| 📋 **Historial Dinámico**     | Tabla editable y eliminable de registros.                         |
| 📈 **Dashboard Analítico**    | KPIs de churn, gráfico circular interactivo y métricas agregadas. |
| 🧰 **API REST Documentada**   | Endpoints descritos en Swagger UI.                                |

---

### 🧠 **Modelo de Predicción**

El modelo se entrena sobre datos históricos de clientes.
Utiliza variables cuantitativas como:

* Edad
* Ingresos mensuales
* Antigüedad (en meses)
* Número de productos contratados

El modelo devuelve:

* `prediction`: `"Abandona"` o `"Permanece"`
* `probability`: probabilidad asociada (0 a 1)

---

### 🧩 **Tecnologías Utilizadas**

**Backend**

* FastAPI
* SQLModel
* Pydantic
* JWT Auth
* Uvicorn

**Frontend**

* Vue 3 (Composition API)
* Axios
* Chart.js
* Tailwind + CSS Custom

---

### 📈 **Próximas Mejoras**

* Integración con base de datos PostgreSQL o MySQL.
* Dashboard ampliado (evolución temporal, histogramas).
* Exportación CSV/PDF de registros.
* Autenticación con roles (Admin / Analista).
* Despliegue en Docker.

---

### 👨‍💻 **Autor**

Ricardo Rivero Martín
Ingeniero Informático
Proyecto desarrollado con enfoque analítico y arquitectura modular.
📧 *Contacto profesional disponible bajo solicitud.*

---


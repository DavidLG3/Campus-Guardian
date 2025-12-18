<template>
  <div class="not-found">
    <h1>404</h1>
    <h2>Página no encontrada</h2>
    <p>La página que buscas no existe.</p>
    <router-link to="/dashboard" class="btn-home">Volver al Dashboard</router-link>
  </div>
</template>

<style scoped>
.not-found {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
}

h1 {
  font-size: 6rem;
  margin: 0;
}

h2 {
  font-size: 2rem;
  margin: 1rem 0;
}

p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.btn-home {
  padding: 1rem 2rem;
  background: white;
  color: #667eea;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 600;
  transition: opacity 0.3s;
}

.btn-home:hover {
  opacity: 0.9;
}
</style>

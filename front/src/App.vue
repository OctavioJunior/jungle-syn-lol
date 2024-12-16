<template>
  <div id="app">
    <h1>Buscador de Campeões com Sinergia - League of Legends</h1>
    <input
      v-model="championName"
      type="text"
      placeholder="Digite o nome do campeão"
    />
    <button @click="fetchChampionData">Buscar Sinergia</button>
    
    <div v-if="loading" class="loading">Carregando...</div>
    <div v-if="error" class="error">{{ error }}</div>
    
    <div v-if="championData">
      <h2>Informações do Campeão</h2>
      <p><strong>Nome:</strong> {{ championData.name }}</p>
      <p><strong>Taxa de Vitória:</strong> {{ championData.winRate }}%</p>
      <h3>Sinergia com Campeões</h3>
      <ul>
        <li v-for="champion in championData.synergy" :key="champion.name">
          {{ champion.name }} - Taxa de Vitória: {{ champion.winRate }}%
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      championName: "",
      championData: null,
      loading: false,
      error: null,
    };
  },
  methods: {
    async fetchChampionData() {
      if (this.championName.trim() === "") {
        this.championData = null;
        return;
      }
      this.loading = true;
      this.error = null;

      try {
        const response = await fetch("http://localhost:8000/synergy", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            champion_name: this.championName.trim(),
          }),
        });

        const data = await response.json();

        if (response.ok) {
          this.championData = {
            name: data.name,
            winRate: data.winRate,
            synergy: data.synergy,
          };
        } else {
          this.error = data.message || "Erro ao buscar os dados";
          this.championData = null;
        }
      } catch (err) {
        this.error = "Erro de rede, tente novamente mais tarde.";
        this.championData = null;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}

input {
  padding: 10px;
  margin: 20px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

.loading {
  color: green;
}

.error {
  color: red;
}

ul {
  list-style-type: none;
  padding: 0;
}
</style>

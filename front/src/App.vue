<template>
  <div id="app">
    <!-- Título principal -->
    <header class="header">
      <h1>Buscador de Campeões - League of Legends</h1>
      <p>Encontre as melhores sinergias e taxas de vitória</p>
    </header>

    <!-- Input e botão -->
    <div class="search-container">
      <input
        v-model="championName"
        type="text"
        placeholder="Digite o nome do campeão"
        class="search-input"
      />
      <button @click="fetchChampionData" class="search-button">Buscar</button>
    </div>

    <!-- Mensagens de carregamento ou erro -->
    <div v-if="loading" class="loading">Carregando...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Exibição de dados -->
    <div v-if="championData" class="result-container">
      <h2 class="result-title">Sinergia de Campeões</h2>
      <ul class="synergy-list">
        <li
          v-for="champion in championData"
          :key="champion.name"
          class="synergy-item"
        >
          <div class="champion-info">
            <span class="champion-name">{{ champion.name }}</span>
            <span class="champion-winrate">
              Taxa de Vitória: <strong>{{ champion.winRate }}%</strong>
            </span>
          </div>
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
					this.championData = Object.keys(data.synergies).map((key) => ({
						name: key,
						winRate: parseFloat(data.synergies[key]),
					}));
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
/* Estilo global */
body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f4f7fb;
  color: #333;
}

/* Cabeçalho */
.header {
  background-color: #3b4a6b;
  color: #fff;
  padding: 20px 0;
  text-align: center;
}

.header h1 {
  margin: 0;
  font-size: 2.5rem;
}

.header p {
  margin-top: 5px;
  font-size: 1rem;
}

/* Área de busca */
.search-container {
  text-align: center;
  margin: 20px 0;
}

.search-input {
  padding: 10px;
  font-size: 16px;
  width: 250px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
}

.search-button {
  margin-left: 10px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #3b4a6b;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #2e3a56;
}

/* Mensagens */
.loading {
  text-align: center;
  font-size: 18px;
  color: #2e3a56;
}

.error {
  text-align: center;
  font-size: 18px;
  color: #d9534f;
}

/* Resultados */
.result-container {
  background-color: #fff;
  margin: 0 auto;
  max-width: 600px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.result-title {
  text-align: center;
  color: #3b4a6b;
  margin-bottom: 15px;
}

.synergy-list {
  list-style: none;
  padding: 0;
}

.synergy-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.synergy-item:last-child {
  border-bottom: none;
}

.champion-info {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.champion-name {
  font-weight: bold;
  color: #3b4a6b;
}

.champion-winrate {
  color: #5a6275;
}
</style>

<template>
  <div id="app">
    <header class="header">
      <h1>Buscador de Campeões - League of Legends</h1>
      <p>Encontre as melhores sinergias e taxas de vitória</p>
    </header>

    <div class="search-container">
      <ChampionDropdown 
        :championName="championName"
        @champion-selected="updateSelectedChampion"
      />
      <button @click="fetchChampionData" class="search-button">Buscar</button>
    </div>

    <LoadingError 
      :loading="loading" 
      :error="error" 
    />

    <ChampionSynergyList :championData="championData" />
  </div>
</template>

<script>
import ChampionDropdown from '@/components/ChampionDropdown.vue';
import ChampionSynergyList from '@/components/ChampionSynergyList.vue';
import LoadingError from '@/components/LoadingError.vue';
import { championService } from '@/services/championService';

export default {
  name: 'App',
  components: {
    ChampionDropdown,
    ChampionSynergyList,
    LoadingError
  },
  data() {
    return {
      championName: '',
      championData: null,
      loading: false,
      error: null
    };
  },
  methods: {
    updateSelectedChampion(champion) {
      this.championName = champion;
    },
    async fetchChampionData() {
      if (this.championName.trim() === '') {
        this.championData = null;
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        this.championData = await championService.fetchChampionSynergy(this.championName);
      } catch (err) {
        this.error = err.message;
        this.championData = null;
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style src="./styles/global.css"></style>
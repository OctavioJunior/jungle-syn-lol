<template>
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
</template>

<script>
export default {
  name: 'ChampionSynergyList',
  props: {
    championData: {
      type: Array,
      default: null
    }
  }
};
</script>
<template>
  <div class="dropdown-container">
    <input
      v-model="localSearchQuery"
      type="text"
      placeholder="Selecione um campeão"
      class="search-input"
      @focus="openDropdown"
      @input="filterChampions"
    />
    <div v-if="isDropdownOpen && filteredChampions.length > 0" class="dropdown-list">
      <div 
        v-for="champion in filteredChampions" 
        :key="champion"
        class="dropdown-item"
        @click="selectChampion(champion)"
      >
        {{ champion }}
      </div>
    </div>
  </div>
</template>

<script>
import { CHAMPION_LIST } from '@/utils/championList';

export default {
  name: 'ChampionDropdown',
  props: {
    championName: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      localSearchQuery: this.championName,
      isDropdownOpen: false,
      championList: CHAMPION_LIST
    };
  },
  computed: {
    filteredChampions() {
      return this.championList
        .filter(champion => 
          champion.toLowerCase().includes(this.localSearchQuery.toLowerCase())
        )
        .slice(0, 10);
    }
  },
  methods: {
    selectChampion(champion) {
      this.localSearchQuery = champion;
      this.isDropdownOpen = false;
      this.$emit('champion-selected', champion);
    },
    openDropdown() {
      this.isDropdownOpen = true;
    },
    filterChampions() {
      this.isDropdownOpen = true;
    },
    closeDropdown(event) {
      if (!this.$el.contains(event.target)) {
        this.isDropdownOpen = false;
      }
    }
  },
  mounted() {
    window.addEventListener('click', this.closeDropdown);
  },
  beforeUnmount() {
    window.removeEventListener('click', this.closeDropdown);
  }
};
</script>
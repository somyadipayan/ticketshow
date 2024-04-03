<template>
  <div class = "container mt-4">
    <div class = "title">
      <h1>Upcoming Shows</h1>
    <div>
    <label for="location-filter"><font-awesome-icon icon="filter" style="color: #2c313a;" /></label>
    <select id="location-filter" v-model="selectedLocation">
      <option value="">All</option> 
      <option v-for="location in uniqueLocations" :key="location" :value="location">{{ location }}</option>
    </select>
    </div>
    </div>
    <PublicTheatre v-for="theatre in filteredTheatres" :key="theatre.id" :theatre="theatre" />

    </div>
</template>

<script>
import PublicTheatre from './PublicTheatre.vue';
export default {
  components: { PublicTheatre },
  data() {
    return {
      theatres: [],
      selectedLocation: '',
    };
  },
  mounted() {
    this.fetchTheatres();
  },
  computed: {
    uniqueLocations() {
      return [...new Set(this.theatres.map(theatre => theatre.location))];
    },
    // Filter theatres based on selectedLocation
    filteredTheatres() {
      if (!this.selectedLocation) {
        return this.theatres;
      } else {
        return this.theatres.filter(theatre => theatre.location === this.selectedLocation);
      }
    },
  },
  methods: {
    async fetchTheatres() {
      try {
        const response = await fetch('http://localhost:5000/alltheatres');
        if (!response.ok) {
          throw new Error('Error fetching theatres');
        }
        const data = await response.json();
        this.theatres = data;
      } catch (error) {
        console.error('Error fetching theatres:', error);
      }
    },
  },
};
</script>

<style scoped>
#location-filter {
  margin-left: 10px;
}
.title {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

</style>

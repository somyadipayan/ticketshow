<template>
    <div class="card-container">
        <div v-if="user" class="welcome">
            <h1> {{ user.name }}'s Theatres</h1>
            <div>
            <button class="btn btn-danger" @click="clearCache" style="margin-right: 1em;">Clear Cache</button>
            <router-link class="add btn btn-primary" to="/addtheatre" role="button">Add Theatre</router-link>
            </div>
        </div>
        <div>
            <div class="grid" v-if="theatres.length > 0">
                <div v-for="theatre in theatres" :key="theatre.id">
                    <TheatreCard :theatre="theatre" />
                </div>
            </div>
            <div v-else>
                <p>You haven't added any theatres.</p>
            </div>
        </div>
        
    </div>
</template>
  
<script>
import userMixin from '../mixins/userMixin'
import TheatreCard from './TheatreCard.vue';
export default {
    name: "MyTheatres",
    mixins: [userMixin],
    data() {
        return {
            theatres: [],
        };
    },
    components: {
        TheatreCard,
    },
    async mounted() {
        await this.fetchTheatresData();
    },
    methods: {
        async fetchTheatresData() {
            try {
                const response = await fetch("http://localhost:5000/theatres", {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                        'Content-Type': 'application/json'
                    },
                });
                if (!response.ok) {
                    throw new Error("Error fetching theatres");
                }
                const data = await response.json();
                this.theatres = data;
                console.log("Theatres:", this.theatres);
            } catch (error) {
                console.error("Error fetching theatres:", error);
            }
        },
        async clearCache() {
            try {
                const response = await fetch("http://localhost:5000/clear_cache", {
                    method: "POST",
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                        'Content-Type': 'application/json'
                    },
                });
                if (!response.ok) {
                    throw new Error("Error clearing cache");
                }
                console.log("Cache cleared successfully");
            } catch (error) {
                console.error("Error clearing cache:", error);
            }
        },
    },
};
</script>
  
<style scoped>
.welcome {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    margin-bottom: 20px;
}

.grid {
    display: grid;
    gap: 1em;
    grid-template-columns: repeat(3, 1fr);
    grid-auto-rows: 1fr;
}

.card-container {
    padding: 2em;
    padding-left: 5em;
    padding-right: 5em;
}
</style>
  
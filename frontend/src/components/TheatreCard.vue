<template>
  <div class="card theatre-card" @mouseover="highlightCard(true)" @mouseleave="highlightCard(false)">
    <span class="delete-icon" @click="deleteTheatre"><font-awesome-icon icon="trash-can" style="color: #80a5e5;" /></span>
    <router-link class="edit-icon" :to="`/edittheatre/${theatre.id}`"><font-awesome-icon icon="pencil"
        style="color: #5e8bd9;" /></router-link>
    <h5 class="card-title">{{ theatre.name }}</h5>
    <div class="card-details">
      <p class="card-text detail-item">{{ theatre.place }}, {{ theatre.location }}</p>
    </div>
    <div class="error" v-if="shows.length != 0">
      <p>{{ shows.length }} Shows Added</p>
    </div>
    <div class="error" v-else>
      <p>No Shows Added</p>
    </div>
    <div class="card-details">
      <p class="card-text capacity">Capacity: {{ theatre.capacity }}</p>
    </div>
    <div class="actions">
      <router-link :to="`/viewshows/${theatre.id}`"
        class="btn btn-primary">
        View Shows
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    theatre: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isHighlighted: false,
      shows: [],
    };
  },
  async mounted() {
    await this.fetchShowsData();
  },
  methods: {
    highlightCard(status) {
      this.isHighlighted = status;
    },
    deleteTheatre() {
      
      const confirmed = window.confirm('Are you sure you want to delete this theatre?');

      if (!confirmed) {
        return;
      }

      const accessToken = localStorage.getItem('access_token');
      fetch(`http://localhost:5000/theatres/${this.theatre.id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Error deleting theatre');
          }
          this.$router.go(0)
        })
        .catch(error => {
          console.error('Delete theatre error:', error);
        });
    },
    async fetchShowsData() {
      try {
        const response = await fetch(`http://localhost:5000/theatres/${this.theatre.id}/shows`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        if (!response.ok) {
          throw new Error("Error fetching shows");
        }
        const data = await response.json();
        this.shows = data.map((show) => ({
          ...show,
          start_time: this.formatTime(show.start_time),
          end_time: this.formatTime(show.end_time),
        }));
        console.log(this.shows);
      } catch (error) {
        console.error("Error fetching shows:", error);
      }
    },
    formatTime(timeString) {
      const [hours, minutes, seconds] = timeString.split(":");
      const time = new Date();
      time.setHours(Number(hours));
      time.setMinutes(Number(minutes));
      time.setSeconds(Number(seconds));
      return time.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    },
  },
};
</script>


<style scoped>
.error {
  text-align: center;
  margin-tOP: 20px;
}

.actions {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px;
}


.card {
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 10px;
  transition: background-color 0.2s, box-shadow 0.2s;
  position: relative;
}

.card-title {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 0.1em;
}

.card-details {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.detail-item {
  font-size: 14px;
  text-align: center;
}

.capacity {
  font-size: 14px;
  text-align: center;
}

.theatre-card {
  background-color: #f0f0f0;
  overflow: hidden;
  position: relative;
}

.theatre-card:hover {
  background-color: #f5f5f5;
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
}

.delete-icon {
  position: absolute;
  top: 10px;
  right: 15px;
  font-size: 16px;
  cursor: pointer;
}

.edit-icon {
  position: absolute;
  top: 10px;
  right: 40px;
  font-size: 16px;
  cursor: pointer;
}
</style>

<template>
  <div class="container mt-5">
    <div>
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2 class="m-0">Shows at {{ this.theatre.name }}</h2>
        <router-link :to="`/addshow/${this.theatre.id}`" class="btn btn-primary">Add Show</router-link>
      </div>

      <div v-if="shows.length != 0">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Show Name</th>
              <th>Date</th>
              <th>Timing</th>
              <th>Sold Tickets</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="show in shows" :key="show.id">
              <td>{{ show.name }}</td>
              <td>{{ show.date }}</td>
              <td>{{ show.start_time }} to {{ show.end_time }}</td>
              <td>{{ show.sold_ticket_count }}</td>
              <td>
                <div class="dropdown">
                  <a class="dropbtn"><font-awesome-icon icon="caret-down" style="color: #5d92ee;" /></a>
                  <div class="dropdown-content">
                    <router-link :to="`/theatres/${this.theatre.id}/shows/${show.id}`"> Edit </router-link>
                    <a @click="deleteShow(show.id)"> Delete </a>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="error" v-else>
        <p>No Shows Added</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      theatre: {},
      shows: [],
    };
  },
  async mounted() {
    const theatreId = this.$route.params.theatreId;
    await this.fetchTheatreData(theatreId);
    await this.fetchShowsData(theatreId);
  },
  methods: {
    async fetchTheatreData(theatreId) {
      try {
        const response = await fetch(`http://localhost:5000/theatres/${theatreId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        if (!response.ok) {
          throw new Error("Error fetching theatre");
        }
        const data = await response.json();
        this.theatre = data;
        console.log(this.theatre);
      } catch (error) {
        console.error("Error fetching theatre:", error);
      }
    },
    async fetchShowsData(theatreId) {
      try {
        const response = await fetch(`http://localhost:5000/theatres/${theatreId}/shows`, {
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
    deleteShow(showId) {
      const confirmed = window.confirm('Are you sure you want to delete this show?');

      if (!confirmed) {
        return;
      }

      const accessToken = localStorage.getItem('access_token');
      fetch(`http://localhost:5000/theatres/${this.theatre.id}/shows/${showId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Error deleting show');
          }
          this.$router.go(0)
        })
        .catch(error => {
          console.error('Delete show error:', error);
        });
    },
  },
};
</script>

<style scoped>

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {
  background-color: #ddd;
}

.dropdown:hover .dropdown-content {
  display: block;
}

</style>

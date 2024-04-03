<template>
  <div class="container mt-4">
    <h3 class="mb-3">Edit Show</h3>
    <div class="card">
      <div class="card-body">
        <form @submit.prevent="submitForm">
          <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input v-model="show.name" type="text" class="form-control" id="name" required>
          </div>
          <div class="mb-3">
            <label for="tags" class="form-label">Tags</label>
            <input v-model="show.tags" type="text" class="form-control" id="tags">
          </div>
          <div class="mb-3">
            <label for="date" class="form-label">Date</label>
            <input v-model="show.date" type="date" class="form-control" id="date" required>
          </div>
          <div class="mb-3">
            <label for="start_time" class="form-label">Start Time</label>
            <input v-model="show.start_time" type="time" class="form-control" id="start_time" required>
          </div>
          <div class="mb-3">
            <label for="end_time" class="form-label">End Time</label>
            <input v-model="show.end_time" type="time" class="form-control" id="end_time" required>
          </div>
          <div class="mb-3">
            <label for="price" class="form-label">Price</label>
            <input v-model="show.price" type="number" class="form-control" id="price" required>
          </div>
          <button type="submit" class="btn btn-primary">Update Show</button>
        </form>
      </div>
    </div>
  </div>
</template>
  
<script>
export default {
  data() {
    return {
      theatreId: null,
      show: {
        name: '',
        tags: '',
        date: '',
        start_time: '',
        end_time: '',
        price: '',
        sold_ticket_count: '',
      },
    };
  },
  mounted() {
    this.theatreId = this.$route.params.theatreId;
    const showId = this.$route.params.showId;
    this.getShowData(showId);
  },
  methods: {
    async getShowData(showId) {
      try {
        const response = await fetch(
          `http://localhost:5000/shows/${showId}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );

        if (response.ok) {
          const showData = await response.json();
          showData.show.start_time = showData.show.start_time.slice(0, 5);
          showData.show.end_time = showData.show.end_time.slice(0, 5);
          this.show = showData.show;
        } else {
          const errorData = await response.json();
          const errorMessage = errorData.message || 'An error occurred.';
          window.alert(errorMessage);
        }
      } catch (error) {
        console.error('Get show data error:', error);
      }
    },
    async submitForm() {
      try {
        const response = await fetch(
          `http://localhost:5000/theatres/${this.theatreId}/shows/${this.show.id}`,
          {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
            body: JSON.stringify(this.show),
          }
        );

        if (response.ok) {
          window.alert('The show has been successfully updated.');
          this.$router.push(`/viewshows/${this.theatreId}`);
        } else {
          const errorData = await response.json();
          const errorMessage = errorData.message || 'An error occurred.';
          window.alert(errorMessage);
        }
      } catch (error) {
        console.error('Edit show error:', error);
        window.alert('An error occurred. Please try again later.');
      }
    }
  }
};
</script>
  
<style scoped>

</style>
  
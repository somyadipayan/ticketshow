<template>
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h2 class="card-title text-center">Add Theatre</h2>
              <form @submit.prevent="addTheatre">
                <div class="mb-3">
                  <label for="name" class="form-label">Name</label>
                  <input type="text" id="name" class="form-control" v-model="name" required>
                </div>
                <div class="mb-3">
                  <label for="place" class="form-label">Place</label>
                  <input type="text" id="place" class="form-control" v-model="place" required>
                </div>
                <div class="mb-3">
                  <label for="location" class="form-label">Location</label>
                  <input type="text" id="location" class="form-control" v-model="location" required>
                </div>
                <div class="mb-3">
                  <label for="capacity" class="form-label">Capacity</label>
                  <input type="number" id="capacity" class="form-control" v-model="capacity" required>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Add Theatre</button>
              </form>
              <div v-if="errorMessage" class="alert alert-danger mt-3">
                {{ errorMessage }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        name: "",
        place: "",
        location: "",
        capacity: "",
        errorMessage: "",
      };
    },

    methods: {
      addTheatre() {
        fetch('http://localhost:5000/theatres', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
          body: JSON.stringify({
            name: this.name,
            place: this.place,
            location: this.location,
            capacity: this.capacity,
          }),
        })
          .then(response => {
            if (!response.ok) {
              throw new Error('Error adding theatre');
            }
            return response.json();
          })
          .then(data => {
            console.log(data);
            window.alert("New Thetre Added!");
            this.$router.push('/mytheatres');
          })
          .catch(error => {
            console.error('Add theatre error:', error);
            this.errorMessage = 'Error adding theatre. Please try again later.';
          });
      },
    },
  };
  </script>
  
  <style>
  </style>
  
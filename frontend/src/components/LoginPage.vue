<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title text-center">Login</h2>
            <form @submit.prevent="login">
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" id="email" class="form-control" v-model="email" required>
              </div>
              <div class="mb-3">  
                <label for="password" class="form-label">Password</label>
                <input type="password" id="password" class="form-control" v-model="password" required>
              </div>
              <button type="submit" class="btn btn-primary btn-block">Login</button>
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
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    login() {
      // Fetch user login data from Flask API
      fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: this.email,
          password: this.password,
        }),
      })
        .then(response => response.json())
        .then(data => {
          if (data && data.access_token) {
            // Store the access token in the browser's local storage
            localStorage.setItem('access_token', data.access_token);
            this.$router.push('/');
          } else {
            // Show login error message (you can customize the error handling based on the Flask API response)
            this.errorMessage = 'Invalid credentials. Please try again.';
          }
        })
        .catch(error => {
          // Handle any fetch errors
          console.error('Fetch error:', error);
          this.errorMessage = 'An error occurred. Please try again later.';
        });
    },
  },
};
</script>

<style>
/* You can add custom styles here if needed */
</style>

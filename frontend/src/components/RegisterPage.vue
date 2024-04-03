<template>
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h2 class="card-title text-center">Sign Up</h2>
              <form @submit.prevent="signup">
                <div class="mb-3">
                  <label for="name" class="form-label">Full Name</label>
                  <input type="text" id="name" class="form-control" v-model="name" required>
                </div>
                <div class="mb-3">
                  <label for="email" class="form-label">Email</label>
                  <input type="email" id="email" class="form-control" v-model="email" required>
                </div>
                <div class="mb-3">
                  <label for="city" class="form-label">City</label>
                  <input type="text" id="city" class="form-control" v-model="city" required>
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" id="password" class="form-control" v-model="password" required>
                </div>
                <div class="mb-3">
                  <label for="confirmPassword" class="form-label">Confirm Password</label>
                  <input type="password" id="confirmPassword" class="form-control" v-model="confirmPassword" required>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Sign Up</button>
              </form>
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
        email: "",
        city: "",
        password: "",
        confirmPassword: "",
      };
    },
    methods: {
    signup() {
      const formData = {
        email: this.email,
        name: this.name,
        city: this.city,
        password: this.password,
      };

      fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        window.alert('Registration successful');
        this.$router.push('/login');
      })
      .catch(error => {
        console.log(formData);
        console.error(error);
        window.alert('Registration failed');
      });
      },
    },
  };
  </script>
  
  <style>
  </style>
  
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light" style="position: sticky;">
    <div class="container">
      <router-link class="navbar-brand" to="/">TicketShow</router-link>

      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav ms-auto">
          <div class="navitems" v-if="isUserLoggedIn">
            <router-link v-if="isAdmin" class="nav-item nav-link" to="/mytheatres">Admin Actions</router-link>
            <router-link v-if="isAdmin" class="nav-item nav-link" to="/reports">Reports</router-link>
            <router-link class="nav-item nav-link" to="/">Book Tickets</router-link>
            <router-link class="nav-item nav-link" to="/bookinghistory">Booking History</router-link>
            <a @click="logout"> <font-awesome-icon icon="arrow-right-from-bracket" style="color: #6d97df;" /> </a>
          </div>
          <div class="navitems" v-else>
            <router-link class="nav-item nav-link" to="/login">Login</router-link>  
            <router-link class="nav-item nav-link" to="/register">Register</router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import UserMixin from '../mixins/userMixin'; 

export default {
  mixins: [UserMixin],
  watch: {
    isLoggedIn(newStatus) {
      if (newStatus) {
        const accessToken = localStorage.getItem('access_token');
        if (accessToken) {
          this.fetchUserInfo(accessToken);
        } else {
          this.user = null;
        }
      } else {
        this.user = null;
      }
    },
  },
  computed: {
    isAdmin() {
      return this.user !== null && this.user.is_admin;
    },
    isUserLoggedIn() {
      return this.user !== null && this.isLoggedIn;
    },
  },
};
</script>


<style>

.navitems {
  display: flex;
  align-items: center;
}

.navitems a {
  margin-left: 15px;
}
</style>

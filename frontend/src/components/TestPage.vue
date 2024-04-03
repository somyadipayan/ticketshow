<template>
  <div>
    <div v-if="loading">
      <p>Loading...</p>
    </div>
    <div v-else>
      <div v-if="(user && user.isLoggedIn)">
        <p>Hi {{ user.name }}, You are logged in as {{ user.is_admin ? 'Admin' : 'User' }}</p>
        <font-awesome-icon :icon="['far', 'trash-can']" style="color: #80a5e5;" />
        <button @click="logout">Logout</button>
      </div>
      <div v-else>
        <p>Please log in to see the welcome message.</p>
      </div>
      
    </div>
  </div>
</template>

<script>
import userMixin from '../mixins/userMixin'; 

export default {
  name: 'TestPage',
  mixins: [userMixin],
};
</script>

<style>
</style>

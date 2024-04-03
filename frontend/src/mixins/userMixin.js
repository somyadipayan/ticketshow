export default {
  data() {
    return {
      user: null,
      loading: true,
      isLoggedIn: false,
    };
  },
  async created() {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      try {
        const data = await this.fetchUserInfo(accessToken);
        this.user = data;
        this.isLoggedIn = true;
      } catch (error) {
        console.error('Fetch error:', error);
        this.isLoggedIn = false;
      }
    } else {
      this.isLoggedIn = false;
      this.loading = false;
    }
  },
  methods: {
    async fetchUserInfo(token) { 
      try {
        const response = await fetch('http://localhost:5000/getuserinfo', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        if (response.status === 401) {
          this.isLoggedIn = false;
          return null; 
        } else {
          return await response.json(); 
        }
      } catch (error) {
        console.error('Fetch error:', error);
        this.isLoggedIn = false;
        throw error;
      } finally {
        this.loading = false;
      }
    },
    logout() {
      fetch('http://localhost:5000/logout', {
        method: 'POST',
        credentials: 'include', 
      })
        .then(() => {
          this.clearCache();
          localStorage.removeItem('access_token');
          this.user = null;
          this.isLoggedIn = false; 
          this.$router.push('/login');
        })
        .catch(error => {
          console.error('Logout error:', error);
        });
    },
    clearCache() {
      // Clear the cache
      fetch('http://localhost:5000/clear_cache', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      })
        .then(response => {
          if (!response.ok) {
            console.error('Clear cache error:', response.statusText);
          } else {
            console.log('Cache cleared successfully');
          }
        })
        .catch(error => {
          console.error('Clear cache error:', error);
        });
    },
  },
};

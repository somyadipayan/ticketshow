<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-12">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title text-center">Your Reports</h2>
            <br><br>
            <div class="d-flex">
              <!-- Line chart for total tickets sold per day -->
              <div class="mb-3">
                <h4 class="text-center">Total Tickets Sold per Day</h4>
                <img :src="getPlotImageUrl(lineChartUrl)" alt="Total Tickets Sold per Day" class="img-fluid">
              </div>
              <!-- Bar graph for shows and revenues -->
              <div class="mb-3">
                <h4 class="text-center">Your Shows and Revenues</h4>
                <img :src="getPlotImageUrl(barGraphUrl)" alt="Your Shows and Revenues" class="img-fluid">
              </div>
            </div>
            <div class="text-center mt-4">
              <button class="btn btn-primary" @click="downloadCSV">Download CSV</button>
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
      lineChartUrl: "", 
      barGraphUrl: "",
    };
  },

  mounted() {
    this.loadPlotUrls();
  },

  methods: {
    async loadPlotUrls() {
      try {
        const accessToken = localStorage.getItem('access_token');

        const headers = {
          'Authorization': `Bearer ${accessToken}`,
        };

        const response1 = await fetch('http://localhost:5000/admin_ticket_stats', { headers });
        const data1 = await response1.json();
        this.lineChartUrl = data1.plot_url;
        console.log(this.lineChartUrl)

        const response2 = await fetch('http://localhost:5000/admin_show_revenue_stats', { headers });
        const data2 = await response2.json();
        this.barGraphUrl = data2.plot_url;
        console.log(this.barGraphUrl)
      } catch (error) {
        console.error('Error loading plot URLs:', error);
      }
    },
    getPlotImageUrl(filename) {
      return `http://localhost:5000/plot_images/${filename}`;
    },
    downloadCSV() {
      try {
        const accessToken = localStorage.getItem('access_token');

        const headers = {
          'Authorization': `Bearer ${accessToken}`,
        };

        fetch('http://localhost:5000/generate_csv', { headers })
          .then(response => response.blob())
          .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'transactions.csv';
            document.body.appendChild(a);
            a.click();
            URL.revokeObjectURL(url);
          });
      } catch (error) {
        console.error('Error downloading CSV:', error);
        window.alert('Error downloading CSV');
      }
    },
  },
};
</script>

<style scoped>


</style>

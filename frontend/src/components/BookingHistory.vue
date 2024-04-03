<template>
  <div class="container mt-4">
    <h3 class="mb-3">Booking History</h3>
    <table class="table">
      <thead>
        <tr>
          <th>Show Name</th>
          <th>Theatre Name</th>
          <th>Date</th>
          <th>No. of Tickets</th>
          <th>Amount</th>
          <th>Ratings</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="booking in bookings" :key="booking.id">
          <td>{{ booking.show_name }}</td>
          <td>{{ booking.theatre_name }}</td>
          <td>{{ booking.date }}</td>
          <td>{{ booking.no_of_tickets }}</td>
          <td>{{ booking.amount }}</td>
          <td>
            <input type="radio" :name="'rating-' + booking.id" value="1" v-model="booking.rating" @change="updateRating(booking.id)">
            <input type="radio" :name="'rating-' + booking.id" value="2" v-model="booking.rating" @change="updateRating(booking.id)">
            <input type="radio" :name="'rating-' + booking.id" value="3" v-model="booking.rating" @change="updateRating(booking.id)">
            <input type="radio" :name="'rating-' + booking.id" value="4" v-model="booking.rating" @change="updateRating(booking.id)">
            <input type="radio" :name="'rating-' + booking.id" value="5" v-model="booking.rating" @change="updateRating(booking.id)">
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="errorMessage" class="alert alert-danger mt-3">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bookings: [],
      errorMessage: "",
    };
  },
  mounted() {
    this.fetchBookingHistory();
  },
  methods: {
    async fetchBookingHistory() {
      try {
        const response = await fetch("http://localhost:5000/my_bookings", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });

        if (response.ok) {
          const bookingData = await response.json();
          this.bookings = bookingData;
          console.log(this.bookings);
        } else {
          const errorData = await response.json();
          this.errorMessage = errorData.message;
        }
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Error occurred while fetching booking history";
      }
    },
    async updateRating(bookingId) {
      try {
        const rating = this.bookings.find((booking) => booking.id === bookingId).rating;
        const response = await fetch("http://localhost:5000/update_rating", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify({ booking_id: bookingId, rating: rating }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message);
        }
      } catch (error) {
        console.error("Rating update error:", error);
        this.errorMessage = "Error occurred while updating rating";
      }
    },

  },
};
</script>

<style>
.table td {
  vertical-align: middle;
}
</style>

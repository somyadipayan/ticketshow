<template>
    <div v-if="show" class="container mt-4">
        <h3 class="mb-3">Book Tickets of {{ this.show.name }}</h3>
        <form @submit.prevent="bookTickets">
            <div class="mb-3">
                <label for="no_of_tickets" class="form-label">Number of Tickets</label>
                <input v-model="noOfTickets" type="number" class="form-control" id="no_of_tickets" required
                    @input="updateTotalAmount">
            </div>
            <div class="mb-3">
                <label>Total Amount: </label>
                <span>{{ totalAmount }}</span>
                <br>
                <div v-if="ticketsleft >= 0">
                    <label>Remaining Tickets: </label>
                    <span>{{ ticketsleft }}</span>
                </div>
                <div v-else>
                    Not Enough Tickets are available.
                </div>
            </div>
            <button type="submit" class="btn btn-primary">Book Tickets</button>
            <div v-if="errorMessage" class="alert alert-danger mt-3">
                {{ errorMessage }}
            </div>
        </form>
    </div>
</template>
<script>
export default {
    data() {
        return {
            show: null,
            noOfTickets: 1,
            errorMessage: "",
        };
    },
    computed: {
        totalAmount() {
            if (!this.show || isNaN(this.noOfTickets) || this.noOfTickets < 1) {
                return 0;
            }
            return (this.show.price * this.noOfTickets).toFixed(2);
        },
        ticketsleft() {
            if (!this.show || isNaN(this.noOfTickets) || this.noOfTickets < 1) {
                return this.remaining_tickets;
            }
            return (this.remaining_tickets - this.noOfTickets);
        },
    },
    mounted() {
        const showId = this.$route.params.showId;
        this.getShowData(showId);
    },
    methods: {
        async getShowData(showId) {
            try {
                const response = await fetch(
                    `http://localhost:5000/shows/${showId}`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                        },
                    }
                );

                if (response.ok) {
                    const showData = await response.json();
                    this.show = showData.show;
                    this.remaining_tickets = showData.remaining_tickets;
                    console.log("Show data:", showData);
                } else {
                    const errorData = await response.json();
                    this.errorMessage = errorData.message;
                }
            } catch (error) {
                console.error("Get show data error:", error);
                window.alert(this.errorMessage);
            }
        },
        async bookTickets() {
            try {
                const response = await fetch(
                    `http://localhost:5000/book_ticket/${this.show.id}`,
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                        },
                        body: JSON.stringify({ no_of_tickets: this.noOfTickets }),
                    }
                );

                if (response.ok) {
                    window.alert("Your Tickets have been Booked!");
                    this.$router.push("/");
                } else {
                    const errorData = await response.json();
                    this.errorMessage = errorData.message;
                }
            } catch (error) {
                console.error("Book tickets error:", error);
                window.alert(this.errorMessage);
            }
        },
        updateTotalAmount() {
            this.errorMessage = "";
        },
    },
};
</script>


  
<style scoped>

</style>
  
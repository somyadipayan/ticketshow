<template>
    <div class="container my-5">
        <h3 class="mb-3">Add New Show</h3>
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
                    <button type="submit" class="btn btn-primary">Add Show</button>
                    <div v-if="errorMessage" class="alert alert-danger mt-3">
                        {{ errorMessage }}
                    </div>
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
            }
        };
    },
    mounted() {
        this.theatreId = this.$route.params.theatreId;
    },
    methods: {
        async submitForm() {
            try {
                console.log(JSON.stringify(this.show));
                const response = await fetch(`http://localhost:5000/theatres/${this.theatreId}/shows`, {
                    method: 'POST',
                    headers: {
                        "Content-Type": 'application/json',
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                    },
                    body: JSON.stringify(this.show)

                });

                if (response.ok) {
                    window.alert("New Show Added!");
                    this.$router.push('/mytheatres');
                } else {
                    console.log(JSON.stringify(this.show));
                    const errorData = await response.json();
                    const errorMessage = errorData.message || 'An error occurred.';
                    window.alert(errorMessage);
                }
            } catch (error) {
                console.error('Add show error:', error);
                window.alert('An error occurred. Please try again later.');
            }
        }
    }
};
</script>

<style scoped></style>
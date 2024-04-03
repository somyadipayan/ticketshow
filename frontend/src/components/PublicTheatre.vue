<template>
    <div class="container mt-4">
        <div class="d-flex flex-row justify-content-center align-items-center">
            <div class="theatre__card">
                <h1>{{ theatre.name }}</h1>
                <p style = "color: #4b4b4d;">{{ theatre.place }},{{ theatre.location }}</p>
                <div  class="shows">
                <PublicShow v-for="show in theatre.shows" :key="show.id" :show="show"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import PublicShow from './PublicShow.vue';
export default {
    props: {
        theatre: {
            type: Object,
            required: true,
        },
    },
    components: { PublicShow }
}
</script>

<style>
.theatre__card {
    width: 100%;
    padding: 15px 25px;
    background-color: #EEEEEE;
    border-radius: 20px;
    color: #051129;
    background: #f1f1f1;

    
}

.theatre__card h1 {
    font-size: 2em;
    margin-bottom: 0.01em;
}

.theatre__card .shows{
    display: flex;
    margin-right: 1em!important;
}
</style>

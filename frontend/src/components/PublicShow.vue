<template>
    <div class="parent">
  <div class="card">
      <div class="content-box">
          <span class="card-title">{{show.name}}</span>
          
          <p class="timing">
              {{ formatTime(show.start_time) }} to {{ formatTime(show.end_time) }}
          </p>
          <p class="price">
            <font-awesome-icon icon="indian-rupee-sign" style="color: #f2f2f2;" /> {{ show.price }}
          </p>

          <p class="timing">{{ show.tags }} <br> Rating: {{ show.rating === 0 ? '-' : show.rating.toFixed(1) }}/5</p>
          <router-link class="see-more" :to="`/book_tickets/${show.id}`">Book Tickets</router-link>
      </div>
      <div class="date-box">
          <span class="month">{{ formatMonth(show.date) }}</span>
          <span class="date">{{ getDay(show.date) }}</span>
      </div>
  </div>
</div>
</template>

<script>
export default {
    props: {
        show: {
            type: Object,
            required: true,
        },
    },

    methods: {
    formatMonth(dateString) {
      const date = new Date(dateString);
      const monthAbbreviation = date.toLocaleString('default', { month: 'short' });
      return monthAbbreviation;
    },
    getDay(dateString) {
      const date = new Date(dateString);
      return date.getDate();
    },
    formatTime(timeString) {
      const [hours, minutes, seconds] = timeString.split(":");
      const time = new Date();
      time.setHours(Number(hours));
      time.setMinutes(Number(minutes));
      time.setSeconds(Number(seconds));
      return time.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    }
  },

}
</script>

<style scoped>

.parent {
  width: 300px;
  padding: 20px;
  perspective: 1000px;
}

.card {
  padding-top: 50px;
  border-radius: 10px;
  transform-style: preserve-3d;
  background-image: radial-gradient(#052e44 2px, transparent 2px), radial-gradient(#0c567e 2px, transparent 2px);
  background-size: 23px 23px;
  background-position: 0 0, 11px 11px;
  background-color: #f0f0f0;
  width: 100%;
  transition: all 0.5s ease-in-out;
}

.card:hover {
  background-position: -110.5px 110.5px, -99px 99px;
  transform: rotate3d(0.5, 1, 0, 30deg);
}

.content-box {
  background: linear-gradient(135deg, rgba(0, 187, 255, 0.81) 0%, rgb(1, 82, 122) 100%);
  border-radius: 0px 100px 10px 10px;
   /* border-right: 2px solid white; */
  width: 90%;
  box-shadow: rgba(142, 142, 142, 0.686) 0px 20px 50px -10px;
  transition: all 0.5s ease-in-out;
  padding: 60px 25px 25px 25px;
  transform-style: preserve-3d;
}

.content-box .card-title {
  display: inline-block;
  color: white;
  font-size: 25px;
  font-weight: 900;
  margin-bottom: 0.1em;
  transition: all 0.5s ease-in-out;
  transform: translate3d(0px, 0px, 60px);
}

.content-box .card-title:hover {
  transform: translate3d(0px, 0px, 50px);
}

.content-box .timing {  
  font-size: 12px;
  font-weight: 700;
  color: #f2f2f2;
  transition: all 0.5s ease-in-out;
  transform: translate3d(0px, 0px, 30px);
}

.content-box .price {
  margin-top: 10px;
  font-size: 20px;
  font-weight: 900;
  color: #f2f2f2;
  transition: all 0.5s ease-in-out;
  transform: translate3d(0px, 0px, 30px);
}

.content-box .timing:hover {
  transform: translate3d(0px, 0px, 50px);
}


.content-box .price:hover {
  transform: translate3d(0px, 0px, 50px);
}


.content-box .see-more {
  cursor: pointer;
  margin-top: 0.01em;
  display: inline-block;
  font-weight: 900;
  font-size: 11px;
  text-transform: uppercase;
  color: #ededed;
  border-left: 2px solid #ededed;
  border-radius: 0 0 0 1rem;
  background: linear-gradient(245deg, rgba(0, 251, 255, 0) 0%, rgba(0,168,255,1) 100%);
  padding: 0.7rem;
  transition: all 0.5s ease-in-out;
  transform: translate3d(0px, 0px, 20px);
}

.content-box .see-more:hover {
  transform: translate3d(0px, 0px, 50px);
}

.date-box {
  position: absolute;
  top: 30px;
  left: 25px;
  height: 60px;
  width: 60px;
  background: linear-gradient(45deg, rgb(255, 255, 255) 0%, #d8d8d8 100%);
  border-left: 2px solid rgb(7, 185, 255);
  border-radius: 10px;
  padding: 10px;
  transform: translate3d(0px, 0px, 80px);
}

.date-box span {
  display: block;
  text-align: center;
}

.date-box .month {
  color: #052e44;
  font-size: 11px;
  font-weight: 700;
}

.date-box .date {
  font-size: 20px;
  font-weight: 900;
  color: rgb(4, 193, 250);
}
 

</style>

import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import LoginPage from './components/LoginPage.vue';
import RegisterPage from './components/RegisterPage.vue';
import TestPage from './components/TestPage.vue';
import MyTheatres from './components/MyTheatres.vue';
import AddTheatre from './components/AddTheatre.vue';
import EditTheatre from './components/EditTheatre.vue';
import AddShow from './components/AddShow.vue';
import EditShow from './components/EditShow.vue';
import BookTickets from './components/BookTickets.vue';
import BookingHistory from './components/BookingHistory.vue';
import TicketComp from './components/TicketComp.vue';
import AdminReport from './components/AdminReport.vue';
import ViewShows from './components/ViewShows.vue';

function checkAuth(to, from, next) {
  const accessToken = localStorage.getItem('access_token');
  if (!accessToken) {
    next('/login');
  } else {
    fetch('http://localhost:5000/getuserinfo', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    })
    .then(response => response.json())
    .then(data => {
      const isAdmin = data.is_admin;
      if (!isAdmin) {
        next('/');
      } else {
        next();
      }
    })
    .catch(error => {
      console.error('Fetch error:', error);
      next('/');
    });
  }
}

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage,
  },
  {
    path: '/test',
    name: 'TestPage',
    component: TestPage,
  },
  {
    path: '/mytheatres',
    name: 'MyTheatres',
    component: MyTheatres,
    meta: { requiresAuth: true },
    beforeEnter: checkAuth,
  },
  {
    path: '/addtheatre',
    name: 'AddTheatre',
    component: AddTheatre,
    meta: { requiresAuth: true },
    beforeEnter: checkAuth,
  },
  {
    path: '/edittheatre/:theatreId',
    name: 'EditTheatre',
    component: EditTheatre,
    meta: { requiresAuth: true },
    beforeEnter: checkAuth,
  },
  {
    path: '/addshow/:theatreId',
    name: 'AddShow',
    component: AddShow,
    meta: { requiresAuth: true },
    beforeEnter: checkAuth,
  },
  {
    path: '/theatres/:theatreId/shows/:showId',
    component: EditShow,
    name: 'EditShow',
    meta: { requiresAuth: true },
    beforeEnter: checkAuth,
  },
  {
    path: "/book_tickets/:showId",
    name: "BookTickets",
    component: BookTickets,
  },
  {
    path: "/bookinghistory",
    name: "BookingHistory",
    component: BookingHistory,
  },
  {
    path: '/ticket',
    name: 'TicketComp',
    component: TicketComp,
  },
  {
    path: '/reports',
    name: 'AdminReport',
    component: AdminReport,
  },
  {
    path: '/viewshows/:theatreId',
    name: 'ViewShows',
    component: ViewShows,
  },

];


const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import router from './routers';
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import './styles/global.css';

library.add(fas)

const app = createApp(App)

app.use(router)
app.mount('#app')
app.component('font-awesome-icon', FontAwesomeIcon)
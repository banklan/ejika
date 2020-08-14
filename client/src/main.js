import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueRouter from 'vue-router'
import axios from 'axios'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@mdi/font/css/materialdesignicons.css'
import VeeValidate from 'vee-validate'
import Routes from './routes';
import {
  store
} from './store';
import './styles/style.css'
import './filters'

Vue.use(VueRouter);
Vue.use(VeeValidate);
Vue.prototype.$axios = axios;

const router = new VueRouter({
  routes: Routes,
  mode: 'history'
})

Vue.config.productionTip = false
Vue.component('my-portfolio', require('./components/child/MyPortFolio.vue').default);
Vue.component('featured', require('./components/child/Featured.vue').default);
Vue.component('popular', require('./components/child/Popular.vue').default);
Vue.component('locations', require('./components/child/Locations.vue').default);
Vue.component('home-how-to', require('./components/child/HomeHowTo.vue').default);
Vue.component('testimonials', require('./components/child/Testimonials.vue').default);
Vue.component('new-services', require('./components/child/NewServices.vue').default);
Vue.component('map-location', require('./components/child/MapLocation.vue').default);

new Vue({
  vuetify,
  router,
  store,
  render: h => h(App),
}).$mount('#app')
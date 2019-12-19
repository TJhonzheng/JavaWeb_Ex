// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Router from 'vue-router'
import axios from 'axios'
import api from './api'
import store from './store/index'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

axios.defaults.baseURL = 'http://127.0.0.1:8060/api'
Vue.prototype.$axios = axios
Vue.prototype.$api = api
Vue.config.productionTip = false
const routerPush = Router.prototype.push
Vue.use(ElementUI)
Router.prototype.push = function push(location){
  return routerPush.call(this, location).catch(error=> error)
}

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})

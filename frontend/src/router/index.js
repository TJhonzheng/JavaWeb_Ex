import Vue from 'vue'
import Router from 'vue-router'
import index from '@/components/index'
import login from '@/components/login'
import register from '@/components/register'
import userInfo from '@/components/userInfo'
import classInfo from '@/components/classInfo'

Vue.use(Router)

export default new Router({
  mode:"hash",
  routes: [
    {
      path: '/',
      name: 'index',
      component: index
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/register',
      name: 'register',
      component: register
    },
    {
      path: '/user',
      name: 'userInfo',
      component: userInfo
    },
    {
      path: '/classInfo/:classNum',
      name: 'classInfo',
      component: classInfo
    },
  ]
})

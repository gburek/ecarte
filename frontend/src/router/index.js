import Vue from 'vue'
import Router from 'vue-router'
import SalesHome from '@/components/SalesHome'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'SalesHome',
      component: SalesHome
    }
  ]
})

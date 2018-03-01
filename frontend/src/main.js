// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'

Vue.config.productionTip = false

/* eslint-disable no-new */
window.App = new Vue({
	el: '#app',
	router,
	components: { App },
	template: '<App/>',

	created() {
		Vue.$http = axios.create({
			baseURL: `http://localhost:8000`,
		})
  	}
})

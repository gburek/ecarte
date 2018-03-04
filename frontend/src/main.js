// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import AJAX_END from './App.vue'
//import { default } from './App.vue'
import * as Ecarte from './App.vue'

Vue.config.productionTip = false

/* eslint-disable no-new */
window.App = new Vue({
	el: '#app',
	router,
	components: { App },
	template: '<App/>',

	created() {
		Vue.$eventBus = new Vue({})
		Vue.$http = axios.create({
			// That should be coming from a config
			baseURL: `http://localhost:8000`,
		})
		// Let everyone know that an ajax call has ended
		// so they can for instance hide throbbers
		Vue.$http.interceptors.response.use(
			function(response) {
				Vue.$eventBus.$emit(Ecarte.AJAX_END)
				return response
			},
			function(error) {
				Vue.$eventBus.$emit(Ecarte.AJAX_END)
				return Promise.reject(error)
			})
  	}
})

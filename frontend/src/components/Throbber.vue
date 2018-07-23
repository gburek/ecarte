<template>
	<span class="ajax-pending" v-show="ajaxPending"><slot>Working...</slot></span>
</template>

<script>
	import Vue from 'vue'
	import * as Ecarte from '../App.vue'

	export default {
		name: 'throbber',

		data() {
			return {
				ajaxPending: false,
			}
		},

		mounted() {
			Vue.$eventBus.$on(Ecarte.AJAX_START, () => {
				this.ajaxPending = true
			})
			Vue.$eventBus.$on(Ecarte.AJAX_END, () => {
				this.ajaxPending = false
			})
		},
	}
</script>

<style lang="scss" scoped>
	.ajax-pending {
		color: yellow;
		padding-left: 33px;
		background-image: url('/static/img/gear.svg');
		background-position: 10px 0;
		background-size: contain;
		background-repeat: no-repeat;
	}
</style>
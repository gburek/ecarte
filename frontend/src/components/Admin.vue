<template>
  <div id="admin-home" v-if="visible">
    <h1>Restaurant and Menu Administration</h1>

    <div>
	    <ul class="main-menu">
	    	<li v-for="panel of panels" :key="panel.id" :class="{active: selectedPanel.id == panel.id}"
	    	    @click="selectedPanel = panel">{{ panel.title }}</li>
	    </ul>

	    <div class="panels">
	    	<div v-for="panel of panels" v-show="panel.id == selectedPanel.id" :is="panel.component"></div>
	    	<br>
	    </div>
	    <br>
	</div>
  </div>
</template>

<script>
	import Vue from 'vue'
	import AccountAdmin from './AccountAdmin.vue'
	import BusinessAdmin from './BusinessAdmin.vue'
	import MenuAdmin from './MenuAdmin.vue'

	export default {
		name: 'Admin',

		components: {
			AccountAdmin, BusinessAdmin, MenuAdmin
		},

		props: {
			visible: {
				type: Boolean,
				default: false,
			},

		},

		data() {
			let _panels = [
					{ id: 'account', title: 'Account', component: 'AccountAdmin' },
					{ id: 'business', title: 'Business Info', component: 'BusinessAdmin' },
					{ id: 'menu', title: 'Menu', component: 'MenuAdmin' },
				]
			return {
				panels: _panels,
				selectedPanel: _panels[0],
			}
		},
	}
</script>

<style lang="scss">
	/* TODO: import sass mixins from materialize to use a grid */
	$dark-yellow: #CCCC00;

	#admin-home {
		margin: 15px 20px 15px 15px;
		background-color: black;
		color: $dark-yellow;
		opacity: 0.9;
		padding: 15px 20px;
		border-radius: 10px;

		h1 {
			font-size: 20px;
			margin: 0;
			margin-bottom: 25px;
			color: $menu-color;
		}
	}

	.main-menu {
		display: inline-block;
		width: 18%;
		height: 95%;
		li {
			color: $menu-color;
			cursor: pointer;
			padding: 3px 0 3px 8px;
			margin-bottom: 5px;
			border-radius: 5px;

			&.active {
				border-bottom: solid $menu-color 1px;
			}
		}
	}

	.panels {
		display: inline-block;
		width: 80%;
		position: relative;
		float: right;
		padding-bottom: 10px;
		clear: both;

		h2 {
			font-size: 16px;
			color: $boo;
		}

		& > div {
			float:left;
		}
	}

	br {
		clear: both;
	}
</style>
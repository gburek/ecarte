<template>
	<div @keydown.enter="update">
		<fieldset>
			<legend>User Information</legend>
			<div class="top-message" :class="{error: haveErrors}" v-html="topMessage"></div>
			<label :class="{error: response.errors.email}">Email
				<i class="material-icons">mail outline</i>
				<input class="error" type="text" placeholder="Email" name="email" autocomplete="off" v-model="userObj.email">
				<span class="error-msg" v-if="response.errors.email">{{ response.errors.email }}</span>
			</label>
			<input style="display:none;">
			<label :class="{error: response.errors.password1}">Password
				<i class="material-icons">lock outline</i>
				<input type="password" placeholder="Password" name="password" autocomplete="off" v-model="password1">
				<span class="error-msg" v-if="response.errors.password1">{{ response.errors.password1 }}</span>
			</label>
			<label :class="{error: response.errors.password2}">Repeat Password
				<i class="material-icons">lock outline</i>
				<input type="password" placeholder="Password - again" name="password1" autocomplete="off" v-model="password2">
				<span class="error-msg" v-if="response.errors.password2">{{ response.errors.password2 }}</span>
			</label>
			<div>
				<!-- TODO: create a button with throbber component -->
				<button class="waves-effect waves-light btn" @click="update">Update</button>
			</div>
		</fieldset>
	</div>
</template>

<script>
	import Vue from 'vue'
	import * as Ecarte from '../App.vue'

	export default {
		name: 'AccountAdmin',

		mounted() {
			this.userObj = App.userObj || {}
		},

		data() {
			return {
				userObj : {},
				password1: '',
				password2: '',
				response: { errors: {} },
				topMessage: '',
			}
		},

		methods: {
			update() {
				//console.log(`PATCH /api/account/${this.userObj.id}`)
				this.topMessage = ''
				Vue.$http.patch(
					`/api/account/${this.userObj.id}`,
					{ 
						email: this.userObj.email,
					  	password1: this.password1,
					  	password2: this.password2 
					}
				).then( (response) => {
					if (response.data.errors) {
						this.response.errors = response.data.errors
						this.topMessage = Ecarte.MSG_VALIDATION_ERROR
					}
					else {
						this.response.errors = {}
						this.password1 = this.password2 = ''
						this.topMessage = Ecarte.MSG_UPDATE_SUCCESS
					}
				});
			}
		},

		computed: {
			haveErrors() {
				return this.response.errors && Object.keys(this.response.errors).length>0
			}
		}
	}
</script>

<style lang="scss" scoped>
	/* This all must go to the unscoped, global style */

	.top-message {
		margin-bottom: 10px;
		color: #cefdce;

		&.error {
			color: $error-color;
		}
	}

	fieldset {
		border-radius: 8px;
		padding: 15px;
		color: #aaa;
	}

	legend {
		padding: 0 10px;
		color: #aaa;
	}

	label {
		display: block;
		position: relative;
		width: 95%;
		margin-bottom: 15px;

		i.material-icons {
			position: absolute;
			left: 10px;
			top: 28px;
			z-index: 2;
		}

		input[type=text], input[type=password] {
			position: relative;
			left: 0;
			top: 0px;
			padding-left: 45px;
			background-color: #111;
			width: 90%;
			min-width: 15em;
			margin-bottom: 0;

			&::placeholder {
				color: #888;
			}
		}

		span.error-msg {
			display: inline-block;
			margin-top: 8px;
			font-size: 125%;
		}
	}

	label.error {
		color: $error-color;

		input {
			border-bottom: 1px solid $error-color;
			color: $error-color;
		}
	}

	button.btn {
		letter-spacing: 2px;
	}
</style>
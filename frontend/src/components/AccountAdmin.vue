<template>
	<div>
		<fieldset>
			<legend>User Information</legend>
			<label >Email
				<i class="material-icons">mail outline</i><input class="error" type="text" placeholder="Email" name="email" autocomplete="off">
				<span class="error-msg">This e-mail is in use!</span>
			</label>
			<input style="display:none;">
			<label>Password
				<i class="material-icons">lock outline</i><input type="password" placeholder="Password" name="password" autocomplete="off">
			</label>
			<label>Repeat Password
				<i class="material-icons">lock outline</i><input type="password" placeholder="Password - again" name="password1" autocomplete="off">
			</label>
			<div>
				<button class="waves-effect waves-light btn">Update</button>
			</div>
		</fieldset>
	</div>
</template>

<script>
	export default {
		name: 'AccountAdmin',

		mounted() {
			this.userObj = App.userObj
		},

		data() {
			return {
				userObj : {},
			}
		}
	}
</script>

<style lang="scss" scoped>
	/* This all must go to the unscoped, global style */

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
		color: #c00;

		input {
			border-bottom: 1px solid #c00;
			color: #c00;
		}
	}

	button.btn {
		letter-spacing: 2px;
	}
</style>
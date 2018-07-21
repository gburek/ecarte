<template>
    <div id="main">
        <transition name="authbox-fade">
            <div id="auth-box" v-show="show_auth_box">
                <h2>Please log in</h2>
                <form autofill="no" @keydown.enter="login" @keydown.esc="hideLoginBox">
                    <div class="error-msg" v-if="loginErrorMsg">{{ loginErrorMsg }}</div>
                    <div><input type="text" ref="username" placeholder="Username or email" v-model="usernm"
                                ></div>
                    <div><input type="password" ref="password" placeholder="Password" v-model="pwd"
                                ></div>
                    <div>
                        <button class="waves-effect waves-light btn" @click="login">Let me in <i class="material-icons right" v-bind:class="{ working: ajaxInProgress }">send</i></button>
                    </div>
                    <i class="material-icons close" @click="hideLoginBox">clear</i>
                </form>
            </div>
        </transition>
        <div class="site-header">
            <h1>mCarte</h1>
            <h3>Restaurant menu that is readable on your phone</h3>

            <div id="login-links">
                Restaurant owners:
                <a href="#" v-if="logged_in" @click="show_admin=!show_admin">Manage menu</a>
                <a href="#" v-if="!logged_in" @click="showLoginBox">Log in</a> |
                <a href="#" v-if="logged_in" @click="logout">Log out</a>
                <a href="#" v-if="!logged_in">Sign up</a>
            </div>
        </div>
    
        <transition name="expand-admin">
            <Admin :visible="show_admin" :userObj="userObj"></Admin>
        </transition>
    </div>

    

</template>

<script>
import Vue from 'vue'
import Admin from './Admin.vue'
import * as Ecarte from '../App.vue'

export default {
	name: 'SalesHome',

    components: {
        Admin,
    },

	mounted() {
        Vue.$eventBus.$on(Ecarte.AJAX_END, () => {
            this.ajaxInProgress = false
        })
        let headers = {}
        if (localStorage.authToken) {
            headers['Authorization'] = localStorage.authToken
        }
		Vue.$http.get('/api/foo', {headers: headers})
           .then(response => {
	           this.logged_in = this.show_admin = true
		   })
		   .catch(error => {
                console.log('***** error:', error)
			if (error.response.status == 401) {
				console.log('** Need to log in **')
                this.logged_in = false
			}
			else {
                console.error('Error when calling API, ', error.response)
            }
		})
	},

	data() {
		return {
            ajaxInProgress: false,
            logged_in: false,
			show_auth_box: false,
            usernm: '',
            pwd: '',
            loginErrorMsg: '',
            show_admin: false,
            userObj: null,
		}
	},

    methods: {
        showLoginBox() {
            this.show_auth_box = true
            setTimeout(() => { this.$refs.username.select() })
        },

        hideLoginBox() {
            this.show_auth_box = false
        },

        login() {
            if (this.ajaxInProgress) // Ignore multiple clicks
                return
            console.log('api/auth...')
            this.ajaxInProgress = true
            this.loginErrorMsg = ''
            Vue.$http.post(
                '/api/login',
                {
                    username: this.usernm,
                    password: this.pwd
                }).then(data => {
                    console.log('/api/login data:', data)
                    // TODO: Add a shake animation if incorrect
                    if (data.data.error)
                        this.loginErrorMsg = data.data.error
                    else {
                        localStorage.authToken = data.data.authToken
                        this.logged_in = true
                        this.show_auth_box = false
                        // AccountAdmin component will edit this, so would have to pass
                        // a prop two levels down. Just don't feel like doing that
                        App.userObj = {
                            id: data.data.userid,
                            username: data.data.username,
                            email: data.data.email,
                            fullName: data.data.fulname
                        }
                        // Need a delay due to hide login box animation
                        setTimeout(() => {
                            this.show_admin =true
                        }, 750)
                        
                    }
                })
        },

        logout() {
            localStorage.removeItem('authToken')
            this.logged_in = this.show_admin = false
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
    @import url('https://fonts.googleapis.com/css?family=Oswald:200,300,400,500,600');    

    #main {
        position: relative;

        .site-header {
            position: relative;
            background-color: black;
            color: yellow;
            margin: 15px 20px 0 15px;
            padding: 5px 25px 20px 25px;
            opacity: 0.65;
            border-radius: 10px;

            h1 {
                font-size: 40px;
                font-weight: 500;
                color: #FF6700;
                font-family: 'Oswald';
                letter-spacing: 8px;
                margin: 0 0 10px 0;
            }

            h3 {
                font-family: 'Oswald';
                font-size: 20px;
                letter-spacing: 3px;
                font-weight: 200;
                color: orange;
                margin: 0;
            }
        }
    }

    #login-links {
        position: absolute;
        top: 15px;
        right: 15px;
        font-family: Arial;
        font-size: 13px;
        color: #aaa;

        a {
            color: yellow;
            text-decoration: none;
            padding: 3px 5px;
        
            &:hover {
                background-color: yellow;
                color: black;
                border-radius: 3px;
            }     
        }
    }

    #auth-box {
        position: absolute;
        top: 180px;
        left: 50%;
        width: 400px;
        margin-left: -200px;
        display: inline-block;
        padding: 5px 20px 20px 20px;
        background-color: black;
        opacity: 0.85;
        z-index: 500;
        border-radius: 10px;

        h2 {
            font-family: "Oswald";
            font-size: 18px;
            color: orange;
            letter-spacing: 2px;
        }

        input,
        :-webkit-autofill,
        :-webkit-autofill:hover, 
        :-webkit-autofill:focus {
            font-family: Arial;
            font-size: 16px;
            -webkit-text-fill-color: black;
            color: orange;
            background-color: #eee !important;
            border: solid 1px orange !important;
            border-radius: 5px;
            padding: 3px 10px !important;
            margin-bottom: 8px;
            width: 85%;
            opacity: 1.0;
        }

        ::placeholder, :-ms-input-placeholder, ::-ms-input-placeholder {
            color: #aaa;
        }

        i.close {
            color: white;
            position: absolute;
            top: 15px;
            right: 15px;
            cursor: pointer;

            &:hover {
                text-shadow: 0 0 8px yellow;
            }
        }
    }

    .error-msg {
        font-face: Arial;
        font-size: 18px;
        color: #ed6969;
        margin-bottom: 15px;
    }

    .authbox-fade-enter-active, .authbox-fade-leave-active {
        transition: all 0.5s ease;
    }

    .authbox-fade-enter, .authbox-fade-leave-to {
        opacity: 0;
        transform: translateY(-250px);
    }

    button i.working {
        transition: 5s;
        transform:rotate(720deg);
    }

    .expand-admin-enter-active, .expand-admin-leave-active {
        transition: max-height 1.5s ease-out;
    }

    .expand-admin-enter, .expand-admin-leave-to {
        max-height: 0;
    }

    .expand-admin-enter-to, .expand-admin-leave {
        max-height: 5000px;
    }
</style>

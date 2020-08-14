import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex, axios);


const is_auth = window.localStorage.getItem('auth-token')
const auth_token = is_auth ? is_auth : null

const is_login = localStorage.getItem('auth-user')
const authUser = is_login ? JSON.parse(is_login) : null

const serv = localStorage.getItem('auth-service')
const service = serv ? JSON.parse(serv) : null


export const store = new Vuex.Store({
    state: {
        auth_token: auth_token,
        authUser: authUser,
        service: service
    },
    getters: {
        getToken(state){
            return state.auth_token;
        },
        getAuthUser(state){
            let authUser = state.auth_token ? state.authUser : null 
            return authUser
        },
        isLoggedIn(state){
            if(state.auth_token){
                return true
            }else{
                return false
            }
        },
        getServFromStore(state)
        {
            return state.service
        }
    },
    actions: {
        getAuthUser(context){
            let token = window.localStorage.getItem('auth-token')
            const config = {
                headers: {
                    'Authorization': 'Token '+ token
                }
            }
            axios.get('http://localhost:8000/api/profile/', config).then((res) => {
                context.commit('set_user', res.data)
                localStorage.setItem('auth-user', JSON.stringify(res.data))
                console.log(res.data)
            })
        },
    },
    mutations: {
        store_token(state, payload){
            state.auth_token = payload
        },
        set_user(state, payload){
            state.authUser = payload
        },
        logout(state){
            window.localStorage.removeItem('auth-token')
            window.localStorage.removeItem('auth-user')
            state.auth_token = null
            state.authUser = null
        },
        store_service(state, payload)
        {
            state.service = payload
            localStorage.setItem('auth-service', JSON.stringify(payload))
        }
    }
})

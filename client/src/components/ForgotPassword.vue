<template>
    <v-container>
        <v-row justify="center">
            <v-col cols="12" md="5" v-if="!passwordRequestMail">
                 <v-card light shaped elevation="6" min-height="250" class="mt-10" >
                    <v-card-title class="title primary white--text justify-center font-weight-thin">Did You Forget Your Password?</v-card-title>
                    <v-card-text class="mt-5">
                        <v-text-field label="Enter Your Email" v-model="email" required v-validate="'required|email'" :error-messages="errors.collect('email')" name="email"></v-text-field>
                    </v-card-text>
                    <v-card-actions class="justify-center">
                        <v-btn color="primary white--text" large @click="retrieve" :loading="loading">Retrieve My Password</v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
            <v-col cols="12" md="10" v-else>
                <v-alert type="success" class="my-6">
                    An email has been sent to your email <strong>{{ email }}</strong>. Please visit your email inbox and follow the instructions contained. Thank you for using ejika.com
                </v-alert>
            </v-col>
            <v-snackbar v-model="passwordRequestFailed" :time="12000" top color="red darken-2 white--text">
                Password reset request failed. Please use an email registered on our website and ensure you have good network connection.
                <v-btn text color="white--text" @click="passwordRequestFailed = false">Close</v-btn>
            </v-snackbar>
        </v-row>
    </v-container>
</template>

<script>
    export default{
        data(){
            return{
                email: '',
                api: 'http://localhost:8000/',
                loading: false,
                passwordRequestFailed: false,
                passwordRequestMail: false,
            }
        },
        beforeRouteEnter(to, from, next) {
            next(vm => {
            if (vm.authToken) {
                next("/");
            }
            });
        },
        methods: {
            retrieve(){
                this.$validator.validateAll().then(isValid => {
                    if (isValid) {
                        this.loading = true
                        this.$axios.post(this.api + 'api/request_password_reset/', {
                            email: this.email
                        }).then(() => {
                            this.loading = false
                            this.passwordRequestMail = true
                        }).catch(() => {
                            this.loading = false
                            this.passwordRequestFailed = true
                        })
                    }
                })
            }
        }
    }

</script>
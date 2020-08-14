<template>
    <v-container>
        <v-row justify="center">
            <v-col cols="12" md="6">
                <v-card light shaped elevation="6" min-height="250" class="mt-10" >
                   <v-card-title class="primary white--text justify-center font-weight-light subtitle-1">Reset Password</v-card-title>
                   <v-card-text class="mt-5">
                       <v-text-field type="password" label="New Password" v-model="pswd.new" required v-validate="'required|min:5|max:20'" ref="newPswd" name="newPswd" :error-messages="errors.collect('newPswd')" data-vv-as="new password"></v-text-field>
                       <v-text-field type="password" label="Confirm New Password" v-model="pswd.conf" required v-validate="'required|confirmed:newPswd'" name="confPswd" :error-messages="errors.collect('confPswd')" data-vv-as="confirm password"></v-text-field>
                   </v-card-text>
                   <v-card-actions class="justify-center pb-8">
                       <v-btn dark large color="primary" width="60%" @click="resetPswd" :loading="loading">Save</v-btn>
                   </v-card-actions>
                </v-card>
            </v-col>
            <v-snackbar v-model="resetFail" :time="12000" top color="red darken-2 white--text">
                Password reset failed. Please ensure the password is between 5 and 20 characters long and that you have good network connection.
                <v-btn text color="white--text" @click="resetFail = false">Close</v-btn>
            </v-snackbar>
        </v-row>
    </v-container>
</template>

<script>
    export default{
        data(){
            return{
                email: this.$route.params.email,
                token: this.$route.params.token,
                api: 'http://localhost:8000/',
                loading: false,
                invalidRequest: false,
                showPasswordForm: false,
                pswd: {
                    new: '',
                    conf: ''
                },
                resetFail: false
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
            verifyToken(){
                this.$axios.get(this.api + `api/verify_token/${this.email}/${this.token}/`, ).then((res) => {
                    if(res.data.message=='ok'){
                        this.showPasswordForm = true
                    }else{
                        this.invalidRequest = true
                    }
                }).catch(() => {
                    this.invalidRequest = true
                })
            },
            resetPswd(){
                this.$validator.validateAll().then(isValid => {
                    if (isValid) {
                        this.loading = true
                        this.$axios.put(this.api + 'api/reset_password/', {
                            token: this.token,
                            password: this.pswd.new,
                            c_password: this.pswd.conf
                        }).then(() =>{
                            this.loading = false
                            this.pswd.new = ''
                            this.pswd.conf = ''
                            this.$router.push('/password_reset_success')
                        }).catch(()=>{
                            this.resetFail = true
                        })
                    }
                })
            }
        },
        created(){
            this.verifyToken()
        }
    }

</script>
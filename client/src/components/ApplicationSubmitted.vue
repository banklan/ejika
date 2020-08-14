<template>
    <v-container>
        <v-row justify="center" class="mt-8 mb-8">
            <v-col cols="12" md="8">
                <v-card light color="green lighten-3" outlined min-height="40" class="my-8">
                    <v-card-title>Thank you for contacting us.</v-card-title>
                    <v-card-text class="subtitle-1">
                        <v-alert type="success">
                            Your application for application finance has been sent. We will contact you through your phone number <strong>+234 {{ application.phone }}</strong> or email address <strong>{{ application.email }}</strong> shortly.
                        </v-alert>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    data(){
        return{
            application: null
        }
    },
    beforeRouteLeave (to, from, next) {
        const sent = localStorage.removeItem('app-sent')
        if(sent){
            next()
        }else{
            next()
        }
    },
    created(){
        this.application = JSON.parse(localStorage.getItem('app-sent'))
    }
}
</script>
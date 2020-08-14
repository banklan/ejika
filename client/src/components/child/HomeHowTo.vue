<template>
    <div class="how_to" id="home_how_to">
        <v-row justify="center">
            <v-col cols="12" md="10" class="justify-center">
                <v-card light shaped color="rgba(228, 228, 228, 0.194)" elevation="6" class="justify-center mx-auto" min-height="400">
                    <v-card-title class="justify-center headline font-weight-light">
                        Be a verified professional, improve your marketability.
                    </v-card-title>
                    <v-card-text>
                        <v-list>
                            <v-list-item-group v-model="item" color="primary">
                                <v-list-item v-for="(how, i) in hows" :key="i">
                                    <v-list-item-icon>
                                        <v-icon v-text="how.icon" large color="accent"></v-icon>
                                    </v-list-item-icon>
                                    <v-list-item-content>
                                        <v-list-item-title v-text="how.text" class="wrap-list"></v-list-item-title>
                                    </v-list-item-content>
                                </v-list-item>
                            </v-list-item-group>
                        </v-list>
                    </v-card-text>
                    <v-card-actions class="justify-center pb-6">
                        <v-btn dark color="accent" rounded x-large class="pa-3 mb-3" to="/register">Join our Professionals</v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>


<script>
export default {
    data(){
        return{
            item: 1,
            hows: [
                {text: "Our main aim is to provide a platform for small/medium service providers to showcase their services to potential clients in their circles.", icon: 'store'},
                {text: "Register, fill in all relevant information correctly.", icon: 'mdi-login'},
                {text: 'Create portfolio showing previous jobs, uploading images of same.', icon: 'camera'},
                {text: 'Ensure you fill in your full business addresses, so it can be easily located on a map, using landmarks where necessary.', icon: 'place'},
                {text: 'Supply your correct mobile phone number, website and social media handles, so potential clients can visit and know more about your services.', icon: 'phone'},
                {text: 'After verifying all information supplied, your account will be marked verified.', icon: 'check_circle'},
            ]
        }
    }
}
</script>
<style lang="scss" scoped>
    .v-card{
        margin-top: 2rem !important;
        .v-card__title.headline{
            padding-top: 40px !important;
            font-size: 1.7rem !important;
        }
        .wrap-list{
            font-size: 21px;
            word-wrap: break-word !important;
            -webkit-line-clamp: 3 !important;
            white-space: normal;
            overflow: hidden;
            line-height: 1.8;
        }
    }
</style>
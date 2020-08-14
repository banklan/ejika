<template>
    <div class="contact">
        <div class="banner"></div>
        <v-container>
            <v-row justify="center" class="text-center">
                <v-col cols="10" md="10">
                    <template v-if="!enquirySent">
                        <v-card elevation="12" light min-height="400" class="mx-auto pt-3">
                            <v-card-title class="font-weight-light headline justify-center mt-3">Drop us a line</v-card-title>
                            <v-card-text class="mt-3">
                                <v-row justify="space-around">
                                    <v-col cols="12" md="6">
                                        <v-text-field label="First Name" v-model="enquiry.f_name" solo dense name="f_name" required v-validate="'required|min:2|max:30'" :error-messages="errors.collect('f_name')" data-vv-as="first name"></v-text-field>
                                        <v-text-field label="Last Name" v-model="enquiry.l_name" solo dense name="l_name" required v-validate="'required|min:2|max:30'" :error-messages="errors.collect('l_name')" data-vv-as="last name"></v-text-field>
                                        <v-row wrap>
                                            <v-col cols="6">
                                                <v-text-field label="Email Address" v-model="enquiry.email" solo dense name="email" required v-validate="'required|email'" :error-messages="errors.collect('email')"></v-text-field>
                                            </v-col>
                                            <v-col cols="6">
                                                <v-text-field label="Phone No" v-model="enquiry.phone" solo dense name="phone" required v-validate="'required|numeric|max:14'" :error-messages="errors.collect('phone')"></v-text-field>
                                            </v-col>
                                        </v-row>
                                        <v-text-field label="Subject" v-model="enquiry.subject" solo dense name="subject" required v-validate="'required|min:3|max:100'" :error-messages="errors.collect('subject')"></v-text-field>
                                        <v-textarea label="Message" v-model="enquiry.message" rows="4" auto-grow solo dense name="message" required v-validate="'required|min:5|max:300'" :error-messages="errors.collect('message')"></v-textarea>
                                        <v-btn block dark large color="primary" class="my-3" @click="sendEnquiry" :loading="loading">Send Enquiry</v-btn>
                                    </v-col>
                                    <v-col cols="12" md="5">
                                        <div class="subtitle-1 font-weight-bold mt-5">You can reach us on any of the following means:</div>
                                        <v-list>
                                            <v-list-item-group>
                                                <v-list-item v-for="(contact, i) in contacts" :key="i">
                                                    <v-list-item-icon>
                                                        <v-icon v-text="contact.icon" color="accent"></v-icon>
                                                    </v-list-item-icon>
                                                    <v-list-item-content>
                                                        <v-list-item-title v-text="contact.text"></v-list-item-title>
                                                    </v-list-item-content>
                                                </v-list-item>
                                            </v-list-item-group>
                                        </v-list>
                                        <div class="socials mt-8 pa-2">
                                            <div class="subtitle-1 mb-4 font-weight-bold">Follow us on our social media accounts.</div>
                                            <div class="d-flex justify-space-around">
                                                <v-btn v-for="item in socials" :key="item.icon" icon :href="`${item.link}`" target="_blank" link>
                                                    <v-icon :color="item.color" v-text="item.icon"></v-icon>
                                                </v-btn> 
                                            </div>
                                        </div>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-card>
                    </template>
                    <template v-if="enquirySent">
                        <v-alert type="success">
                            Your enquiry has been sent. We will contact you shortly.
                        </v-alert>
                    </template>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
export default {
    data(){
        return{
            contacts: [
                {icon: 'email', text: 'info@ejika.com'},
                {icon: 'phone', text: '08023456789'},
                {icon: 'place', text: 'Some Address Here'},
            ],
            socials: [
                {icon: 'mdi-facebook', color: '#1877f2', link: 'https://www.facebook.com/ejika'},
                {icon: 'mdi-twitter', color: '#1da1f2', link: 'https://www.twitter.com/ejika'},
                {icon: 'mdi-instagram', color: '#c32aa3', link: 'https://www.instagram.com/ejika'},
            ],
            loading: false,
            enquiry: {
                f_name: '',
                l_name: '',
                email: '',
                phone: '',
                subject: '',
                message: ''
            },
            api: 'http://localhost:8000/api/',
            enquirySent: false
        }
    },
    methods:{
        sendEnquiry(){
            this.$validator.validateAll().then(isValid => {
                if (isValid) {
                    this.loading = true
                    this.$axios.post(this.api + 'send_enquiry/', {
                        f_name: this.enquiry.f_name,
                        l_name: this.enquiry.l_name,
                        email: this.enquiry.email,
                        phone: this.enquiry.phone,
                        subject: this.enquiry.subject,
                        message: this.enquiry.message,
                    }).then(() => {
                        this.loading = false
                        this.enquirySent = true
                    }).catch(() =>{
                        this.loading = false
                    })
                }
            })
        }
    },
}
</script>

<style scoped lang="scss">
    .contact{
        width: 100vw;
        background: rgba(238, 238, 238, .39);

        .banner{
            height: 18rem;
            width: 100%;
            background-image: linear-gradient(to bottom right, rgba(0, 59, 99, 0.89), rgba(255, 23, 69, 0.623)), url('../statics/images/contact.jpg');
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
        }
        .v-card{
            margin-top: -7rem; 
            z-index: 1000;
            margin-bottom: 8rem;

            .v-list{
                .v-list-item__content{
                    flex: none !important;
                }
            }
        }
    }
</style>
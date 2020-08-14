<template>
    <div class="footer" color="#08192B" light>
        <v-container>
            <v-row wrap class="main" justify="center">
                <v-col cols="6" md="4">
                    <div class="link_wrap">
                        <p class="white--text ml-n7">Quick Links</p>
                        <ul>
                            <li><router-link to="/register">Join Our Professionals</router-link></li>
                            <li><router-link to="/services">Search For Service</router-link></li>
                            <li><router-link to="/how_it_works">How it works</router-link></li>
                            <li><router-link to="/about_us">About Us</router-link></li>
                        </ul>
                    </div>
                </v-col>
                <v-col cols="6" md="4">
                    <div class="link_wrap">
                        <p class="white--text ml-7">Quick Links</p>
                        <ul>
                            <li><router-link to="/">Home </router-link></li>
                            <li><router-link to="/login">Login </router-link></li>
                            <li><router-link to="/contact_us">Contact Us</router-link></li>
                            <li><router-link to="/testimonials">Testimonials</router-link></li>
                        </ul>
                    </div>
                </v-col>
                <v-col cols="6" md="4">
                    <div class="link_wrap">
                        <p class="white--text ml-n12">Extras</p>
                        <ul>
                            <li><router-link to="/appliances_financing">Appliances Financing</router-link></li>
                            <li><router-link to="/advert">Promote Your Business</router-link></li>
                            <li><router-link to="/terms_conditions">Terms & Conditions</router-link></li>
                            <li><router-link to="/privacy_policy">Privacy Policy</router-link></li>
                            <li><router-link to="/faq">FAQ</router-link></li>
                        </ul>
                    </div>
                </v-col>
            </v-row>
        </v-container>
            <v-row justify="center" class="base">
                <v-col cols="6" class="text-center">
                    <v-btn large v-for="icon in icons" :key="icon.name" class="white--text mx-4" icon :href="`${icon.link}`" target="_blank" link>
                        <v-icon :color="icon.color">{{ icon.name }}</v-icon>
                    </v-btn>
                </v-col>
                <v-col cols="6" class="text-center">
                    <div class="body-2 pt-2 white--text">&copy; {{ new Date().getFullYear() }} ejika.com All rights reserved </div>
                </v-col>
            </v-row>
    </div>
</template>

<script>
export default {
    data(){
        return{
            icons: [
                {name: 'mdi-facebook', color:'#1877f2', link:'https://www.facebook.com/ejika'},
                {name: 'mdi-twitter', color: '#1da1f2', link: 'https://www.twitter.com/ejika'},
                {name: 'mdi-instagram', color: '#c32aa3', link: 'https://www.instagram.com/ejika'}
            ],
        }
    }
}
</script>

<style scoped lang="scss">
    .footer{
        background-color: #08192B;
        width: 100vw !important;
        // margin-top: 40px;
    
        .main{
            color: #242729;
            min-height: 10rem;
            display: flex !important;
            justify-content: space-around !important;
            align-items: center;

            .link_wrap{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                flex-wrap: wrap;
                
                p{
                    text-align: left;
                }
                ul{
                    list-style: none;
                    margin-left: 10px;

                    li{
                        line-height: 1.8;
                        padding-bottom: 10px;
                    
                        a{
                            text-decoration: none;
                            color: #cfcccc;
                            transition: all .4s;
                            font-size: 15px;

                            &:hover{
                                color:rgb(255, 255, 255);
                            }
                        }
                    }
                }
            }

            
        }
        .base{
            background-color: #002E4F;
        }
    }
</style>
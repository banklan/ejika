<template>
    <div class="how_it_works">
        <div class="banner"></div>
        <v-container>
            <v-row justify="center">
                <v-col cols="12" md="10">
                    <v-card shaped light min-height="400" class="mx-auto px-5 py-5 mt-5">
                        <v-card-title class="justify-center headline mb-3 font-weight-light">How it works</v-card-title>
                        <v-card-subtitle class="title primary--text">To search for a service within your locality.</v-card-subtitle>
                        <v-card-text class="subtitle-1">
                            <v-list>
                                <v-list-item-group color="primary">
                                    <v-list-item v-for="(how, i) in howTo1" :key="i">
                                        <v-list-item-content>
                                            {{ how.text | capFirstLetter }} 
                                        </v-list-item-content>
                                    </v-list-item>
                                    <v-list-item class="mt-4">
                                        <v-list-item-content>
                                            Visit our <router-link to="/terms_conditions">Terms & Condition</router-link> page and read carefully through before you use this site.
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-list-item-group>
                            </v-list>
                        </v-card-text>
                    </v-card>
                    <v-card shaped light min-height="400" class="mx-auto mt-8 py-5 px-5">
                        <v-card-subtitle class="title primary--text">To register as a professional/service provider.</v-card-subtitle>
                        <v-card-text class="subtitle-1">
                            <v-list>
                                <v-list-item-group>
                                    <v-list-item>
                                        <v-list-item-content>
                                            Go to <router-link to="/register">Register page</router-link>, fill your personal details to register. Once successfully registered, login with your email and password. 
                                        </v-list-item-content>
                                    </v-list-item>
                                    <v-list-item>
                                        <v-list-item-content>
                                            Go to <router-link to="/profile">Profile</router-link>. Click on Services, then Add Service. Kindly ensure you give correct information of your services, including your business address, so it can be correctly captured on the map.
                                        </v-list-item-content>
                                    </v-list-item>
                                    <v-list-item>
                                        <v-list-item-content>
                                            Add portfolio showing the jobs you have done in the past, including images. Portfolios are your selling points. PLEASE DO NOT POST OTHER PEOPLE'S IMAGES TO AVOID COPYRIGHT INFRINGEMENTS.
                                        </v-list-item-content>
                                    </v-list-item>
                                    <v-list-item>
                                        <v-list-item-content>
                                            Be clear on your terms, pricing, timing and everything else clients needs to know to help them make decisions when creating your service.
                                        </v-list-item-content>
                                    </v-list-item>
                                    <v-list-item>
                                        <v-list-item-content>
                                            We will take issues of falsification and scamming of clients on this site seriously and legally. Kindy ensure all dealings with clients are done in all honesty.
                                        </v-list-item-content>
                                    </v-list-item>
                                    <v-list-item>
                                        <v-list-item-content>
                                            Do ensure that your business address, mobile phone numbers, email addresses, websites and other social media handles supplied are correct.
                                        </v-list-item-content>
                                    </v-list-item>
                                    <v-list-item>
                                        <v-list-item-content>
                                            Do not hesitate to report any mis-dealings with clients met on this site to us through any of the means listed on our <router-link to="/contact_us">Contact Page</router-link>. When contacting us, kindly supply every relevant details of the transaction and client.
                                        </v-list-item-content>
                                    </v-list-item>
                                    <v-list-item>
                                        <v-list-item-content>
                                            Do not accept money from any client until you meet them in person and have a concrete agreement as to the execution of the job/service.
                                        </v-list-item-content>
                                    </v-list-item>
                                    <v-list-item class="mt-4">
                                        <v-list-item-content>
                                            Visit our <router-link to="/terms_conditions">Terms & Condition</router-link> page and read carefully through before you use this site.
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-list-item-group>
                            </v-list>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
export default {
    data(){
        return{
            howTo1: [
                {text: 'This site was created to help start-ups and medium service providers and professionals to list their services and showcase their portfolio. We do not allow listing of physical products on this site.'},
                {text: 'From the home page, choose your state and the category of the service you are searching for, or click on Services on the menu.'},
                {text: 'You can also search for name of service provider, category or keywords, if known.'},
                {text: 'Filter to a subcategory or simply scroll through the list of displayed services.'},
                {text: 'When you find a service you want, click to open the service page, go through the profile, portfolio and reviews of previous clients.'},
                {text: 'Kindly note that we do not accept responsibilities of any mis-dealings from any service providers. Users are to ensure they carry out their own due diligence before engaging the services of any service provider.'},
                {text: 'We implore our users to always write objective reviews after dealing with any service provider on their pages. This will help guide potential clients in the choice of services and professionals.'},
                {text: 'Do not hesitate to contact us to report any unprofessional or unpleasant encounter with any of the service providers listed on our website. When contacting us, kindly supply all relevant details of the encounter.'},
                {text: 'DO NOT PAY FOR ANY SERVICES before meeting professionals and having a concrete agreement with them first. It is advisable to keep evidence of agreements and payments to service providers.'}
            ],
        }
    }
}
</script>

<style lang="scss" scoped>
    .how_it_works{
        background: rgba(243, 243, 243, 0.5);

        .banner{
            min-height: 18rem;
            width: 100%;
            background-image: linear-gradient(to bottom right, rgba(0, 59, 99, 0.89), rgba(255, 23, 69, 0.623)), url('../statics/images/how.jpg');
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .v-list{
            .v-list-item__content{
                font-size: 18px !important;
                line-height: 1.80;
                font-family: 'Source Sans Pro', sans-serif;
                display: inline-block !important;
                tranition: all .4s;
                a{
                    text-decoration: none;
                    &:hover{
                        color: #002E4F !important;
                    }
                }
            }
        }
    }
</style>
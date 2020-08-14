<template>
    <div class="about">
        <div class="banner"></div>
        <v-container>
            <v-row wrap justify="center">
                <v-col cols="12" md="10">
                    <v-card shaped light class="mx-auto mt-8 pa-8">
                        <v-card-title class="headline font-weight-light justify-center">Our Story</v-card-title>
                        <v-card-text>
                            <div class="title mb-3 font-weight-bold">Our Mission</div>
                            <div class="mission mb-6 font-weight-bold">To help provide the online platform that gives start-ups and mid-size service providers the needed visibility and marketability to thrive their businesses.</div>
                            <p>Welcome to ejika.com, an online resource dedicated to empowering small scale artisans, professionals, start-ups and medium-sized companies to achieve success.</p>
                            <p>We are a brand borne out of a pressing desire to bridge the gap between the tools the big bluechip organizations use as an advantage over the small-scale start-ups and medium-sized companies. Global online presence. </p>
                            <p>In an era where almost every economic and social factors (among others) work against start-ups, providing a platform where they can list and showcase their services and portfolios for free will no doubt go a long way to address some of the gaps.
                            </p>
                            <p>At Ejika, we help you re-discover your business and provide a platform to launch your services to the consciousness of your local market.</p>
                            <p>Our directory boasts of thousands of unique visitors every month who search for service providers, based on categories and location-specific listings. 
                                Service providers can take advantage of this, to customize their service page and express themselves, just the way it suits their businesses. Our feedback tools can also help them 
                                gain key knowledge vital to help grow their businesses.</p>
                            <p>Whats more? We help you harness the powerful magic of social media to propagate your unique business ideas to the people and market that matters. Our aim is to develop a close bond with you
                                that will enable us gain insight into and share in your dreams. Beeing a part of your success story is our motivation and fulfillment indeed.
                            </p>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<style lang="scss" scoped>
    .about{
        background: rgba(238, 238, 238, .39);
        width: 100vw !important;

        .banner{
            height: 18rem;
            width: 100%;
            background-image: linear-gradient(to bottom right, rgba(0, 59, 99, 0.89), rgba(255, 23, 69, 0.623)), url('../statics/images/about.jpg');
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
        }
        .v-card__text{
            font-family: 'Source Sans Pro', sans-serif;
            line-height: 1.80;
            color: rgba(0,0,0,.88) !important;

            .mission{
                font-size: 20px;
                line-height: 1.7;
            }
            p{
                font-size: 18px !important;
                line-height: 1.80;
                font-family: 'Source Sans Pro', sans-serif;
            }
        }
    }
    
</style>
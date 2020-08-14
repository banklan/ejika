<template>
    <div class="faq">
        <div class="banner"></div>
        <v-container>
            <v-row wrap justify="center">
                <v-col cols="12" md="10">
                    <v-card flat shaped min-height="600" class="mt-6 mx-auto">
                        <v-card-title class="headline mb-3 justify-center font-weight-bold">Frequently Asked Questions</v-card-title>
                        <v-card-text>
                            <div class="faqs" v-for="(faq, i) in faqs" :key="i">
                                <div class="title mb-3">{{ faq.sn }}. {{ faq.question }}</div>
                                <div class="answers mb-5 pl-5"><strong>Answer: </strong> {{ faq.answer }} </div>
                            </div>
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
            faqs: [
                {sn: '1', question: 'Does Ejika guarantee the originality and accept responsibility for any loss or damage that happens while engaging the use of any service provider listed on this site?', answer: 'No. While we seek to ensure that services listed on our websites are genuine and take intentional steps to verify the authenticity of such services, we wish to state categorically that we do not accept any liability for any loss that may arise from the engagement of such service providers. It remains the sole responsibilty of users to carry out due diligence to ensure they are dealing with a non-fraudulent service providers.'},
                {sn: '2', question: 'Does Ejika charge service providers who list their services on the website?', answer: 'At the moment, we do not charge service providers for listing their services and publishing their services on ejika,com, it id absolutely free. However, this might change in the future.'},
                {sn: '3', question: 'Does Ejika charge for advertisement of services?', answer: 'For a service to be prominently displayed and priotized, we will charge a fee. This will help us in taking care of overheads such as website maintenance and hosting fees.'},
                {sn: '4', question: 'Do we allow publishing of physical products or items on our site?', answer: 'No. This website is targeted at small and medium scale service providers, who provides intangible services(services that can not be touched or seen in the real sense, like drycleaning, plumbig, house-cleaning, security etc). We will delete contents that are not services.'},
                {sn: '5', question: 'Does Ejika give preference for some kind of services while displaying on our site?', answer: 'No. As long as the services published do not contravene our policies and terms, we treat all services equally. However, services paid for understandably gets priotized and enjoys more visibility.'},
                {sn: '6', question: 'Does Ejika confirm the genuiness of services posted on our site?', answer: 'While we carry out some checks to confirm the services do exist and the claims are genuine, unfortunately we still do not guarantee if the services listed are genuine. Potential clients are expected to run their on background checks before engaging the services.'},
                {sn: '7', question: 'A Service Provider asked that i pay an upfont sum before commencing a job, what should i do?', answer: 'We strongly recommend that before any financial transactions take place, clients should meet with the SP, confirm their genuiness and ability to do the job. PAYMENTS SGOULD NOT BE MADE BEFORE MEETING ANY SERVIE PROVIDER LISTED ON OUR SITE.'},
                {sn: '8', question: 'In the event of a Service Provider scamming me, what should i do?', answer: 'Immediately you notice that a SP is acting fraudulently, kindly contact us via email or our mobile number listed on our Contact page. We will blacklist such SP and renove their profiles from our site. If they have been paid for a service and fails to meet up with their obligations, consider reporting them to law enforcement agents.'},
                {sn: '9', question: 'I tried posting my service on the site, it showed that it was successful but i cannot find it on the site.', answer: 'Every service published will be approved by our admins before it appears on the listing. So, just be patient.'},
                {sn: '10', question: 'I got a call from someone purpotedly from Ejika to pay an amount before my service is listed on the site.', answer: 'Ejika will not call to request for payment before listing your service. At the moment, listing of services on our platform is absolutely free, except for premium services. If you get such call or message, kindly report to us immediately.'},
                {sn: '11', question: 'Can i publish multiple services with same account?', answer: 'No. You can only publish a service with your account but can publish a maximum of 5 portfolio with an account.'},
            ]
        }
    }
}
</script>

<style lang="scss" scoped>
    .faq{
        background: rgba(238, 238, 238, 0.5);

        .banner{
            height: 18rem;
            width: 100%;
            background-image: linear-gradient(to bottom right, rgba(0, 59, 99, 0.89), rgba(255, 23, 69, 0.623)), url('../statics/images/faq.jpg');
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
        }
        .v-card__text{
            line-height: 1.75 !important;
            color: rgba(0, 0, 0, .88) !important;

            .title{
                font-size: 19px !important;
            }
            .answers{
                font-size: 18px !important;
                line-height: 1.80;
                font-family: 'Source Sans Pro', sans-serif;
            }
        }
    }
    
</style>
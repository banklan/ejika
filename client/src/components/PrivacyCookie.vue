<template>
    <v-container>
        <v-row wrap justify="center">
            <v-col cols="12" md="10">
                <v-card flat shaped min-height="600" class="mt-6 mx-auto">
                    <v-card-title class="headline mb-3 justify-center font-weight-bold">Privacy And Cookie Policy</v-card-title>
                    <v-card-text>
                        <div class="policy">
                            <div class="title mb-3">1. About this Notice</div>
                            <p>This Privacy and Cookie Notice provides information on how Jumia collects and processes your personal data when you visit our website or mobile applications.</p>
                        </div>
                        <div class="policy">
                            <div class="title mb-3">2. The Data We Collect About You?</div>
                            <p>We collect your personal data in order to provide and continually improve our products and services. We may collect, use, store and transfer the following different kinds of personal data about you: Here for marketing and personal data optimization purposes. Jumia also uses Google Digital Marketing to propose targeted offers.
                               To find out more:
                               <ol>
                                   <li>Information you provide to us: We receive and store the information you provide to us including your identity data, contact data, delivery address and financial data.</li>
                                   <li>Information on your use of our website and/or mobile applications: We automatically collect and store certain types of information regarding your use of the Ejika web app including information about your searches, views, locations and clicks.</li>
                                   <li>Information from third parties and publicly available sources: We may receive information about you from third parties including our carriers; and advertising service providers.</li>
                               </ol>
                            </p>
                        </div>
                        <div class="policy">
                            <div class="title mb-3">3. Cookies and How We Use Them</div>
                            <p>A cookie is a small file of letters and numbers that we put on your computer if you agree.
                               Cookies allow us to distinguish you from other users of our website and mobile applications, which helps us to provide you with an enhanced browsing experience. For example we use cookies for the following purposes:
                                <ol>
                                    <li>Recognising and counting the number of visitors and to see how visitors move around the site when they are using it (this helps us to improve the way our website works, for example by ensuring that users can find what they are looking for).</li>
                                    <li>Identifying your preferences and subscriptions e.g. language settings, saved items, items stored in your basket and Prime membership; and</li>
                                    <li>Sending you newsletters and commercial/advertising messages tailored to your interests.</li>
                                </ol>
                                Our approved third parties may also set cookies when you use our marketplace. Third parties include search engines, providers of measurement and analytics services, social media networks and advertising companies.
                            </p>
                        </div>
                        <div class="policy">
                            <div class="title mb-3">4. How We Use Your Personal Data</div>
                            <p>We use your personal data to operate, provide, develop and improve the services that we offer, including the following:
                                <ol>
                                    <li>Registering you as a new user.</li>
                                    <li>Managing your relationship with us.</li>
                                    <li>Improving our website, applications, services.</li>
                                    <li>Recommending/advertising services which may be of interest to you.</li>
                                    <li>Complying with our legal obligations, including verifying your identity where necessary.</li>
                                    <li>Detecting fraud.</li>
                                </ol>
                            </p>
                        </div>
                        <div class="policy">
                            <div class="title mb-3">5. How We Share Your Personal Data</div>
                            <p>We may need to share your personal data with third parties when it becomes legally neccessary.</p>
                            <p>When we share your personal data with third parties we:
                                <ol>
                                    <li>require them to agree to use your data in accordance with the terms of this Privacy and Cookie Notice, our Privacy Policy and in accordance with the law; and</li>
                                    <li>only permit them to process your personal data for specified purposes and in accordance with our instructions. We do not allow our third-party service providers to use your personal data for their own purposes.</li>
                                </ol>
                            </p>
                        </div>
                        <div class="policy">
                            <div class="title mb-3">Data Security</div>
                            <p>We have put in place appropriate security measures to prevent your personal data from being accidentally lost, used or accessed in an unauthorised way, altered or disclosed.</p>
                            <p>In addition, we limit access to your personal data to those employees, agents, contractors and other third parties who have a business need to know. They will only process your personal data on our instructions and they are subject to a duty of confidentiality.</p>
                            <p>We have put in place procedures to deal with any suspected personal data breach and will notify you and any applicable regulator of a breach where we are legally required to do so.</p>
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<style lang="scss" scoped>
    .v-card__text{
        line-height: 1.75 !important;
        color: rgba(0, 0, 0, .88) !important;

        .policy{
            margin-top: 15px;

            p{
                font-size: 17px !important;
                ol{
                    padding-top: 12px;
                    margin-left: 18px !important;
                    li{
                        padding-bottom: 10px !important;
                        list-style-type:lower-alpha;
                    }
                }
            }
        }
    }
</style>
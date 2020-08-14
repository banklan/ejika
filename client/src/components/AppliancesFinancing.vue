<template>
    <div class="appliances_financing">
        <div class="banner"></div>
        <v-container>
            <v-row justify="center">
                <v-col cols="12" md="10">
                    <v-card flat light min-height="400" class="mt-8">
                        <v-card-title class="justify-center headline my-4 pt-3">Appliances Financing</v-card-title>
                        <v-card-text class="intro">
                            <p>We understand your dreams and need of acquiring household appliances and office equipments without having to pause your life. Our desires are to help you live the life you want. </p>
                            <p>This is why we are offering you flexible and convenient payment plans that suits your budget. You can choose to pay daily, weekly or monthly. </p>
                            <p class="pb-8">To get started, fill the form below and tell us just what you need. We will call you back to discuss your needs and give you a custom-rate, specific to your needs and budgets.</p>
                            <v-alert>Kindly note that the fields marked with * are required. </v-alert>
                            <v-card outlined light shaped class="mx-auto pt-3 mb-5">
                                <v-card-text>
                                    <v-row wrap>
                                        <v-col cols="12" md="6">
                                            <v-text-field label="Email*" v-model="email" required v-validate="'required|email'" name="email" :error-messages="errors.collect('email')"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" md="6">
                                            <v-select label="Title*" v-model="title" :items="title_list" item-text="name" item-value="name" required v-validate="'required'" name="title" :error-messages="errors.collect('title')"></v-select>
                                        </v-col>
                                        <v-col cols="12" md="6">
                                            <v-text-field label="First Name*" v-model="f_name" required v-validate="'required|max:30|min:3'" name="f_name" :error-messages="errors.collect('f_name')"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" md="6">
                                            <v-text-field label="Last Name / Surname*" v-model="l_name" required v-validate="'required|max:30|min:3'" name="l_name" :error-messages="errors.collect('l_name')"></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row wrap>
                                        <v-col cols="12" md="6">
                                            <v-text-field label="Phone Number*" v-model="phone" required v-validate="'required|numeric|max:14'" name="phone" :error-messages="errors.collect('phone')"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" md="6">
                                            <v-text-field label="Occupation*" v-model="occupation" required v-validate="'required|max:30'" name="occupation" :error-messages="errors.collect('occupation')"></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-text-field label="Appliance Needed*" placeholder="e.g Big Sumec Generator" v-model="appliance" required v-validate="'required|max:30'" name="appliance" :error-messages="errors.collect('appliance')"></v-text-field>
                                    <v-row wrap>
                                        <v-col cols="12" md="6">
                                            <v-text-field label="Appliance Brand" placeholder="e.g Samsung or LG" v-model="brand" v-validate="'required|max:30'" name="brand" :error-messages="errors.collect('brand')"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" md="6">
                                            <v-textarea label="Appliance Capacity/Ratings" placeholder="e.g 42 inches (for TV)" v-model="capacity" rows="1" auto-grow v-validate="'max:30'" name="capacity" :aria-errormessage="errors.collect('capacity')"></v-textarea>
                                        </v-col>
                                    </v-row>
                                    <v-textarea label="Other Information" placeholder="Any other information about appliance/equipment" v-model="other_info" rows="1" auto-grow v-validate="'max:150'" :counter="150" name="other_info" :aria-errormessage="errors.collect('other_info')"></v-textarea>
                                    <v-text-field label="Monthly Income*" placeholder="Your monthly income e.g 150000 (Without , or .)" v-model="income" required v-validate="'required|numeric'" name="income" :error-messages="errors.collect('income')"></v-text-field>
                                    <v-text-field label="Location*" placeholder="Your City, State" v-model="location" required v-validate="'required|max:50'" name="location" :error-messages="errors.collect('location')"></v-text-field>
                                    <v-row wrap>
                                        <v-col cols="6">
                                            <v-select label="How often would you prefer to re-payment?*" :items="pymt_frequency" item-text="mode" item-value="mode" v-model="frequency" v-validate="'required'" name="frequency" :error-messages="errors.collect('frequency')"></v-select>
                                        </v-col>
                                        <v-col cols="6">
                                            <v-select label="Select your tenure of re-payment*" :items="pymt_tenure" item-text="tenure" item-value="tenure" v-model="tenure" v-validate="'required'" name="tenure" :error-messages="errors.collect('tenure')"></v-select>
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                                <v-card-actions class="justify-center mb-5">
                                    <v-btn text large width="25%" color="accent">Clear</v-btn>
                                    <v-btn dark color="primary" width="25%" large @click='sendAppl' :loading="loading">Send</v-btn>
                                </v-card-actions>
                            </v-card>
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
            title: '',
            f_name: '',
            l_name: '',
            occupation: '',
            phone: '',
            email: '',
            brand: '',
            appliance: '',
            capacity: '',
            other_info: '',
            income: null,
            frequency: '',
            tenure: '',
            location: '',
            title_list: [
                {name: 'Mr.', value: 'Mr.'},
                {name: 'Miss', value: 'Miss'},
                {name: 'Mrs', value: "Mrs"},
                {name: 'Chief', value: "Chief"}
            ],
            pymt_frequency: [
                {mode: 'Daily'},
                {mode: 'Weekly'},
                {mode: 'Fortnightly'},
                {mode: 'Monthly'},
            ],
            pymt_tenure: [
                {tenure: '30 days'},
                {tenure: '60 days'},
                {tenure: '90 days'}
            ],
            loading: false,
            api: 'http://localhost:8000/api/',
        }
    },
    methods: {
        sendAppl(){
            this.$validator.validateAll().then(isValid => {
                if (isValid) {
                    this.loading = true;
                    this.$axios.post(this.api + 'send_finance_application/', {
                        title: this.title,
                        f_name: this.f_name,
                        l_name: this.l_name,
                        occupation:  this.occupation,
                        phone: this.phone,
                        email: this.email,
                        brand: this.brand,
                        appliance: this.appliance,
                        capacity: this.capacity,
                        other_info: this.other_info,
                        income: this.income,
                        tenure: this.tenure,
                        frequency: this.frequency,
                        location: this.location
                    }).then((res) => {
                        this.loading = false
                        // console.log(res.data.result)
                        localStorage.setItem('app-sent', JSON.stringify(res.data.result))
                        this.$router.push('/application_submitted')
                    }).catch(() =>{
                        this.loading = false
                    })
                }
            })
        }
    }
}
</script>   

<style lang="scss" scoped>
    .appliances_financing{
        .banner{
            min-height: 18rem;
            width: 100%;
            background-image: linear-gradient(to bottom right, rgba(0, 59, 99, 0.89), rgba(255, 23, 69, 0.623)), url('../statics/images/appliances.jpg');
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .v-card{
            .intro{
                font-size: 18px !important;
                line-height: 1.7;
                color: #3a3a3a;
            }
        }
    }
</style>
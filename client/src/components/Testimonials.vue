<template>
    <div class="testimonial">
        <div class="banner"></div>
        <v-container>
            <v-btn fixed dark elevation="12" fab bottom right color="accent" class="mt-5 mr-4" @click="testForm = true"><v-icon>add</v-icon></v-btn>
            <v-row justify="center" wrap>
                <template v-if="!testForm">
                    <template v-if="loading">
                        <v-progress-circular indeterminate color="accent" :width="7" :size="70" v-if="loading" justify="center" class="mx-auto"></v-progress-circular>
                    </template>
                    <template v-else>
                        <v-col cols="12">
                            <div class="headline text-center my-4">Testimonials</div>
                        </v-col>
                        <template v-if="testimonials.length > 0">
                            <v-col cols="12" md="10" v-for="(test, index) in testimonials" :key="test.id">
                                <div class="testimonial_card">
                                    <v-img :src="test.image" alt="Testimonial author" height="100%" width="33%" ></v-img>
                                    <div class="texts">
                                        <h4>{{ test.name | capFirstLetter }}</h4>
                                        <p class="caption">{{ test.created }}</p>
                                        <p>{{ test.text | capFirstLetter }}</p>
                                        <div v-if="isLoggedIn && authUser.id == test.user">
                                            <v-btn text @click="confirmDelDial(test.id, index)">
                                                <v-icon color="accent">delete_forever</v-icon>
                                            </v-btn>
                                        </div> 
                                    </div>
                                </div>
                            </v-col>
                        </template>
                        <template v-else>
                            <v-col cols="12" md="6" class="justify-center mx-auto">
                                <v-card outlined light color="blue lighten-4" min-height="30">
                                    <v-card-title class="subtitle-2">
                                        <v-icon color="red ligten-2" left>warning</v-icon> There are no testimonials submitted yet.
                                    </v-card-title>
                                </v-card>
                            </v-col>
                        </template>
                    </template>
                </template>
                <template v-else>
                    <v-col cols="12" md="8">
                        <v-card outlined light min-height="450" class="mx-auto">
                            <v-card-title class="headline justify-center font-weight-light">New Testimonial</v-card-title>
                            <v-card-text>
                                <v-row wrap>
                                    <v-col cols="12" md="6" v-if="!isLoggedIn">
                                        <v-text-field label="First Name" v-model="newTest.f_name" required v-validate="'required|min:2|max:30'" :error-messages="errors.collect('f_name')" name="f_name" data-vv-as="first name"></v-text-field>
                                    </v-col>
                                    <v-col cols="12" md="6" v-if="!isLoggedIn">
                                        <v-text-field label="Last Name" v-model="newTest.l_name" required v-validate="'required|min:2|max:30'" :error-messages="errors.collect('l_name')" name="l_name" data-vv-as="last name"></v-text-field>
                                    </v-col>
                                    <v-col cols="12" md="6" v-if="!isLoggedIn">
                                        <v-text-field label="Email" v-model="newTest.email" required v-validate="'required|email'" :error-messages="errors.collect('email')" name="email"></v-text-field>
                                    </v-col>
                                    <v-col cols="12" md="6" v-if="!isLoggedIn">
                                        <v-text-field label="Position" v-model="newTest.position" v-validate="'min:3|max:30'" :error-messages="errors.collect('position')" name="position"></v-text-field>
                                    </v-col>
                                </v-row>
                                <v-text-field v-if="!isLoggedIn" label="Company" v-model="newTest.company" required v-validate="'required|min:2|max:150'" :error-messages="errors.collect('company')" name="company"></v-text-field>
                                <v-textarea v-if="!isLoggedIn" label="Address" rows="1" auto-grow v-model="newTest.address" v-validate="'min:10|max:150'" :error-messages="errors.collect('address')" name="address"></v-textarea>
                                <v-textarea label="Testimonial" rows="1" auto-grow v-model="newTest.text" required v-validate="'required|min:10|max:300'" counter="300" :error-messages="errors.collect('text')" name="text"></v-textarea>
                            </v-card-text>
                            <v-card-text class="ml-3">
                                <template v-if="!previewImg">
                                    <v-btn outlined color="secondary" class="mb-5 mr-5" @click="openUpload">Upload Picture</v-btn>
                                    <input type="file" ref="image" style="display:none" @change.prevent="pickImg" accept="image/*"> 
                                </template>
                                <v-card v-else flat class="justify-start ml-n5" max-width="250">
                                    <v-card-title class="subtitle-1 font-weight-bold justify-center">Preview</v-card-title>
                                    <v-img :src="previewImgUrl" height="100" contain alt="Testimonial picture" class="ml-n5"></v-img>
                                    <v-card-actions class="mb-3 justify-center">
                                        <v-btn text color="accent" @click="removeImg">Cancel</v-btn>
                                    </v-card-actions>
                                </v-card>
                            </v-card-text>
                            <v-card-actions class="justify-center my-5 pb-5">
                                <v-btn color="accent" dark text @click="testForm = false">Cancel</v-btn>
                                <v-btn color="primary" dark @click="submitTest" width="30%" :loading="loading">Submit</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-col>
                </template>
                <v-dialog v-model="confirmDel" max-width="450">
                    <v-card>
                        <v-card-title class="title justify-center mb-4">Delete Testimonial?</v-card-title>
                        <v-card-text class="subtitle-1">Do you really want to delete this testimonial? </v-card-text>
                        <v-card-actions class="pb-4 pl-3">
                            <v-spacer></v-spacer>
                            <v-btn text color="accent" @click="confirmDel = false" width="20%">Cancel</v-btn>
                            <v-btn color="primary white--text" :loading="loading" width="30%" @click="deleteTest">Yes, Delete!</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
                <v-snackbar v-model="submitted" :time="8000" top color="green darken-1 white--text">Your testimonial has been sent. Please note that your testimonial will only be listed after approval by our admin. Thank you. 
                    <v-btn text color="white--text" @click="submitted = false">Close</v-btn>
                </v-snackbar>
                <v-snackbar v-model="submitErr" :time="6000" top color="red darken-1 white--text">{{ submitErrMsg }} 
                    <v-btn text color="white--text" @click="submitErr = false">Close</v-btn>
                </v-snackbar>
                <v-snackbar v-model="delSuccess" :time="6000" top color="green darken-1 white--text">The testimonial has been deleted. 
                    <v-btn text color="white--text" @click="delSuccess = false">Close</v-btn>
                </v-snackbar>
                <v-snackbar v-model="deleteFail" :time="6000" top color="red darken-1 white--text">There is a problem trying to delete the testimonial. Please try again. 
                    <v-btn text color="white--text" @click="deleteFail = false">Close</v-btn>
                </v-snackbar>
            </v-row>
        </v-container>
    </div>
</template>

<script>
export default {
    data(){
        return{
            api: 'http://localhost:8000/api/',
            testimonials: [],
            loading: false,
            testForm: false,
            newTest: {
                f_name: '',
                l_name: '',
                email: '',
                position: '',
                company: '',
                address: '',
                text: '',
                image: null
            },
            previewImg: false,
            previewImgUrl: null,
            submitted: false,
            submitErr: false,
            submitErrMsg: '',
            confirmDel: false,
            testToDel: null,
            testIndexToDel: null,
            delSuccess: false,
            deleteFail: false
        }
    },
    computed: {
        authToken() {
            return this.$store.getters.getToken;
        },
        authUser() {
            return this.$store.getters.getAuthUser;
        },
        isLoggedIn(){
          return this.$store.getters.isLoggedIn
        },
        authService(){
            return this.$store.getters.getServFromStore
        },
        header() {
            let conf = {
                headers: {
                    Authorization: "Token " + this.authToken,
                },
            };
            return conf;
        },
        contentHeader(){
            let conf = {
                headers: {
                    "content-type": "multipart/form-data"
                }
            }
            return conf;
        }
    },
    methods: {
        getTestimonials(){
            this.loading = true
            this.$axios.get(this.api + 'testimonials/').then((res) => {
                this.loading = false
                this.testimonials = res.data
            })
        },
        openUpload(){
            this.$refs.image.click()
        },
        pickImg(e){
            const file = e.target.files[0]
            this.newTest.image = file
            this.previewImg = true
            this.previewImgUrl = URL.createObjectURL(file)
        },
        submitTest(){
            this.$validator.validateAll().then((isValid) => {
                if (isValid) {
                    let form = new FormData();
                    form.append('name', this.authToken ? this.authUser.fullname : this.newTest.f_name + ' ' + this.newTest.l_name)
                    form.append('email', this.authToken ? this.authUser.email : this.newTest.email)
                    form.append('position', this.authToken ? 'Owner' : this.newTest.position)
                    form.append('company', this.authToken ? this.authService.title : this.newTest.company)
                    form.append('address', this.authToken ? this.authService.street_address + ',' + this.authService.city : this.newTest.address)
                    form.append('user', this.authToken ? this.authUser.id : '')
                    form.append('text', this.newTest.text)
                    form.append('image', this.newTest.image)
                    this.loading = true;
                    this.$axios.post(this.api + 'send-testimonial/', form, this.contentHeader).then(() =>{
                       this.loading = false
                       this.testForm = false
                       this.submitted = true
                    }).catch(() => {
                        this.loading = false
                        this.submitErr = true
                        this.submitErrMsg = 'Your testimonial was not sent. Please ensure you complete all fields and try again.'
                    })
                }
            })
        },
        removeImg(){
            this.previewImg = false
            this.previewImgUrl = null
            this.newTest.image = null
        },
        confirmDelDial(test, index){
            this.testToDel = parseInt(test)
            this.testIndexToDel = index
            this.confirmDel = true
        },
        deleteTest(){
            this.isLoading = true
            this.$axios.delete(this.api + `testimonial_delete/${this.testToDel}/`, this.header).then(() => {
                this.isLoading = false
                this.confirmDel = false
                this.testimonials.splice(this.testIndexToDel, 1)
                this.delSuccess = true
            }).catch(() =>{
                this.isLoading = false
                this.deleteFail = true
            })
        }
    },
    mounted(){
        this.getTestimonials()
    }
}
</script>

<style lang="scss" scoped>
    .testimonial{
        background: rgba(238, 238, 238, .39);
        .banner{
            height: 18rem;
            width: 100%;
            background-image: linear-gradient(to bottom right, rgba(0, 59, 99, 0.89), rgba(255, 23, 69, 0.623)), url('../statics/images/testimonial.jpg');
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
        }
        .testimonial_card{
            margin-top: 20px;
            height: 250px;
            border: 1px solid rgb(255, 255, 255);
            width: 100%;
            border-radius: 4px;
            box-shadow: 0px 5px 5px -3px rgba(0, 0, 0, 0.2), 0px 8px 10px 1px rgba(0, 0, 0, 0.14), 0px 3px 14px 2px rgba(0, 0, 0, 0.12) !important;
            margin-bottom: 15px;
            outline: none;
            transition-property: box-shadow, opacity;
            overflow: hidden;
            // overflow-wrap: break-word;
            display: block;
            position: relative;
            white-space: normal;
            transition: box-shadow 280ms cubic-bezier(0.4, 0, 0.2, 1);
            will-change: box-shadow;
            background-color: #fff;
            color: rgba(0, 0, 0, 0.87);
            cursor: pointer;

            display: flex;
            justify-content: space-between;

            .v-img{
                height: 220px;
                // width: 50% !important;
            }
            .texts{
                margin: 1.5rem 1rem;
                // padding: 1.5rem .85rem;
                align-self: center;
            }
        }
    }
    
</style>
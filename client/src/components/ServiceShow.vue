<template>
  <v-container>
    <v-row justify="center" class="mt-4">
      <v-col cols="12">
        <v-btn rounded color="accent" dark elevation="3" left @click.prevent="$router.go(-1)"><v-icon left>arrow_left</v-icon> Back</v-btn>
      </v-col>
      <v-col cols="12">
        <h2 v-if="service" class="headline text-center">{{ service.title | capFirstLetter }} </h2>
      </v-col>
    </v-row>
    <v-row class="service_single">
      <v-col cols="12" md="8">
        <v-card class="mb-4" light outlined min-height="450">
          <template v-if="isLoading">
            <v-progress-circular indeterminate color="accent" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
          </template>
          <template v-else>
            <template v-if="service">
              <v-img :src="service.image" aspect-ration="1" height="380" transition="scale-transition"></v-img>
              <v-card-subtitle class="body-1 black--text lighten-5 text-center mt-3"
              >Published on {{ service.created }} | {{ service.subcategory && service.subcategory.name }}, {{ service.subcategory && service.subcategory.category.name }}</v-card-subtitle>
              <v-divider></v-divider>
              <v-card-actions class="align-center justify-space-around">
                <v-rating dense v-model="service.ratings" color="accent" class="mr-1" readonly></v-rating>
                <span class="ml-8">
                  <v-icon dense color="primary">visibility</v-icon>
                  {{ service.view_count }}
                </span>
                <v-chip v-if="service.is_verified" class="ma-2" color="green darken-3" text-color="white">
                  <v-avatar left><v-icon>mdi-checkbox-marked-circle</v-icon></v-avatar>
                  Verified
                </v-chip>
              </v-card-actions>
              <v-divider></v-divider>
              <v-card-text class="subtitle-1 black--text lighten-3 mt-3 ml-2 mr-2 mb-2">{{ service.description }}</v-card-text>
            </template>
            <template v-else>No service selected</template>
          </template>
        </v-card>

        <!-- <v-card class="mb-7" light outlined rounded elevation="8" min-height="400" :loading="mapLoading">
            <v-card-title class="justify-center mt-3">Location on map</v-card-title>
            <v-card-text>{{ center }}</v-card-text> 
        </v-card> -->
        <!-- <map-location :location="service"></map-location> -->

        <v-card class="mb-7" light outlined min-height="100" :loading="isLoading">
          <template v-if="service">
            <v-card-title class="title justify-center primary white--text" color="primary"
            >Reviews ({{ service.reviews && service.reviews.length }})</v-card-title>
            <div class="pa-5" v-if="isLoggedIn && service.owner.id != getAuth.id">
                <v-spacer></v-spacer>
                <v-btn rounded elevation="3" class="primary white--text" @click="openReviewDialog = true">Add Review</v-btn>
            </div>
            <div class="pa-5" v-if="!isLoggedIn">
                <router-link to="/login">Login to submit review</router-link>
            </div>
            <template v-if="service.reviews && service.reviews.length > 0">
              <v-divider></v-divider>
                <template v-if="!showAllReview">
                  <v-card-text class="pa-1"> 
                    <div v-for="(review, i) in service.reviews.slice(0, 3)" :key="i" class="py-3 px-3">
                      <p class="body-1 primary--text">{{ review.author && review.author.fullname }} on {{ review.created }}</p>
                      <v-rating small dense color="accent" readonly v-model="review.rating" class="mt-n3" half-increments></v-rating>
                      <p class="body-1 font-weight-bold mt-4">{{ review.title | capFirstLetter }}</p>
                      <p class="body-1 black--text lighten-5 mt-n2">{{ review.body | capFirstLetter }}</p>
                      <div v-if="isLoggedIn">
                        <div v-if="review.author.id == getAuth.id" class="py-2 mt-n2">
                          <v-btn text color="primary" small @click="editReviewDial(review)">
                            <v-icon small left>edit</v-icon>
                          </v-btn>
                          <v-btn text color="accent" small @click="deleteReviewDial(review.id, i)">
                            <v-icon small left>delete_outline</v-icon>
                          </v-btn>
                        </div>
                      </div>
                      <v-divider v-if="i < 2"></v-divider>
                    </div>
                  </v-card-text>
                  <v-divider></v-divider>
                  <v-card-actions class="justify-center">
                    <v-btn text color="primary" @click="showAllReview = true">All Reviews</v-btn>
                  </v-card-actions>
              </template>
              <template v-else>
                <v-card-text class="pa-3">
                  <div v-for="(review, i) in service.reviews" :key="i" class="py-4 px-3">
                      <p class="body-1 primary--text">{{ review.author && review.author.username }} at {{ review.created }}</p>
                      <v-rating small dense color="accent" readonly v-model="review.rating" class="mt-n3" half-increments></v-rating>
                      <p class="body-1 font-weight-bold mt-4">{{ review.title | capFirstLetter }}</p>
                      <p class="body-1 black--text lighten-5 mt-n2">{{ review.body | capFirstLetter }}</p>
                      <div v-if="isLoggedIn">
                        <div v-if="review.author.id == getAuth.id" class="py-2 mt-n2">
                          <v-btn text color="primary" small @click="editReviewDial(review)">
                            <v-icon small left>edit</v-icon>
                          </v-btn>
                          <v-btn text color="accent" small @click="deleteReviewDial(review.id, i)">
                            <v-icon small left>delete_outline</v-icon>
                          </v-btn>
                        </div>
                      </div>
                      <v-divider v-if="i < service.reviews.length - 1"></v-divider>
                    </div>
                  </v-card-text>
                  <v-divider></v-divider>
                  <v-card-actions class="justify-center">
                    <v-btn text color="primary" @click="showAllReview = false">Less Reviews</v-btn>
                  </v-card-actions>
              </template>
            </template>
            <template v-else>
              <v-card-text class="body-1 py-4">There are no reviews yet for this service.</v-card-text>
            </template>
          </template>
          <template v-else>
            <v-card-text class="body-1">No service selected</v-card-text>
          </template>
        </v-card>
        <v-card class="mb-7" light outlined min-height="100" :loading="fetchingPf">
          <template v-if="service">
            <template v-if="service.portfolio.length > 0">
              <v-card-title class="title justify-center primary white--text">Portfolio({{ service.portfolio.length }})</v-card-title>
              <v-card-text>
                <v-list three-line nav>
                  <template v-for="(item, i) in service.portfolio">
                    <v-list-item :to="{name: 'PortFolioShow', params: {id: item.id, slug:item.slug}}" :key="item.title" class="mt-3" link>
                      <v-list-item-avatar>
                        <v-img :src="item.image" height="250" alt="Portfolio Image"></v-img>
                      </v-list-item-avatar>
                      <v-list-item-content class='mt-n3'>
                          <v-list-item-title class="subtitle-1 primary--text">{{ item.title | capFirstLetter }}</v-list-item-title>
                          <v-list-item-subtitle class="mt-n3 subtitle-2">{{ item.description | capFirstLetter | truncate(160) }}</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                    <v-divider v-if="i != service.portfolio.length - 1" :key="i"></v-divider>
                  </template>   
                </v-list>
              </v-card-text>
            </template>
            <template v-else>
              <v-card-title class="title justify-center primary white--text">Portfolio</v-card-title>
              <v-card-text class="pa-4 body-1"> No Portfolio has been published for this service.</v-card-text>
            </template>
          </template>
          <template v-else>
            <v-card-title class="title justify-center primary white--text">
              This service does not exist.
            </v-card-title>
          </template>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card class="mx-auto" light :loading="fetchingPf">
            <v-card-title class="justify-center primary white--text">Details</v-card-title>
            <template v-if="service">
              <v-list rounded>
                <v-list-item-group color="primary">
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon color="accent">people_alt</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ service && service.owner.fullname }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon color="accent">location_city</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ service.street_address }},</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon color="accent">place</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ service.city }}, {{ service && service.state.state }} State</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon color="accent">mdi-phone</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ service.phone_number }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon color="accent">mdi-email</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ service && service.owner.email }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon color="accent">view_list</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ service && service.subcategory.name }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon color="accent">view_quilt</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ service && service.subcategory.category.name }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item v-if="service.website" :href="service.website" target="_blank" link>
                    <v-list-item-icon>
                      <v-icon color="accent">place</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ service.website }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item v-if="service.fb" :href="`https://www.facebook.com/${service.fb}`" target="_blank" link>
                    <v-list-item-icon>
                      <v-icon color="accent">mdi-facebook</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>https://facebook.com/{{ service.fb }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item v-if="service.instag" :href="`https://www.instagram.com/${service.instag}`" target="_blank" link>
                    <v-list-item-icon>
                      <v-icon color="accent">mdi-instagram</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ service.instag }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </template>
            <template v-else>
              <v-card-text>This service does not exist.</v-card-text>
            </template>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-dialog v-model="openReviewDialog" max-width="550">
          <v-card>
              <v-card-title class="title justify-center mb-4">Add a review for this Service</v-card-title>
              <v-card-text>
                  <v-text-field label="Review Title" v-model="review.title" required :counter="80" v-validate="'required|min:3|max:80'" :error-messages="errors.collect('review.title')" name="title" data-vv-scope="review"></v-text-field>
                  <v-textarea rows="1" auto-grow label="Review" v-model="review.body" required :counter="400" v-validate="'required|min:5|max:400'" :error-messages="errors.collect('review.body')" name="body" data-vv-scope="review"></v-textarea>
                  <p class="light-grey mt-2">Rate Us</p>
                  <v-rating half-increments dense color="primary lighten-1" v-model="review.rating" ripple background-color="primary" required v-validate="'required'" :error-messages="errors.collect('review.rating')" name="rating" data-vv-scope="review"></v-rating>
              </v-card-text>
              <v-card-actions class="pb-4 pl-3 justify-center">
                  <v-spacer></v-spacer>
                  <v-btn text color="accent" @click="cancelReview" width="20%">Cancel</v-btn>
                  <v-btn color="primary white--text" :loading="isSaving" width="30%" @click="sendReview">Submit</v-btn>
              </v-card-actions>
          </v-card>
      </v-dialog>
      <v-dialog v-model="reviewEditDial" max-width="550">
          <v-card>
              <v-card-title class="title justify-center mb-4">Edit Review</v-card-title>
              <v-card-text>
                  <v-text-field label="Review Title" v-model="editReview.title" required :counter="80" v-validate="'required|min:3|max:80'" :error-messages="errors.collect('editReview.title')" name="title" data-vv-scope="editReview"></v-text-field>
                  <v-textarea rows="1" auto-grow label="Review" v-model="editReview.body" required :counter="400" v-validate="'required|min:5|max:400'" :error-messages="errors.collect('editReview.body')" name="body" data-vv-scope="editReview"></v-textarea>
                  <p class="light-grey mt-2">Rate Us</p>
                  <v-rating half-increments dense color="primary lighten-1" v-model="editReview.rating" ripple background-color="primary" required v-validate="'required'" :error-messages="errors.collect('editReview.rating')" name="rating" data-vv-scope="editReview"></v-rating>
              </v-card-text>
              <v-card-actions class="pb-4 pl-3 justify-center">
                  <v-spacer></v-spacer>
                  <v-btn text color="accent" @click="cancelEditReview" width="20%">Cancel</v-btn>
                  <v-btn color="primary white--text" :loading="isSaving" width="30%" @click="updateReview">Update Review</v-btn>
              </v-card-actions>
          </v-card>
      </v-dialog>
      <v-dialog v-model="reviewDelDial" max-width="450">
          <v-card>
              <v-card-title class="title justify-center mb-4">Delete Review?</v-card-title>
              <v-card-text class="subtitle-1">Do you really want to delete this review? </v-card-text>
              <v-card-actions class="pb-4 pl-3">
                  <v-spacer></v-spacer>
                  <v-btn text color="accent" @click="reviewDelDial = false" width="20%">Cancel</v-btn>
                  <v-btn color="primary white--text" :loading="isSaving" width="30%" @click="deleteReview">Yes, Delete!</v-btn>
              </v-card-actions>
          </v-card>
      </v-dialog>
      <v-snackbar v-model="reviewError" :timeout="6000" top color="red darken-1 white--text">
          Review was not sent. Kindly ensure you filled the fields and rate the service before submitting.
          <v-btn text color="white--text" @click="reviewError = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="reviewUpdated" :timeout="6000" top color="green darken-1 white--text">
          Review was updated successfully.
          <v-btn text color="white--text" @click="reviewUpdated = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="reviewUpdateFailed" :timeout="6000" top color="red darken-1 white--text">
          Review was not updated. Kindly ensure you fill all fields and rate service before submitting.
          <v-btn text color="white--text" @click="reviewUpdateFailed = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="reviewSentSuccess" :timeout="6000" top color="green darken-1 white--text">
          Review has been sent.
          <v-btn text color="white--text" @click="reviewSentSuccess = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="reviewSentFail" :timeout="6000" top color="red darken-1 white--text">
          Review was not sent. Kindly ensure you fill all fields and rate service before submitting.
          <v-btn text color="white--text" @click="reviewSentFail = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="reviewDelSuccess" :timeout="6000" top color="green darken-1 white--text">
          Your review has been deleted..
          <v-btn text color="white--text" @click="reviewDelSuccess = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="reviewDelFail" :timeout="6000" top color="red darken-1 white--text">
          Your review was not deleted.
          <v-btn text color="white--text" @click="reviewDelFail = false">Close</v-btn>
      </v-snackbar>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      id: this.$route.params.id,
      slug: this.$route.params.slug,
      isLoading: false,
      service: null,
      fetchingPf: false,
      mapLoading: false,
      center: {},
      openReviewDialog: false,
      isSaving: false,
      review: {
        title: '',
        body: '',
        rating: 0
      },
      api: "http://localhost:8000/api/",
      reviewError: false,
      showAllReview: false,
      reviewEditDial: false,
      reviewToEdit : null,
      editReview: {
        id: null,
        title: '',
        body: '',
        rating: ''
      },
      reviewUpdated: false,
      reviewUpdateFailed: false,
      reviewSentSuccess: false,
      reviewSentFail: false,
      reviewToDel: null,
      reviewIndexToDel: null,
      reviewDelDial: false,
      reviewDelSuccess: false,
      reviewDelFail: false
    };
  },
  computed: {
      getAuth(){
          return this.$store.getters.getAuthUser
      },
      isLoggedIn(){
          return this.$store.getters.isLoggedIn
      },
      authToken(){
          return this.$store.getters.getToken
      },
      config() {
        let conf = {
            headers: {
                Authorization: "Token " + this.authToken,
            },
        };
        return conf;
      }
  },
  methods: {
    getService() {
      this.isLoading = true;
      this.$axios.get(`http://localhost:8000/api/services/${this.id}/`)
        .then(res => {
          this.isLoading = false;
          this.service = res.data;
        });
     },
     getLocation(){
       navigator.geolocation.getCurrentPosition(position =>{
          this.center = {
            lat: position.coords.latitude,
            long: position.coords.longitude
          }, () =>{
            // console.log(error + " - Error getting location")
          }
       })
     },
     cancelReview(){
       this.openReviewDialog =  false
       this.review.title = ''
       this.review.body = ''
       this.review.rating = 0
       this.$validator.reset()
     },
     sendReview(){
       this.$validator.validateAll('review').then((isValid) => {
          if (isValid && this.review.rating > 0) {
              this.isSaving = true;
              this.$axios.post(this.api + `review/new/${this.$route.params.id}/`, {
                title: this.review.title,
                body: this.review.body,
                rating: this.review.rating,
              }, this.config).then((res) => {
                this.isSaving = false
                this.cancelReview()
                this.reviewSentSuccess = true
                this.service.reviews.unshift(res.data)
              }).catch(() =>{
                this.isSaving = false
                this.reviewSentFail = true
              })
          }else{
            this.reviewError = true
          }
       })
     },
     editReviewDial(review){
       this.reviewEditDial = true
       this.editReview.id = review.id
       this.editReview.title = review.title
       this.editReview.body = review.body
       this.editReview.rating = review.rating
     },
     updateReview(){
        this.$validator.validateAll('editReview').then((isValid) => {
          if (isValid) {
            this.isSaving = true
            this.$axios.patch(this.api + `review/update/${this.editReview.id}/`, {
                title: this.editReview.title,
                body: this.editReview.body,
                rating: this.editReview.rating,
            }, this.config).then(() => {
              this.isSaving = false
              this.reviewUpdated = true
              this.reviewEditDial = false
              this.getService()
            }).catch(() =>{
              this.isSaving = false
              this.reviewUpdateFailed = true
            })
          }
        })
     },
     cancelEditReview(){
       this.reviewEditDial = false
     },
     deleteReviewDial(review, i){
       this.reviewToDel = review
       this.reviewIndexToDel = i
       this.reviewDelDial = true
     },
     deleteReview(){
       this.isLoading = true
       this.$axios.delete(this.api + `reviews/${this.reviewToDel}/`, this.config).then(() =>{
         this.isLoading = false
         this.reviewDelSuccess = true
         this.service.reviews.splice(this.reviewIndexToDel, 1)
         this.reviewDelDial = false
       }).catch(() => {
         this.reviewDelFail = true
       })
     }
  },
  mounted() {
    this.getService();
    this.getLocation()
  }
};
</script>

<style lang="scss" scoped>
.service_single {
  .v-card {
    .review {
      height: 50px;
      display: flex !important;
      justify-content: space-around !important;
      align-items: center !important;
      flex-wrap: wrap;

      .rating {
        flex: 0 1 60%;
      }
      .view {
        flex: 0 1 40%;
      }
    }
  }
}
</style>
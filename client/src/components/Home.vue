<template>
  <div class="home">
    <div class="banner">
      <div class="banner_caption text-center">
        <h1 class="display-3 font-weight-thin white--text mb-3">Welcome to Ejika...</h1>
        <h3 class="display-1 font-weight-thin white--text mt-5 pb-4">Connecting you to your neighbourhood service providers.</h3>
        <div class="mx-auto">
            <v-container fluid>
                  <v-row justify="center" no-gutters class="mt-8">
                    <v-col class="d-flex" cols="12" sm="5">
                      <v-select outlined height="50" :items="states" item-text="state" item-value="slug" v-model="location" dark color="white" label="choose State"></v-select>
                    </v-col>
                    <v-col class="d-flex" cols="8" sm="5">
                      <v-select autofocus outlined height="50" :items="categories" item-text="name" item-value="slug" v-model="category" dark color="white" label="Category"></v-select>
                    </v-col>
                    <v-col class="d-flex" cols="4" sm="2">
                      <v-btn dark color="accent" x-large width="100%" height="55" @click="search">GO</v-btn>
                    </v-col>
                  </v-row>  
              </v-container>
            </div>
      </div>
    </div>
    <!-- <v-btn fixed dark elevation="12" fab bottom right color="accent" class="mt-5 mr-4" href="/my_cart"><v-icon>shopping_cart</v-icon></v-btn> -->
    <div class="introd my-5 pa-5">
      <v-container>
        <v-row>
          <v-col cols="12">
            <h2 class="display-1 font-weight-light mt-2 pb-3 text-center">How to use the app?</h2>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col cols="12" md="5">
            <v-card hovered tile raised outlined ripple min-height="450" light>
              <v-card-title class="justify-center my-2">
                <svg class="svg_icon_prof">
                  <use xlink:href="../statics/svgicons/sprite2.svg#icon-tools-2" />
                </svg>
              </v-card-title>
              <v-card-text class="text-center">
                <p class="headline pa-3 primary--text">Become a professional.</p>
                <p class="title pt-2">Put your services in the consciousness of your world. Get reviewed by clients.</p>
                <p class="title pt-2">Upload your portfolio and earn our verification...join free!</p>
              </v-card-text>
              <v-card-actions class="justify-center mb-4">
                <v-btn color="primary white--text" large to="/register">Register Now</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col cols="12" md="5">
            <v-card hover tile raised outlined ripple min-height="450" light>
              <v-card-title class="justify-center my-2">
                <svg class="svg_icon">
                  <use xlink:href="../statics/svgicons/sprite.svg#icon-search" />
                </svg>
              </v-card-title>
              <v-card-text class="text-center">
                <p class="headline pa-3 primary--text">Search for a service provider.</p>
                <p class="title pt-2">Select your location, pick a category and search for a service provider close to you. </p>
                <p class="title pt-2">Browse their profile and reviews, then contact service provider...all in easy steps! </p>
              </v-card-text>
              <v-card-actions class="justify-center mb-4 mt-n1">
                <v-btn color="primary white--text" large @click="goToSearch">Search Now</v-btn>
                <a ref="search" href="#search_prof" style="display:none">Search</a>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
    <div class="search_div my-5 pa-5">
        <v-container>
            <v-row justify="center">
                <v-col cols="12" md="7">
                    <h2 class="headline font-weight-light white--text text-center mb-8 py-2">
                        Looking for a service professional, technician or artisan within your neighbourhood?
                    </h2>
                    <v-card light flat tile elevation="4" min-height="400" class="mt-5 pa-5" id="search_prof">
                        <v-card-title class="justify-center title mt-7 mb-4">Choose your location & category</v-card-title>
                        <v-card-actions class="justify-center mt-6 mb-5">
                            <v-select dense outlined :items="states" item-text="state" item-value="slug" label="Select State" v-model="location" persistent-hint></v-select>
                            <v-spacer></v-spacer>
                            <v-select class="ml-2" dense outlined :items="categories" item-text="name" item-value="slug" label="Select Category" v-model="category" persistent-hint></v-select>
                        </v-card-actions>
                        <v-card-actions class="justify-center mt-4">
                            <v-btn color="accent white--text" large @click="search" width="50%">Search</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
    <featured :services="featured"></featured>
    <locations></locations>
    <popular :services="popular"></popular>
    <new-services :services="newServices"></new-services>
    <home-how-to></home-how-to>
    <testimonials></testimonials>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      services: [],
      states: [],
      categories: [],
      location: null,
      category: null,
      newServices: [],
      featured: [],
      popular: [],
    };
  },
  methods: {
      search(){
          if(this.location != null && this.category != null){
              this.$router.push({name: 'ServicesByLoc', params: {state: this.location, categ: this.category }})
          }
      },
      goToSearch(){
        this.$refs.search.click()
      }
  },
  mounted() {
    this.$axios.get("http://localhost:8000/api/users").then(res => {
      this.users = res.data;
    });

    this.$axios.get("http://localhost:8000/api/services").then(res => {
      this.services = res.data;
      this.newServices = res.data.slice(0, 3)
      let featured = res.data.filter(a => a.is_featured == true)
      this.featured = featured

      let popular = res.data.sort((a, b) => parseFloat(b.ratings) - parseFloat(a.ratings))
      this.popular = popular.slice(0, 3)
      
    });

    this.$axios.get("http://localhost:8000/api/states").then(res => {
      this.states = res.data;
    });
    this.$axios.get("http://localhost:8000/api/categories").then(res => {
      this.categories = res.data;
    });
  }
};
</script>

<style lang="scss" scoped>
  .introd{
    .svg_icon{
      height: 3.25rem;
      fill: #ff1744;
    }
    .svg_icon_prof{
      height: 3.25rem;
      fill: #ff1744;
    }
  }
    .search_div{
        height: 100vh;
        width: 100%;
        background: linear-gradient(to bottom right, rgba(0, 63, 107, 0.95), rgba(1, 47, 74, 0.7), rgba(5, 8, 7, 0.98));
        clip-path: polygon(0 0, 100% 0, 100% 82%, 0 100%);
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;

        h2{
            line-height: 1.6;
        }
        .v-btn{
            width: 30%;
        }
    }
    
</style>
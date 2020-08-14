<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" class="mb-8">
        <v-row justify-center>
          <v-col cols="9" md="4" offset-md="5" class="d-flex justify-center">
            <v-select dense outlined :items="categories" item-text="name" item-value="slug" label="Select Category" v-model="query.category" persistent-hint></v-select>
          </v-col>
          <v-col colc="3" md="3">
            <v-btn dark color="primary" @click="filter">Filter</v-btn>
          </v-col>
        </v-row>
        <v-row justify="center" class="mt-2">
          <h2 class="headline text-center">Services for {{ servState && servState.state }} state</h2>
        </v-row>
        <v-row class="mt-4 mb-16">
          <v-progress-circular indeterminate color="accent" :width="7" :size="70" v-if="isLoading" justify="center" class="mx-auto"></v-progress-circular>
          <template v-else>
            <template v-if="services.length > 0">
              <v-col cols="12" md="4" v-for="service in services" :key="service.id" class="mb-6">
                  <v-card light outlined min-height="400" :loading="isLoading" class="mx-auto" :to="{name: 'ServiceShow', params:{id: service.id, slug: service.slug}}">
                      <v-img :src="service.image" height="300" transition="scale-transition" aspect-ratio="1"></v-img>
                      <v-card-title class="title justify-center mb-2">{{ service.title }}</v-card-title>
                      <v-card-subtitle class="text-center mb-1">
                          <v-chip v-if="service.is_verified" class="pa-2" color="green darken-3" text-color="white">
                              <v-avatar left><v-icon>mdi-checkbox-marked-circle</v-icon></v-avatar>
                              Verified
                          </v-chip>
                          <v-chip class="pa-2 ml-2" color="primary" text-color="white">
                              <v-avatar left><v-icon>view_quilt</v-icon></v-avatar>
                              {{ service.subcategory && service.subcategory.category.name }}
                          </v-chip>
                      </v-card-subtitle>
                      <v-card-text class="body-1 mt-1">{{ service.description | truncate(140) }}</v-card-text>
                      <v-card-actions class="mt-n2 mb-5 justify-center">
                          <v-rating dense v-model="service.ratings" color="accent" readonly></v-rating>
                      </v-card-actions>
                  </v-card>
              </v-col>
            </template>
            <template v-else>
              <v-col cols="12" md="6" class="mx-auto">
                  <v-card outlined light color="blue lighten-4" min-height="30">
                      <v-card-title class="subtitle-2">
                          <v-icon color="red ligten-2" left>warning</v-icon> Your search returned no services.
                          <v-spacer></v-spacer>
                          <v-btn text color="primary" @click="clearFilter">Clear Filter</v-btn>
                      </v-card-title>
                  </v-card>
              </v-col>
            </template>
          </template>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      state: this.$route.params.state,
      category: this.$route.params.categ,
      services: [],
      api: 'http://localhost:8000/api/',
      isLoading: true,
      servState: null,
      servCateg: null,
      categories: [],
      query: {
        category: '',
      }
    };
  },
  methods: {
    getServices() {
      this.$axios.get(this.api + `get_services_by_loc_cat/${this.$route.params.state}/${this.$route.params.categ}/`)
        .then((res) => {
          this.isLoading = false;
          this.services = res.data;
        });
    },
    getState() {
      this.$axios.get(this.api + `get_state/${this.state}/`)
        .then(res => {
          this.servState = res.data;
        });
    },
    getCateg() {
      this.$axios.get(this.api + `get_categ/${this.category}/`)
        .then(res => {
          this.servCateg = res.data;
        });
    },
    getAllCategs(){
        this.$axios.get(this.api + 'categories/').then(res => {
            this.categories = res.data;
        });
    },
    filter(){
      this.$axios.get(this.api + `get_services_by_loc_cat/${this.$route.params.state}/${this.query.category}/`)
        .then((res) => {
          this.services = res.data
        })
     },
    clearFilter(){
        this.query.category = ''
        this.getServices()
    }
  },
  mounted() {
    this.getServices();
    this.getState();
    this.getAllCategs()
  }
};
</script>

<template>
    <v-container>
        <v-row class="justify-center mt-6">
            <v-col cols="12" md="9">
                <h2 class="title text-center mb-2">Services in {{ servState && servState.state }}</h2>
            </v-col>
            <v-col cols="12" md="3" class="mx-auto">
                <!-- <v-select dense outlined :items="states" item-text="state" item-value="slug" label="Change State" v-model="query.state" persistent-hint></v-select> -->
            </v-col>
        </v-row>
        <v-row class="justify-start" wrap>
            <v-progress-circular indeterminate color="accent" :width="7" :size="70" v-if="isLoading" justify="center" class="mx-auto"></v-progress-circular>
            <template v-else>
                <v-col cols="12" md="10" class="mx-auto mt-n6">
                    <v-row wrap class="justify-center">
                        <v-col cols="5" md="3">
                            <v-select dense outlined :items="categories" item-text="name" item-value="slug" label="Select Category" v-model="query.category" @change="getsubCategories"></v-select>
                        </v-col>
                        <v-col cols="5" md="3">
                            <v-select dense outlined :items="subcategories" item-text="name" item-value="slug" label="Select SubCategory" v-model="query.subcategory" persistent-hint></v-select>
                        </v-col>
                        <v-col cols="2" md="2">
                            <v-btn dark color="primary" @click="filter" :loading="isFetching">Filter</v-btn>
                        </v-col>
                        <v-col cols="12" md="4">
                            <v-text-field outlined dense placeholder="Search for service.." v-model="q" solo prepend-inner-icon="search" @keyup.enter="search"></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row wrap class="justify-center" v-if="resultReturned">
                        <v-col cols="12" md="10">
                            <div class="title">Filtered <strong>{{ services.length | pluralize('service') }}</strong> </div>
                        </v-col>
                    </v-row>
                </v-col>
                <template v-if="services.length == 0">
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
                <template v-else>
                    <v-col cols="12" md="4" class="d-flex justify-space-around" v-for="service in services" :key="service.id">
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
            </template>
        </v-row>
        <v-row class="justify-center mt-2 pb-4" v-if="services.length != 0">
            <v-col cols="12">
                <div class="text-center">
                    <v-btn :disabled="!previous" color="primary white--text" class="mr-3" link @click="getPrevious"><v-icon left>arrow_left</v-icon>Previous</v-btn>
                    <v-btn :disabled="!next" color="primary white--text" link @click="getNext">Next<v-icon right>arrow_right</v-icon></v-btn>
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    data(){
        return{
            id: this.$route.params.id,
            slug: this.$route.params.slug,
            services: [],
            api: "http://localhost:8000/api/",
            isLoading: false,
            next: null,
            previous: null,
            page: 1,
            states: [],
            categories: [],
            subcategories: [],
            query: {
                state: '',
                category: '',
                subcategory: ''
            },
            q: '',
            servState: {},
            isFetching: false,
            resultReturned: false
        }
    },
    methods: {
        getServices(){
            this.isLoading = true
            this.$axios.get(this.api + `services_by_state/${this.id}/`).then((res) => {
                this.isLoading = false
                this.services = res.data.results
                this.count = res.data.count
                this.next = res.data.next
                this.previous = res.data.previous
            })
        },
        getNext(){
            const params = new URL(this.next).searchParams;
            this.$axios.get(this.next).then((res) => {
                this.services = res.data.results
                this.count = res.data.count
                this.next = res.data.next
                this.previous = res.data.previous
                let pageNum = params.get('page')
                this.$router.push({path: '/services', query:{page: pageNum}})
            })
        },
        getPrevious(){
            const params = new URL(this.previous).searchParams;
            this.$axios.get(this.previous).then((res) => {
                this.services = res.data.results
                this.count = res.data.count
                this.next = res.data.next
                this.previous = res.data.previous
                let pageNum = params.get('page')
                if(pageNum == null){
                    this.$router.push({path: '/services'})
                }else{
                    this.$router.push({path: '/services', query:{page: pageNum}})
                }
            })
        },
        getState(){
            this.$axios.get(this.api + `get_state/${this.slug}/`)
            .then(res => {
              this.servState = res.data;
            });
        },
        getStates(){
            this.$axios.get(this.api + 'states/').then(res => {
                this.states = res.data;
            });
        },
        getCategories(){
            this.$axios.get(this.api + 'categories/').then(res => {
                this.categories = res.data;
            });
        },
        getsubCategories(){
            this.$axios.get(this.api + `get_subcategories/${this.query.category}/`).then((res) => {
                this.subcategories = res.data
            })
        },
        filter(){
            if(this.query.category !== null){
                if(this.query.subcategory !== ''){
                    this.isFetching = true
                    this.$axios.get(this.api + `services_by_subcategories?state__slug=${this.slug}&subcategory__slug=${this.query.subcategory}`).then((res) => {
                        this.isFetching = false
                        this.services = res.data.results
                        this.resultReturned = true
                    }).catch(() => {
                        this.isFetching = false
                    })
                }else{
                    this.isFetching = true
                    this.$axios.get(this.api + `all_services?state__slug=${this.slug}&subcategory__category__slug=${this.query.category}`).then(() => {
                        this.isFetching = false
                    })
                }
            }
        },
        search(){
            if(this.q.trim() !== ''){
                this.$axios.get(this.api + `services_by_state/${this.id}?search=${this.q}`).then((res) => {
                    this.services = res.data.results
                })
            }
        },
        clearFilter(){
            this.q = ''
            this.query.state = ''
            this.query.category = ''
            this.getServices()
        }
    },
    created(){
        this.getServices()
        this.getState()
        this.getStates()
        this.getCategories()
    }
}
</script>
<template>
    <v-container>
        <v-row class="justify-center mt-6">
            <v-col cols="12" md="3" v-for="service in services" :key="service.id">
                <v-card outlined elevation="12" shaped min-height="400">
                    {{ service }}
                </v-card>
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
        }
    },
    methods: {
        getServices(){
            this.isLoading = true
            this.$axios.get(this.api + `services_by_state/${this.id}/`).then((res) => {
                this.isLoading = false
                this.services = res.data.results
            })
        },
    },
    mounted(){
        this.getServices()
    }
}
</script>
<template>
    <div class="locations">
        <v-container>
            <v-row wrap justify="center" align="center">
                <v-col cols="12" md="10">
                    <v-card light outlined class="mx-auto py-5" min-height="420">
                        <v-card-title class="justify-center mt-2">
                            <svg class="svg_icon">
                                <use xlink:href="../../statics/svgicons/sprite.svg#icon-map-signs" />
                            </svg>
                        </v-card-title>
                        <v-card-title class="justify-center font-weight-light title">Search Popular Locations</v-card-title>
                        <v-card-text class="text-center">
                            <v-row align="center" justify="center">
                                <v-col cols="6" md="2" v-for="(loc, i) in states" :key="i">
                                    <v-btn light outlined color="pry_light" :to="{name: 'ServicesByState', params: {id: loc.id, slug: loc.slug}}">{{ loc.state }}</v-btn>
                                </v-col>
                            </v-row>
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
            states: []
        }
    },
    created() {
        this.$axios.get('http://localhost:8000/api/popular_states/').then((res) =>{
            this.states = res.data
        })
    },
}
</script>

<style lang="scss" scoped>
    .locations{
        // height: 45rem;
        background: rgba(243, 243, 243, 0.5);
        .svg_icon{
            fill: #003B63 !important;
            height: 5.25rem;
        }
    }
</style>
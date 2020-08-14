<template>
    <v-container>
        <v-row justify="center">
            <v-col cols="12">
                <v-card class="mb-7" light outlined rounded elevation="8" min-height="400" :loading="mapLoading">
                    <v-card-title class="justify-center mt-3">Location on map</v-card-title>
                    <!-- <v-card-text>{{ location && location.street_address }}, {{ location && location.city }}. {{ location && location.state && location.state.state }}</v-card-text>  -->
                    <v-card-text class="subtitle-1">{{ loc }}</v-card-text>
                    <v-card-text>{{ street }}</v-card-text>
                    <v-card-text>{{ city }}</v-card-text>
                    <v-card-text>{{ state }}</v-card-text>
                    <v-card-text>{{ postcode }}</v-card-text>
                    <v-card-text>{{ country }}</v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    props: ['location'],
    data(){
        return{
            mapLoading: false,
            street: '',
            city: '',
            state: '',
            postcode: '',
            country: ''
        }
    },
    computed: {
        loc(){
            let add = this.location && this.location.street_address
            let city = this.location && this.location.city
            let state = this.location && this.location.state.state
            return add + ' ' + city + '. ' + state + '. Nigeria'
        }
    },
    // watch: {
    //     loc: function() {
    //         fetch(`https://autocomplete.geocoder.api.here.com/6.2/suggest.json?app_id=Tq3pxFdiiiN7LKEFwKYm&app_code=sVkpm1hApafQSk-QEQyQlATBcAvRCGXSV_76h7Fm2Tg&maxresults=1&query=${this.loc}`)
    //             .then(result => result.json())
    //             .then(result => {
    //                 if(result.suggestions && result.suggestions.length > 0) {
    //                     if(result.suggestions[0].address.houseNumber && result.suggestions[0].address.street) {
    //                         this.street = result.suggestions[0].address.houseNumber + " " + result.suggestions[0].address.street;
    //                     } else {
    //                         this.street = "";
    //                     }
    //                     this.city = result.suggestions[0].address.city ? result.suggestions[0].address.city : "";
    //                     this.state = result.suggestions[0].address.state ? result.suggestions[0].address.state : "";
    //                     this.postcode = result.suggestions[0].address.postalCode ? result.suggestions[0].address.postalCode : "";
    //                     this.country = result.suggestions[0].address.country ? result.suggestions[0].address.country : "";
    //                 } else {
    //                     this.street = "";
    //                     this.city = "";
    //                     this.state = "";
    //                     this.postalCode = "";
    //                     this.country = "";
    //                 }
    //             }, error => {
    //                 console.error(error);
    //             });
    //     }
    // },
    methods: {
        // getMap(){
        //     return fetch(`https://geocoder.api.here.com/6.2/geocode.json?app_id=Tq3pxFdiiiN7LKEFwKYm&app_code=sVkpm1hApafQSk-QEQyQlATBcAvRCGXSV_76h7Fm2Tg&searchtext=${this.loc}`)
        //         .then(result => result.json())
        //         .then(result => {
        //             if(result.Response.View.length > 0 && result.Response.View[0].Result.length > 0) {
        //                 let data = result.Response.View[0].Result[0];
        //                 return data;
        //             }
        //         }, error => {
        //             console.error(error);
        //         });
        //     }

        getMap(){
            this.$axios.get("https://maps.googleapis.com/maps/api/geocode/json?address="+this.loc+"&key=AIzaSyDSLwn1tVf4N-FdjULLFVo0HvtLU_9nHgc").then((res) => {
                console.log(res.data)
            })
            // navigator.geolocation.getCurrentPosition(
            //     position => {
            //         console.log(position.coords.latitude);
            //         console.log(position.coords.longitude);
            //     },
            //     error => {
            //         console.log(error.message);
            //     },
            // )
        }
    },
    mounted() {
        this.getMap()
    },
}
</script>
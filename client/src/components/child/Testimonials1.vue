<template>
    <div class="testimonial">
        <v-container>
            <v-row wrap justify="center" align="center">
                <v-col cols="10" md="6" class="align-center">
                    <div class="headline text-center font-weight-light">What our professionals are saying</div>
                    <v-carousel height="350" width="400" cycle class="mx-auto align-center">
                        <v-carousel-item v-for="(item, i) in items.slice(0, 3)" :key="i" :src="item.image" reverse-transition="fade-transition" transition="fade-transition">
                            <v-row class="fill-height py-3 mx-4" align="end" justify="center">
                                <div class="title title-wrap">{{ item.text }}</div>
                            </v-row>
                        </v-carousel-item>
                    </v-carousel>
                    <div class="cta">
                        <v-btn rounded dark large color="accent" to="/testimonials">All Testimonials</v-btn>
                    </div>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
export default {
    data(){
        return{
            api: 'http://localhost:8000/api/',
            items: []
        }
    },
    methods:{
        getTestimonials(){
            this.$axios.get(this.api + 'testimonials/').then((res) => {
                this.items = res.data
                console.log(res.data)
            })
        }
    },
    created(){
        this.getTestimonials()
    }
}
</script>

<style lang="scss" scoped>
    .testimonial{
        height: 40rem;
        padding: 2rem;
        margin-top: -4rem !important;
        margin-bottom: 3rem;

        .headline{
            font-size: 30px !important;
            margin-top: -25px;
            margin-bottom: 30px;
        }
        .v-image__image{
            border-radius: 6px !important;
        }

        .title-wrap{
            background: rgba(8, 8, 8, 0.582);
            color: #fff;
            border:1px solid rgba(192, 191, 191, 0.219);
            border-radius: 4px;
            padding: 12px 15px;
        }
        .cta{
            display: flex;
            margin: 2rem auto;
            justify-content: center;
            align-items: center;
        }
    }
</style>
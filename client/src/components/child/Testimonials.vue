<template>
    <div class="testimonial">
        <v-container>
           <v-row wrap justify="center">
                <svg class="svg_icon">
                    <use xlink:href="../../statics/svgicons/sprite.svg#icon-chat" />
                </svg>
                <v-col cols="12">
                    <div class="text-center headline font-weight-light mt-3">What our users are saying</div>
                </v-col>
            </v-row>
            <v-row wrap justify="center">
               <v-col cols="12" md="4" v-for="(item, i) in items.slice(0, 3)" :key="i">
                   <v-card flat elevation="6" :loading="isFetching" min-height="150" light class="pa-2">
                       <v-card-text v-text="item.text"></v-card-text>
                       <v-card-actions justify="space-around" align="center">
                           <v-avatar size="60px">
                               <v-img :src="item.image" alt="item.name"></v-img>
                           </v-avatar>
                           <div class="user">
                               <div class="subtitle-1 font-weight-regular">
                                   {{item.name}}
                               </div>
                               <div class="subtitle-1 font-weight-regular font-italic">
                                   {{item.company}}
                               </div>
                           </div>
                       </v-card-actions>
                   </v-card>
               </v-col>
           </v-row>
           <v-row justify="end" class="mt-3">
               <v-btn dark large rounded to="/testimonials" color="accent">See All Testimonials</v-btn>
            </v-row>
        </v-container>
    </div>
</template>

<script>
export default {
    data(){
        return{
            api: 'http://localhost:8000/api/',
            items: [],
            isFetching: false
        }
    },
    methods:{
        getTestimonials(){
            this.isFetching = true
            this.$axios.get(this.api + 'testimonials/').then((res) => {
                this.isFetching = false
                this.items = res.data
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
        min-height: 35rem;
        padding: 2rem;
        margin-top: 3rem !important;
        background: rgba(243, 243, 243, 0.5);

        .headline{
            font-size: 30px !important;
            margin-top: -25px;
            margin-bottom: 30px;
        }
        .user{
            flex: 0 1 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
            margin-left: .7rem;
        }
        .svg_icon{
            fill: #003B63 !important;
            height: 3rem;
        }
    }
</style>
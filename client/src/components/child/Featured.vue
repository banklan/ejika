<template>
    <div class="featured">
        <v-container>
            <v-row wrap justify="center">
                <v-col cols="12">
                    <div class="text-center font-weight-light headline my-5">Featured Services</div>
                    <v-row wrap justify="start" class="mt-5">
                        <v-col cols="12" md="4" v-for="service in services.slice(0,3)" :key="service.id">
                            <v-card light elevation="4" height="380" class="mt-5 mb-3" :to="{name: 'ServiceShow', params:{id: service.id, slug: service.slug}}">
                                <v-img :src="service.image" alt="Featured Images" aspect-ratio="1" height="200" transition="scale-transition"></v-img>
                                <v-card-title class="justify-center">{{ service.title | capFirstLetter}}</v-card-title>
                                <v-card-text class="text-center body-1 grey--text mt-n3">{{ service.state.state }} State | {{ service && service.subcategory.category.name }} </v-card-text>
                                <v-card-actions class="justify-space-around pb-4">
                                    <v-chip v-if="service.is_verified" class="ma-2" color="green darken-3" text-color="white">
                                        <v-avatar left><v-icon>mdi-checkbox-marked-circle</v-icon></v-avatar>
                                        Verified
                                    </v-chip>
                                    <v-rating v-model="service.ratings" readonly dense color="accent"></v-rating>
                                </v-card-actions>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
export default {
    props: ['services']
}
</script>

<style lang="scss" scoped>
    
</style>
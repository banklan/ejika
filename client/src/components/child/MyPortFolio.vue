<template>
    <v-card flat>
        <template v-if="newForm">
            <v-card-title class="justify-center mb-2">Add New Portfolio</v-card-title>
            <v-card-text class="mx-4">
                <v-text-field label="Title" type="text" v-model="newPf.title" required v-validate="'required|min:10|max:100'" :error-messages="errors.collect('title')" name="title"></v-text-field>
                <v-textarea rows="1" auto-grow label="Description" v-model="newPf.description" required v-validate="'required|min:12|max:400'" :error-messages="errors.collect('description')" name="description"></v-textarea>
                <v-text-field label="Cost Of Service (NGN)" v-model="newPf.cost" required v-validate="'required|decimal'" :error-messages="errors.collect('cost')" name="cost"></v-text-field>
                <v-card max-width="250" v-if="prevImg">
                    <div class="caption text-center pt-2">Preview</div>
                    <v-img :src="prevImgUrl" alt="Preview Img" height="150" contain></v-img>
                    <v-card-actions class="justify-center mt-1">
                        <v-btn text color="accent" @click="dropImg">Cancel</v-btn>
                    </v-card-actions>
                </v-card>
                <v-btn v-if="!prevImg" large outlined color="primary" @click="chooseFile" class="mt-3 mb-2">Upload Image</v-btn>
                <input type="file" ref="pImg" accept="image/*" style="display:none" @change.prevent="uploadFile">
                <v-alert color="blue lighten-3 mt-3">A portfolio is a showcase for your service. It is important and necessary to upload an image for every portfolio published.</v-alert>
            </v-card-text>
            <v-card-actions class="justify-center mt-2 mb-3">
                <v-btn large light color="primary" width="25%" @click="savePortFolio" :loading="loading">Publish</v-btn>
                <v-btn text color="accent" width="25%" @click="cancelForm">Cancel</v-btn>
            </v-card-actions>
        </template>
        <template v-else>
            <v-card-title v-if="portfolio.length < 5" class="justify-end">
                <v-btn right large elevation="6" dark color="accent" @click="newForm = true">Add Portfolio</v-btn>
            </v-card-title>
            <template v-if="portfolio.length === 0">
                <v-card-text class="subtitle-1">
                    You have not published any portfolio for your service.
                </v-card-text>
            </template>
            <template v-else>
                <v-list three-line nav>
                    <v-subheader class="mt-2">You have published {{ portfolio.length }} portfolio </v-subheader>
                    <template v-for="(item, i) in portfolio">
                        <v-list-item :key="item.title" class="mt-3">
                            <v-list-item-avatar>
                                <v-img :src="item.image" height="80"></v-img>
                            </v-list-item-avatar>
                            <v-list-item-content >
                                <router-link :to="{name: 'PortFolioShow', params: {id: item.id, slug:item.slug}}">
                                    <v-list-item-title class="title">{{ item.title | capFirstLetter }}</v-list-item-title>
                                    <v-list-item-subtitle class="pt-1 body-1">{{ item.description | capFirstLetter | truncate(120) }}</v-list-item-subtitle>
                                    <v-list-item-title class="accent--text pt-2">Cost: &#8358;{{ item.cost | price }}</v-list-item-title>
                                </router-link>
                                <v-card flat>
                                    <v-card-actions class="mb-n3">
                                        <v-btn icon><v-icon color="accent" @click="confirmDel(item.id, i)">delete</v-icon></v-btn>
                                    </v-card-actions>
                                </v-card>
                            </v-list-item-content>
                            <v-list-item-action>
                            </v-list-item-action>
                        </v-list-item>
                        <v-divider v-if="i != portfolio.length - 1" :key="i"></v-divider>
                    </template>   
                </v-list>
            </template>
        </template>
        <v-dialog v-model="delConfirmDial" max-width="380">
            <v-card>
                <v-card-title class="title mb-4">Are you sure you want to delete this portfolio?</v-card-title>
                <v-card-actions class="justify-center">
                    <v-btn text color="accent" @click="delConfirmDial = false">
                        Cancel
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" :loading="loading" large @click="deletePf">Yes, Delete</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-snackbar
            v-model="createPfSuccess" :timeout="6000" top color="green darken-1 white--text">
            Your portfolio has been created!.
            <v-btn text color="white--text" @click="createPfSuccess = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar
            v-model="createPfFail" :timeout="6000" top color="red darken-1 white--text">
            There is a problem trying to create your portfolio. Please update a valid image.
            <v-btn text color="white--text" @click="createPfFail = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar
            v-model="deleteSuccess" :timeout="6000" top color="green darken-1 white--text">
            Your portfolio has been deleted!.
            <v-btn text color="white--text" @click="deleteSuccess = false">Close</v-btn>
      </v-snackbar>
    </v-card>
</template>

<script>
    export default {
        props: ['portfolio'],
        data() {
            return{
                newForm: false,
                api: "http://localhost:8000/api/",
                newPf: {
                    title: '',
                    description: '',
                    cost: null,
                    image: null
                },
                prevImg: false,
                prevImgUrl: null,
                loading: false,
                createPfSuccess: false,
                delConfirmDial: false,
                itemToDel: null,
                indexToDel: null,
                deleteSuccess: false,
                createPfFail: false
            }
        },
        computed:{
            authToken() {
                return this.$store.getters.getToken;
            },
            fullHeader() {
                let conf = {
                    headers: {
                    Authorization: "Token " + this.authToken,
                    "Content-Type": "multipart/form-data",
                    },
                };
                return conf;
            },
        },
        methods: {
            savePortFolio(){
                this.$validator.validateAll().then((isValid) => {
                    if (isValid && this.newPf.image !== '') {
                        let form = new FormData();
                        form.append('title', this.newPf.title)
                        form.append('description', this.newPf.description)
                        form.append('cost', this.newPf.cost)
                        form.append('image', this.newPf.image)
                        this.loading = true;

                        this.$axios.post(this.api + 'my-portfolio/', form, this.fullHeader)
                            .then((res) => {
                                this.loading = false
                                this.portfolio.unshift(res.data)
                                this.cancelForm()
                                this.createPfSuccess = true
                            }).catch(() => {
                                this.loading = false
                                this.createPfFail = true
                            })
                    }
                })
            },
            chooseFile(){
                this.$refs.pImg.click()
            },
            uploadFile(e){
                this.prevImg = true
                const file = e.target.files[0]
                this.newPf.image = file
                this.prevImgUrl = URL.createObjectURL(file)
            },
            dropImg(){
                this.prevImg = false
                this.$refs.pImg.value = ''
                this.newPf.image = null
            },
            cancelForm(){
                this.newForm = false
                this.$refs.pImg.value = ''
                this.newPf.image = ''
                this.newPf.title = ''
                this.newPf.description = ''
                this.newPf.cost = ''
                this.prevImg = false
                this.prevImgUrl = null
            },
            confirmDel(item, i){
                this.delConfirmDial = true
                this.itemToDel = item
                this.indexToDel = i
            },
            deletePf(){
                this.loading = true
                this.$axios.delete(this.api + `my-portfolio/${this.itemToDel}/`, this.fullHeader).then(() =>{
                    this.loading = false
                    this.portfolio.splice(this.indexToDel, 1)
                    this.delConfirmDial = false
                    this.deleteSuccess = true
                })
            }
        },
    }
</script>

<style lang="scss" scoped>
    .v-list-item__content{
        a{
            text-decoration: none !important;
            color: rgb(36, 36, 36);

        }
    }
</style>
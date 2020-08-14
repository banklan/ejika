<template>
    <v-container>
        <v-row justify="center" class="mt-4">
            <v-col cols="12">
                <h2 class="title">
                    <v-btn rounded small color="accent" elevation="6" @click.prevent="$router.go(-1)"><v-icon left>chevron_left</v-icon> Back</v-btn>
                    <span class="ml-6"> Portfolio / {{ getService.title | capFirstLetter }}</span>
                </h2>
            </v-col>
        </v-row>
        <v-row class="justify-center mt-6">
            <v-col cols="12" md="8">
                <v-card shaped min-height="400" :loading="loading" v-if="!edit">
                    <template v-if="loading">
                        <v-progress-circular indeterminate color="accent" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
                    </template>
                    <template v-else>
                        <template v-if="portfolio">
                            <v-img :src="portfolio.image" aspect-ratio="1" alt="Portfolio image" height="300"></v-img>
                            <v-card-title class="mt-3 primary--text">{{ portfolio.title | capFirstLetter }}</v-card-title>
                            <v-card-subtitle class="mt-n3">
                                <p class="subtitle-2">Published By <strong>{{ portfolio.author && portfolio.author.fullname }}</strong> on {{ portfolio.created }}</p>
                            </v-card-subtitle>
                            <v-card-text class="subtitle-1">{{ portfolio.description | capFirstLetter }}</v-card-text>
                            <v-card-text class="subtitle-1 secondary--text mt-n2">Cost: &#8358;{{ portfolio.cost | price }}</v-card-text>
                            <template v-if="isLoggedIn">
                                <v-card-actions class="pb-8" v-if="portfolio.author && portfolio.author.id === getAuth.id">
                                    <v-btn text small color="primary" @click="openEdit"><v-icon left>edit</v-icon> Edit</v-btn>
                                    <v-btn text small color="accent" class="ml-5" @click="confirmDel = true"><v-icon left>delete_forever</v-icon>Delete</v-btn>
                                </v-card-actions>
                            </template>
                        </template>
                    </template>
                </v-card>
                <v-card shaped min-height="200" :loading="loading" transition="scale-transition" v-else>
                    <v-card-title class="mt-3 justify-center">Update Portfolio</v-card-title>
                    <v-card-text class="mx-auto">
                        <v-text-field label="Title" v-model="editPf.title" required v-validate="'required|min:10|max:100'" :counter="100" :error-messages="errors.collect('title')" name="title"></v-text-field>
                        <v-textarea label="Description" rows="1" auto-grow v-model="editPf.description" required v-validate="'required|min:20|max:400'" :counter="400" :error-messages="errors.collect('description')" name="description"></v-textarea>
                        <v-text-field label="Cost (Naira)" v-model="editPf.cost" required v-validate="'required|numeric'" :error-messages="errors.collect('cost')" name="cost"></v-text-field>
                    </v-card-text>
                    <v-card-actions class="justify-center mt-4 pb-8">
                        <v-btn text color="accent" @click="cancelEdit" large width="30%">Cancel</v-btn>
                        <v-btn dark color="primary" @click="update" large width="30%" :loading="isSaving">Update</v-btn>
                    </v-card-actions>
                    <v-divider></v-divider>
                    <v-card flat v-if="previewImgChange" class="mt-3">
                        <v-card-subtitle class="subtitle-1 text-center">Preview Image</v-card-subtitle>
                        <v-img :src="updtImg" alt="Preview Image" height="150" contain aspect-ratio="1"></v-img>
                        <v-card-actions class="justify-center my-5 pb-5">
                            <v-btn text color="accent" @click="previewImgChange = false">Cancel</v-btn>
                            <v-btn color="primary" dark :loading="loading" @click="changeImage">Upload</v-btn>
                        </v-card-actions>
                    </v-card>
                    <v-card-text class="py-4" v-else>
                        <v-btn outlined large color="primary" @click="pickFile" class="my-3"> Change Picture </v-btn>
                        <input type="file" style="display:none" ref="image" accept="image/*" @change="selectImg">
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col cols="12" md="4">
                <v-card shaped :loading="loading">
                    <template v-if="loading">
                        <v-progress-circular indeterminate color="accent" :width="4" :size="70" justify="center" class="mx-auto"></v-progress-circular>
                    </template>
                    <template v-else>
                        <template v-if="others">
                            <v-card-title class="justify-center title">Service Portfolio</v-card-title>
                            <v-divider></v-divider>
                            <v-card-text>
                                <v-list three-line nav>
                                    <template v-for="(item, i) in others">
                                        <v-list-item dense :to="{name: 'PortFolioShow', params: {id: item.id, slug:item.slug}}" :key="item.title" class="mt-3">
                                            <v-list-item-avatar>
                                                <v-img :src="item.image" height="80"></v-img>
                                            </v-list-item-avatar>
                                            <v-list-item-content class='mt-n3'>
                                                <v-list-item-title class="subtitle-1 primary--text">{{ item.title | capFirstLetter }}</v-list-item-title>
                                                <v-list-item-subtitle class="mt-n3 subtitle-2">{{ item.description | capFirstLetter | truncate(120) }}</v-list-item-subtitle>
                                            </v-list-item-content>
                                        </v-list-item>
                                        <v-divider v-if="i != portfolio.length - 1" :key="i"></v-divider>
                                    </template>   
                                </v-list>
                            </v-card-text>
                        </template>
                        <template v-else>
                            <v-card-title class="justify-center title">Service Portfolio</v-card-title>
                            <v-divider></v-divider>
                            <v-card-text class="subtitle-1">
                                No other portfolio have been published for this service.
                            </v-card-text>
                        </template>
                    </template>
                </v-card>
            </v-col>
            <v-snackbar v-model="updatedSuccess" :timeout="6000" top color="green darken-1 white--text">
                Your portfolio has been updated!.
                <v-btn text color="white--text" @click="updatedSuccess = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="modifyFail" :timeout="6000" top color="red darken-1 white--text">
                Update failed. Please try again.
                <v-btn text color="white--text" @click="modifyFail = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="deleteSuccess" :timeout="4500" top color="green darken-1 white--text">
                Portfolio deleted successfully.
                <v-btn text color="white--text" @click="deleteSuccess = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="deleteFail" :timeout="6000" top color="red darken-1 white--text">
                Portfolio deleted failed.
                <v-btn text color="white--text" @click="deleteFail = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="imageChanged" :timeout="6000" top color="green darken-1 white--text">
                Portfolio image changed successfully.
                <v-btn text color="white--text" @click="imageChanged = false">Close</v-btn>
            </v-snackbar>
            <v-dialog v-model="confirmDel" max-width="480">
                <v-card>
                    <v-card-title class="title justify-center">Are you sure you want to delete your portfolio?</v-card-title>
                    <v-card-text class="subtitle-1 accent--text">If you proceed, you will not be able to recover it.</v-card-text>
                    <v-card-actions>
                        <div class="flex-grow-1"></div>
                        <v-btn text dark color="red darken-1" @click="confirmDel = false"> Cancel </v-btn>
                        <v-btn dark :loading="loading" color="primary" @click="deletePf">Yes, Delete</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
    </v-container>
</template>

<script>
    export default{
        data(){
            return{
                id: this.$route.params.id,
                portfolio: null,
                loading: false,
                api: "http://localhost:8000/api/",
                others: [],
                edit: false,
                editPf: {
                    title: '',
                    description: '',
                    cost: ''
                },
                isSaving: false,
                updatedSuccess: false,
                modifyFail: false,
                confirmDel: false,
                deleteSuccess: false,
                deleteFail: false,
                image: '',
                updtImg: '',
                previewImgChange: false,
                imageChanged: false
            }
        },
        watch: {
            '$route.params':{
                handler(newVal){
                    let id = newVal
                    this.getPortfolio(id);
                    this.otherPortFolio(id)
                },
                immediate: true
            }
        },
        computed: {
            isLoggedIn(){
                return this.$store.getters.isLoggedIn
            },
            getAuth(){
                return this.$store.getters.getAuthUser
            },
            authToken() {
                return this.$store.getters.getToken;
            },
            config() {
                let conf = {
                    headers: {
                        Authorization: "Token " + this.authToken,
                    },
                };
                return conf;
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
            getService(){
                return this.$store.getters.getServFromStore
            }
        },
        methods: {
            getPortfolio(){
                this.loading = true
                this.$axios.get(this.api + `my-portfolio/${this.$route.params.id}/`, this.config).then((res) => {
                    this.loading = false
                    this.portfolio = res.data
                    console.log(res.data)
                })
            },
            otherPortFolio(){
                this.loading = true
                this.$axios.get(this.api + `other-portfolio/${this.$route.params.id}/`, this.config).then((res) => {
                    this.others = res.data
                })
            },
            openEdit(){
                this.edit = true
                this.editPf.title = this.portfolio.title
                this.editPf.description = this.portfolio.description
                this.editPf.cost = this.portfolio.cost
            },
            pickFile(){
                this.$refs.image.click()
            },
            cancelEdit(){
                this.edit = false
                this.$refs.image.value = ''
            },
            update(){
                this.$validator.validateAll().then((isValid) => {
                    if (isValid) {
                        this.isSaving = true;
                        this.$axios.put(this.api + `my-portfolio/${this.$route.params.id}/`, {
                            title: this.editPf.title,
                            description: this.editPf.description,
                            cost: this.editPf.cost
                        },this.config).then((res) => {
                            this.isSaving = false
                            this.edit = false
                            this.portfolio = res.data
                            this.updatedSuccess = true
                        }).catch(() =>{
                            this.isSaving = false
                            this.modifyFail = true
                        })
                    }
                })
            },
            selectImg(e){
                const image = e.target.files[0]
                this.image = image
                this.previewImgChange = true 
                this.updtImg = URL.createObjectURL(image)
            },
            changeImage(){
                if(this.image !== ''){
                    this.loading = true
                    let form = new FormData();
                    form.append('image', this.image)
                    this.$axios.put(this.api + `portfolio/update_image/${this.$route.params.id}/`, form, this.fullHeader)
                        .then(() => {
                            this.loading = false
                            this.imageChanged = true
                            this.previewImgChange = false
                            this.edit = false
                            this.getPortfolio()
                        }).catch(() => {
                            this.loading = false
                        })
                }
            },
            cancelUpload(){
                this.$refs.image.value = ''
                this.previewImgChange = false
                this.updtImg = null
            },
            deletePf(){
                this.$axios.delete(this.api + `my-portfolio/${this.$route.params.id}/`, this.config).
                    then(() => {
                        this.deleteSuccess = true
                        this.confirmDel = false
                        setTimeout(() => {
                            this.$router.push('/profile')
                        }, 3000);
                    }).catch(() => {
                        this.deleteFail = true
                        this.confirmDel = false
                    })
            }
        },
        created(){
            this.getPortfolio()
            this.otherPortFolio()
        }
    }
</script>
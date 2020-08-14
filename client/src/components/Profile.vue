<template>
  <v-container>
    <v-row class="justify-center mt-6">
      <v-col cols="12" md="10">
        <v-card light>
          <v-tabs v-model="tab" background-color="primary" dark>
            <v-tab>Profile</v-tab>
            <v-tab>Service</v-tab>
            <v-tab>PortFolio</v-tab>
          </v-tabs>
          <v-tabs-items v-model="tab">
            <v-tab-item>
              <v-card flat>
                <v-row>
                  <v-col cols="12" v-if="!editNm">
                    <v-card-text>
                      <v-simple-table fixed-header min-height="150px">
                        <template v-slot:default>
                          <tr>
                            <th width="25%">First Name</th>
                            <td>{{ profile && profile.first_name }}</td>
                          </tr>
                          <tr>
                            <th>Last Name</th>
                            <td>{{ profile && profile.last_name }}</td>
                          </tr>
                          <tr>
                            <th>Email</th>
                            <td>{{ profile && profile.email }}</td>
                          </tr>
                        </template>
                      </v-simple-table>
                    </v-card-text>
                    <v-card-actions class="justify-flex-start mb-5 flex-wrap pa-5 ml-3">
                      <v-btn text class="primary white--text mb-5 mr-2" @click="EditProfile">Edit Profile</v-btn>
                      <v-btn outlined color="primary" class="mb-5 mr-2" @click="openPswdDialg = true">Change Password</v-btn>
                      <v-btn text class="accent white--text mb-5 mr-2" @click="disableConfirm = true">Disable Profile</v-btn>
                    </v-card-actions>
                  </v-col>
                  <v-col cols="12" md="6" v-else>
                    <v-card-subtitle class="subtitle-1 mt-1 ml-2">Update Profile</v-card-subtitle>
                    <v-card-text>
                      <v-text-field label="First Name" v-model="editNames.first" v-validate="'required'" :error-messages="errors.collect('editNames.first')" name="first" data-vv-scope="editNames"></v-text-field>
                      <v-text-field label="Last Name" v-model="editNames.last" v-validate="'required'" :error-messages="errors.collect('editNames.last')" name="last" data-vv-scope="editNames"></v-text-field>
                    </v-card-text>
                    <v-card-actions class>
                      <v-btn text dark color="red" @click="editNm = false">Cancel</v-btn>
                      <v-spacer></v-spacer>
                      <v-btn class="primary white--text mb-5 mr-2" @click="updateProfile">Save</v-btn>
                    </v-card-actions>
                  </v-col>
                </v-row>
              </v-card>
            </v-tab-item>
            <v-tab-item>
              <v-card flat class="service_card">
                <v-row v-if="noService == false">
                  <v-col cols="12" v-if="!editServ">
                    <v-card-text>
                      <v-simple-table fixed-header min-height="200px">
                        <template v-slot:default>
                          <tr>
                            <th>Company</th>
                            <td>{{ service && service.title | capFirstLetter }}</td>
                          </tr>
                          <tr>
                            <th>Status</th>
                            <td v-if="service.is_verified == true">Verified</td>
                            <td v-else>Not Verified</td>
                          </tr>
                          <tr>
                            <th width="25%">Service Description</th>
                            <td>{{ service && service.description | capFirstLetter }}</td>
                          </tr>
                          <tr>
                            <th>Service Category</th>
                            <td>{{ service && service.subcategory.name }}</td>
                          </tr>
                          <tr>
                            <th>Phone Number</th>
                            <td>{{ service && service.phone_number }}</td>
                          </tr>
                          <tr>
                            <th>Address</th>
                            <td>{{ service && service.street_address | capFirstLetter }}</td>
                          </tr>
                          <tr>
                            <th>City/Town</th>
                            <td> {{ service && service.city | capFirstLetter }}</td>
                          </tr>
                          <tr>
                            <th>Location</th>
                            <td>{{ service && service.state.state }}</td>
                          </tr>
                          <tr>
                            <th>Website</th>
                            <td>{{ service && service.website }}</td>
                          </tr>
                          <tr>
                            <th>Facebook</th>
                            <td>{{ service && service.fb || null}}</td>
                          </tr>
                          <tr>
                            <th>Instagram</th>
                            <td>{{ service && service.instag }}</td>
                          </tr>
                        </template>
                      </v-simple-table>
                    </v-card-text>
                    <v-card flat light max-height="350" v-if="service && service.image">
                        <v-img v-if="!previewImg" :src="service && service.image" contain aspect-ratio="1" height="300" class="my-3" alt="service photo"></v-img>
                        <template v-else>
                            <v-card-subtitle class="text-center subtitle-1">Preview Upload Image</v-card-subtitle>
                            <v-img :src="previewImgUrl" height="200" contain alt="service photo" aspect-ratio="1"></v-img>
                            <v-card-actions class="justify-center mt-4 ml-n3">
                              <v-btn small @click="saveImg"><v-icon color="primary" left>cloud</v-icon></v-btn> 
                              <v-btn text small @click="removeImg"><v-icon color="accent">delete</v-icon></v-btn> 
                            </v-card-actions>
                        </template>
                    </v-card>
                    <v-card-actions class="justify-space-around flex-wrap px-3">
                      <v-btn v-if="service" dark shaped color="accent" class="mb-5 mr-5" :to="{name: 'ServiceShow', params: {id: service.id, slug: service.slug}}">Go TO Service</v-btn>
                      <v-btn outlined color="secondary" class="mb-5 mr-5" @click="openUpload">Update Image</v-btn>
                      <input type="file" ref="image" style="display:none" @change.prevent="pickImg" accept="image/*"> 
                      <v-btn dark color="primary" class="mb-5 mr-5" @click="modifyService">Edit</v-btn>
                      <v-btn text class="red white--text mb-5" @click="confirmDelete = true">
                        <v-icon left>delete_forever</v-icon>Delete Service
                      </v-btn>
                    </v-card-actions>
                  </v-col>
                  <v-col cols="12" md="8" v-else>
                    <v-card-subtitle class="subtitle-1 mt-1 ml-2">Update Service</v-card-subtitle>
                    <v-divider></v-divider>
                    <v-card-text>
                      <v-text-field label="Title" v-model="editService.title" v-validate="'required|min:5|max:200'" :counter="200" :error-messages="errors.collect('editService.title')" name="title" data-vv-scope="editService"></v-text-field>
                      <v-text-field label="Phone Number" v-model="editService.phone_number" v-validate="'required|numeric'" :error-messages="errors.collect('editService.phone_number')" name="phone_number" data-vv-scope="editService"></v-text-field>
                      <v-textarea auto-grow label="Street Address" v-model="editService.street_address" v-validate="'required|min:10|max:200'" :error-messages="errors.collect('editService.street_address')" name="street_address" data-vv-scope="editService"></v-textarea>
                      <v-text-field label="City/Town" v-model="editService.city" v-validate="'required'" :error-messages="errors.collect('editService.city')" name="city" data-vv-scope="editService"></v-text-field>
                      <v-select label="State" v-model="editService.state" :items="states" item-text="state" return-object required persistent-hint v-validate="'required'" :error-messages="errors.collect('editService.state')" name="state" data-vv-scope="editService"></v-select>
                      <v-select label="Category" v-model="editService.subcategory" :items="subcategories" item-text="name" return-object required persistent-hint v-validate="'required'" :error-messages="errors.collect('editService.subcategory')" name="subcategory" data-vv-scope="editService"></v-select>
                      <v-textarea auto-grow label="Description" v-model="editService.description" v-validate="'required|min:20|max:2000'" :error-messages="errors.collect('editService.description')" name="description" data-vv-scope="editService"></v-textarea>
                      <v-text-field label="Website" v-model="editService.website" v-validate="'url'" :error-messages="errors.collect('editService.website')" name="website" data-vv-scope="editService"></v-text-field>
                      <v-text-field label="Facebook" v-model="editService.fb" name="fb" data-vv-scope="editService"></v-text-field>
                      <v-text-field label="Instagram" v-model="editService.instag" name="instag" data-vv-scope="editService"></v-text-field>
                    </v-card-text>
                    <v-card-actions class="justify-center mb-3">
                      <v-btn text color="red" @click="editServ = false">Cancel</v-btn>
                      <v-btn class="px-8" color="primary white--text" :loading="loading" @click="updateService" large>Update</v-btn>
                    </v-card-actions>
                  </v-col>
                </v-row>
                <v-row v-else>
                  <v-col cols="12">
                    <template v-if="!createService">
                      <v-card-text class="ml-2">No service has been published for this account.</v-card-text>
                      <v-card-actions class="ml-3">
                        <v-btn dark color="primary" @click="openCreateService">Add Service</v-btn>
                      </v-card-actions>
                    </template>
                    <template v-else>
                      <v-card-text>
                        <v-text-field label="Title" v-model="newService.title" v-validate="'required|min:10|max:200'" :error-messages="errors.collect('newService.title')" name="title" data-vv-scope="newService" persistent-hint></v-text-field>
                        <v-textarea auto-grow label="Description" v-model="newService.description" v-validate="'required|min:20|max:2000'" :error-messages=" errors.collect('newService.description')" name="description" data-vv-scope="newService"></v-textarea>
                        <v-text-field label="Street Address1" placeholder="e.g No 1," v-model="newService.street_address1" v-validate="'required|max:20'" :error-messages="errors.collect('newService.street_address1')" name="street_address1" data-vv-as="Street Address1" data-vv-scope="newService"></v-text-field>
                        <v-textarea auto-grow rows="1" label="Street Address2" placeholder="e.g Xyz street," v-model="newService.street_address2" v-validate="'required|min:10|max:180'" :error-messages="errors.collect('newService.street_address2')" name="street_address2" data-vv-as="Street Address2" data-vv-scope="newService"></v-textarea>
                        <v-text-field label="City" v-model="newService.city" v-validate="'required|max:50'" :error-messages="errors.collect('newService.city')" name="city" data-vv-scope="newService"></v-text-field>
                        <v-text-field label="Phone Number" placeholder="e.g 08012345678" v-model="newService.phone_number" v-validate="'required|numeric|min:8|max:14'" :error-messages="errors.collect('newService.phone_number')" name="phone_number" data-vv-scope="newService"></v-text-field>
                        <v-select label="State" v-model="newService.state" :items="states" item-text="state" return-object v-validate="'required'" :error-messages="errors.collect('newService.state')" name="state" data-vv-scope="newService"></v-select>
                        <v-select label="Category" v-model="newService.subcategory" :items="subcategories" item-text="name" return-object v-validate="'required'" :error-messages="errors.collect('newService.subcategory')" name="subcategory" data-vv-scope="newService"></v-select>
                        <v-text-field label="Website - http://" placeholder="www.mywebsite.com" v-model="newService.website" v-validate="'url'" :error-messages="errors.collect('newService.website')" name="website" data-vv-scope="newService"></v-text-field>
                        <v-text-field label="Facebook name" placeholder="Enter your facebook name" v-model="newService.fb" name="fb" data-vv-scope="newService"></v-text-field>
                        <v-text-field label="Instagram handle" placeholder="Enter your instagram handle" v-model="newService.instag" name="instag" data-vv-scope="newService"></v-text-field>
                      </v-card-text>
                      <v-card-actions>
                        <div class="flex-grow-1"></div>
                        <v-btn text color="red darken-1" @click="createService = false">cancel</v-btn>
                        <v-btn dark color="secondary" @click="addService" :loading="loading">Save</v-btn>
                      </v-card-actions>
                    </template>
                  </v-col>
                </v-row>
              </v-card>
            </v-tab-item>
            <v-tab-item>
              <template v-if="service && service.portfolio">
                <my-portfolio :portfolio="service && service.portfolio"></my-portfolio>
              </template>
              <template v-else>
                <v-card flat>
                  <v-card-text class="ml-2">No service has been published for this account</v-card-text>
                </v-card>
              </template>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-snackbar v-model="editNameSuccess" :timeout="6000" top color="green darken-1 white--text">
        Your profile have been modified.
        <v-btn text color="white--text" @click="editNameSuccess = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="editServiceSuccess" :timeout="6000" top color="green darken-1 white--text">
        Your service have been modified.
        <v-btn text color="white--text" @click="editServiceSuccess = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar
        v-model="createSuccess" :timeout="6000" top color="green darken-1 white--text">
        Your service have been created!.
        <v-btn text color="white--text" @click="createSuccess = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar
        v-model="deleteSuccess" :time="6000" top color="green darken-2 white--text">
        Your service has been deleted.
        <v-btn text color="white--text" @click="deleteSuccess = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="deleteFailed" :time="8000" top color="red darken-2 white--text">
        Service delete failed, please try again.
        <v-btn text color="white--text" @click="deleteFailed = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="imageUploadSuccess" :time="6000" top color="green darken-1 white--text">Your service image has been updated 
        <v-btn text color="white--text" @click="imageUploadSuccess = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="imageUploadFail" :time="6000" top color="red darken-2 white--text">Your service image upload failed. Please try again! 
        <v-btn text color="white--text" @click="imageUploadFail = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="pswdUpdateSuccess" :time="6000" top color="green darken-2 white--text">Password has been updated successfully. 
        <v-btn text color="white--text" @click="pswdUpdateSuccess = false">Close</v-btn>
      </v-snackbar>
      <v-snackbar v-model="disabledSuccess" :time="3000" top color="green darken-2 white--text">Account has been disabled. 
        <v-btn text color="white--text" @click="disabledSuccess = false">Close</v-btn>
      </v-snackbar>
      <v-dialog v-model="confirmDelete" max-width="450">
        <v-card>
          <v-card-title class="title justify-center">Are you sure you want to delete your service?</v-card-title>
          <v-card-text class="subtitle-1 accent--text">If you proceed, you will not be able to recover it.</v-card-text>
          <v-card-actions>
            <div class="flex-grow-1"></div>
            <v-btn text dark color="red darken-1" @click="confirmDelete = false"> Cancel </v-btn>
            <v-btn dark :loading="loading" color="primary" @click="deleteService">Yes, Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="openPswdDialg" max-width="420">
        <v-card>
          <v-card-title class="title justify-center">Change Password</v-card-title>
          <v-card-subtitle v-if="pswdChngErr" class="text-center py-2 mx-2 pink lighten-4 red--text">{{ pswdErr }}</v-card-subtitle>
          <v-card-text>
            <v-text-field label="Old Password" type="password" v-model="passwordChange.old" v-validate="'required|max:20|min:5'" :error-messages="errors.collect('pswdChang.old_pswd')" name="old_pswd" data-vv-as="Old Password" data-vv-scope="pswdChang"></v-text-field>
            <v-text-field label="New Password" type="password" v-model="passwordChange.new" v-validate="'required|max:20|min:5'" :error-messages="errors.collect('pswdChang.new_pswd')" name="new_pswd" ref="new_pswd" data-vv-as="new password" data-vv-scope="pswdChang"></v-text-field>
            <v-text-field label="Confirm New Password" type="password" v-model="passwordChange.confirm" v-validate="'required|confirmed:new_pswd'" :error-messages="errors.collect('pswdChang.confirm')" name="confirm" data-vv-as="confirm password" data-vv-scope="pswdChang"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <div class="flex-grow-1"></div>
            <v-btn text dark color="red darken-1" @click="openPswdDialg = false"> Cancel </v-btn>
            <v-btn dark :loading="loading" color="primary" @click="changePswd" width="50%">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="disableConfirm" max-width="450">
        <v-card>
          <v-card-title class="title justify-center">Are you sure you want to disable your account?</v-card-title>
          <v-card-text class="body-2">
            <v-alert type="warning">To enable it and have access to your account back, you have to contact us.</v-alert>
          </v-card-text>
          <v-card-actions>
            <div class="flex-grow-1"></div>
            <v-btn text dark color="red darken-1" @click="disableConfirm = false"> Cancel </v-btn>
            <v-btn dark :loading="loading" color="primary" @click="disableAccount">Yes, Disable</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      tab: null,
      items: [],
      profile: null,
      service: null,
      loading: false,
      editNames: {
        first: "",
        last: "",
      },
      api: "http://localhost:8000/api/",
      subcategories: [],
      states: [],
      editNameSuccess: false,
      editServ: false,
      editService: {
        title: "",
        description: "",
        phone_number: "",
        street_address: "",
        city: "",
        state: {},
        subcategory: null,
        website: '',
        fb: '',
        instag: ''
      },
      editNm: false,
      editServiceSuccess: false,
      noService: false,
      createService: false,
      newService: {
        title: "",
        description: "",
        street_address1: "",
        street_address2: "",
        phone_number: "",
        city: "",
        state: null,
        subcategory: null,
        website: '',
        fb: '',
        instag: ''
      },
      createSuccess: false,
      confirmDelete: false,
      deleteSuccess: false,
      deleteFailed: false,
      image: null,
      previewImgUrl: '',
      previewImg: false,
      imageUploadSuccess: false,
      imageUploadFail: false,
      openPswdDialg: false,
      passwordChange: {
        old: '',
        new: '',
        confirm: ''
      },
      pswdChngErr: false,
      pswdErr: '',
      pswdUpdateSuccess: false,
      disableConfirm: false,
      disabledSuccess: false,
    };
  },
  computed: {
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
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      if (vm.authToken) {
        next();
      }else{
        next('/')
      }
    });
  },
  methods: {
    getAuthUser() {
      const config = {
        headers: {
          Authorization: "Token " + this.authToken,
          "Content-Type": "multipart/form-data",
        },
      };
      this.$axios
        .get("http://localhost:8000/api/profile/", config)
        .then((res) => {
          // console.log(res.data);
          this.profile = res.data;
        });
    },
    getService() {
      const config = {
        headers: {
          Authorization: "Token " + this.authToken,
        },
      };
      this.$axios
        .get("http://localhost:8000/api/auth_service/", config)
        .then((res) => {
          if (res.data.status != 404) {
            this.noService = false;
            this.service = res.data;
            this.$store.commit('store_service', res.data)
          } else {
            this.noService = true;
          }
        });
    },
    EditProfile() {
      this.editNm = true;
      this.editNames.first = this.profile.first_name;
      this.editNames.last = this.profile.last_name;
    },
    updateProfile() {
      this.$validator.validateAll("editNames").then((isValid) => {
        if (isValid) {
          this.loading = true;
          this.$axios.put(this.api + "profile/update/",{
                first_name: this.editNames.first,
                last_name: this.editNames.last,
              },this.config).then((res) => {
              this.loading = false;
              this.profile = res.data;
              this.editNm = false;
              this.editNameSuccess = true;
            });
        }
      });
    },
    modifyService() {
      this.editServ = true;
      this.getCateg();
      this.getStates();
      this.editService.title = this.service.title;
      this.editService.description = this.service.description;
      this.editService.phone_number = this.service.phone_number;
      this.editService.street_address = this.service.street_address;
      this.editService.city = this.service.city;
      this.editService.state = this.service.state;
      this.editService.subcategory = this.service.subcategory;
      this.editService.website = this.service.website !== null ? this.service.website.substring(7) : ''
      this.editService.fb = this.service.fb
      this.editService.instag = this.service.instag
    },
    updateService() {
      this.$validator.validateAll("editService").then((isValid) => {
        if (isValid) {
          this.loading = true
          this.$axios.patch(
              this.api + "update_service/",{
                title: this.editService.title,
                description: this.editService.description,
                phone_number: this.editService.phone_number,
                street_address: this.editService.street_address,
                city: this.editService.city,
                state: this.editService.state,
                subcategory: this.editService.subcategory,
                website: 'http://'+ this.editService.website,
                fb: this.editService.fb,
                instag: this.editService.instag
              },this.config).then((res) => {
              this.loading = false;
              this.service = res.data;
              this.editServ = false;
              this.editServiceSuccess = true;
            });
        }
      });
    },
    openCreateService() {
      this.createService = true;
      this.getCateg();
      this.getStates();
    },
    addService() {
      this.$validator.validateAll("newService").then((isValid) => {
        if (isValid) {
          this.loading = true;
          let street_address = this.newService.street_address1 + ", " + this.newService.street_address2;
          this.$axios.post(this.api + "service/create/",{
                title: this.newService.title,
                description: this.newService.description,
                street_address: street_address,
                phone_number: this.newService.phone_number,
                city: this.newService.city,
                state: this.newService.state,
                subcategory: this.newService.subcategory,
                website: 'http://' + this.newService.website,
                fb: this.newService.fb,
                instag: this.newService.instag
              },
              this.config).then(() => {
              this.loading = false;
              this.getService();
              this.createSuccess = true;
            })
            .catch(() => {
              this.loading = false;
            });
        }
      });
    },
    deleteService() {
      this.loading = true;
      this.$axios
        .delete(this.api + "service/delete/", this.config)
        .then(() => {
          this.loading = false;
          this.confirmDelete = false;
          this.deleteSuccess = true;
          this.noService = true;
          this.$router.go();
        })
        .catch(() => {
          this.loading = false;
          this.confirmDelete = false;
          this.deleteFailed = true;
        });
    },
    openUpload(){
      this.$refs.image.click()
    },
    pickImg(e){
      const file = e.target.files[0]
      this.image = file
      this.previewImg = true
      this.previewImgUrl = URL.createObjectURL(file)
    },
    saveImg(){
      if(this.image !== null){
        this.loading = true
        let form = new FormData();
        form.append('image', this.image)

        this.$axios.put(this.api + 'service/update_image/', form, this.fullHeader).then((res) => {
          this.loading = false
          this.service.image = res.data
          this.imageUploadSuccess = true
          this.getService()
          this.removeImg()
        }).catch(() => {
          this.loading = false
          this.imageUploadFail = true
        })
      }
    },
    removeImg(){
      this.$refs.image.value = ''
      this.previewImgUrl = '';
      this.previewImg = false;
    },
    getCateg() {
      this.$axios.get(this.api + "subcategories/").then((res) => {
        this.subcategories = res.data;
      });
    },
    getStates() {
      this.$axios.get(this.api + "states/").then((res) => {
        this.states = res.data;
      });
    },
    changePswd(){
        this.$validator.validateAll('pass').then((isValid) =>{
          if(isValid){
              this.loading = true
              if(this.passwordChange.old != this.passwordChange.new){
                  this.$axios.put(this.api + 'password-change/', {
                    password: this.passwordChange.old,
                    new_password: this.passwordChange.new,
                    confirm_password: this.passwordChange.confirm
                  }, this.config).then(() => {
                    this.loading =  false
                    this.pswdUpdateSuccess = true
                    this.removePswdDialog()
                  }).catch(() => {
                     this.loading = false
                     this.pswdChngErr = true
                     this.pswdErr = 'Password change failed. Your old password might be wrong!'
                  })
              }else{
                this.loading = false
                this.pswdChngErr = true
                this.pswdErr = 'The new password is the same with the old password you are trying to change!'
              }
          }
        })
    },
    removePswdDialog(){
        this.openPswdDialg = false
        this.$validator.reset()
        this.passwordChange.old = ''
        this.passwordChange.new = ''
        this.passwordChange.confirm = ''
    },
    disableAccount(){
      this.loading = true
      this.$axios.put(this.api + 'disable-account/', {}, this.config).then(() => {
        this.loading = false
        setTimeout(() => {
            this.disabledSuccess = true
        }, 3000);
        this.logout()
      }).catch(() => {
        this.loading = false
      })
    },
    logout() {
      if (this.authToken) {
        this.$store.commit("logout");
        if (this.$route.path != "/") {
          this.$router.push("/");
        }
      }
    }
  },
  mounted() {
    this.getAuthUser();
    this.getService();
    // console.log("mounted " + this.service);
  },
};
</script>

<style lang="scss" scoped>
  .v-data-table table tr th,
  .v-data-table table tr td {
    font-size: 15px !important;
    font-family: 'Roboto', sans-serif;
  }
  .service_card{
    .v-card__actions{
      .v-input{
        display: none !important;
      }
    }
  }
</style>

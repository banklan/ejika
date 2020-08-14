<template>
    <div>
        
    </div>
</template>

<script>
export default {
    data(){
        return{
            map: {},
            platform: {},
            geocoder: {},
            appId: null,
            aooCode: null,
        }
    },
    props: {
        location: ''
    },
    created(){
        this.platform = new H.service.Platform({
            "app_id": this.appId,
            "app_code": this.appCode
        });
        this.geocoder = this.platform.getGeocodingService()
    }
}
</script>
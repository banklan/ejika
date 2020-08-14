const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')

module.exports = {
    // configureWebpack:{
    //     plugins: [
    //         new VuetifyLoaderPlugin()
    //     ]
    // },
    "transpileDependencies": [
        "vuetify"
    ],
    chainWebpack: (config) => {
        config.module
            .rule('vue')
            .use('vue-loader')
            .loader('vue-loader')
            .tap((options) => {
                options.transformAssetUrls = {
                    "v-img": ['src', 'lazy-src'],
                    "v-card": 'src',
                    "v-card-media": 'src',
                    "v-responsive": 'src',
                    "v-carousel-item": 'src',
                    "img" : 'src' 
                };
                return options;
            });
            config.plugin("VuetifyLoaderPlugin").tap((args) => [
                {
                    progressiveImages: true,
                },
            ]);
        }}

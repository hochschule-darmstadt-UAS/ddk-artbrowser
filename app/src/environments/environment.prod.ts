export const environment = {
  production: true,
  elasticBase: '/api',
  iconclassBase: '/api/iconclass',
  imagesBase: '/api/images',
  analytics: window.location.host === 'https://cai-ddk-art-browser-staging.fbi.h-da.de'
    ? {
      // staging
      enabled: true,
      url: 'https://openartbrowser.org/api/analytics/',
      propertyId: '3'
    }
    : {
      // production
      enabled: true,
      url: '/api/analytics/',
      propertyId: '1'
    }
};

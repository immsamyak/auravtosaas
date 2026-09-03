from . import delivery_city
from . import delivery_district
from . import delivery_province
from . import product_review
from . import collection
from . import gift_card_transaction
from . import gift_card
from . import api_log
from . import webhook_endpoint
from . import api_key
from . import email_campaign
from . import newsletter_subscriber
from . import coupon
from . import popup_banner

from django.urls import path, include
from .dashboard import DashboardView, AdminLoginView, AdminLogoutView

from .platform_settings import SystemSettingListView, SystemSettingCreateView, SystemSettingUpdateView
from .brand_settings import BrandSettingListView, BrandSettingCreateView, BrandSettingUpdateView
from .landing_page import LandingPageConfigUpdateView
from .pages_footer import PageListView, PageCreateView, PageUpdateView
from .footer_sections import FooterSectionListView, FooterSectionCreateView, FooterSectionUpdateView
from .testimonials import TestimonialListView, TestimonialCreateView, TestimonialUpdateView
from .blogs import BlogPostListView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView
from .contact_messages import ContactMessageListView, ContactMessageDetailView, ContactMessageDeleteView
from .landing_page_features import LandingPageFeatureListView, LandingPageFeatureCreateView, LandingPageFeatureUpdateView, LandingPageFeatureDeleteView
from .landing_page_extras import FAQItemListView, FAQItemCreateView, FAQItemUpdateView, FAQItemDeleteView, MetricListView, MetricCreateView, MetricUpdateView, MetricDeleteView, IntegrationPlatformListView, IntegrationPlatformCreateView, IntegrationPlatformUpdateView, IntegrationPlatformDeleteView
from .feature_flags import FeatureFlagListView, FeatureFlagCreateView, FeatureFlagUpdateView
from .platform_integrations import PlatformIntegrationListView, PlatformIntegrationCreateView, PlatformIntegrationUpdateView
from .global_settings import GlobalSettingsUpdateView, TestEmailView
from .users import UserListView, UserCreateView, UserUpdateView
from .roles_groups import GroupListView, GroupCreateView, GroupUpdateView
from .consumers import ConsumerProfileListView, ConsumerProfileCreateView, ConsumerProfileUpdateView
from .user_photo_profiles import UserPhotoProfileListView, UserPhotoProfileCreateView, UserPhotoProfileUpdateView
from .brands import BrandListView, BrandCreateView, BrandUpdateView, ImpersonateBrandView, ImpersonateRevertView
from .brand_integrations import BrandIntegrationListView, BrandIntegrationCreateView, BrandIntegrationUpdateView
from .returns import ReturnRequestListView, ReturnRequestUpdateView
from .brand_staff import BrandStaffListView, BrandStaffUpdateView
from .store_themes import StoreThemeListView, StoreThemeCreateView, StoreThemeUpdateView
from .products import ProductListView, ProductCreateView, ProductUpdateView
from .product_variants import ProductVariantListView, ProductVariantCreateView, ProductVariantUpdateView
from .categories import CategoryListView, CategoryCreateView, CategoryUpdateView
from .colors import ColorListView, ColorCreateView, ColorUpdateView
from .vto_dashboard import VTOQueueDashboardView, QAModerationView, QAModerationActionView
from .sizes import SizeListView, SizeCreateView, SizeUpdateView
from .size_charts import SizeChartListView, SizeChartCreateView, SizeChartUpdateView
from .style_tags import StyleTagListView, StyleTagCreateView, StyleTagUpdateView
from .product_types import ProductTypeListView, ProductTypeCreateView, ProductTypeUpdateView
from .product_ai_profiles import ProductAIProfileListView, ProductAIProfileCreateView, ProductAIProfileUpdateView
from .locations import LocationListView, LocationCreateView, LocationUpdateView
from .stock_levels import StockLevelListView, StockLevelCreateView, StockLevelUpdateView
from .global_orders import OrderListView, OrderCreateView, OrderUpdateView
from .carts import CartListView, CartCreateView, CartUpdateView
from .shipping_zones import ShippingZoneListView, ShippingZoneCreateView, ShippingZoneUpdateView
from .virtual_try_on_jobs import VirtualTryOnListView, VirtualTryOnCreateView, VirtualTryOnDetailView
from .fit_passports import FitPassportListView, FitPassportCreateView, FitPassportUpdateView
from .vto_products import VTOProductListView, VTOProductCreateView, VTOProductUpdateView
from .vto_product_assets import VTOProductAssetsListView, VTOProductAssetsCreateView, VTOProductAssetsUpdateView
from .virtual_wardrobe_looks import VirtualWardrobeLookListView, VirtualWardrobeLookCreateView, VirtualWardrobeLookUpdateView
from .vto_sessions import VTOSessionListView, VTOSessionCreateView, VTOSessionDetailView
from .vto_photo_vaults import VTOPhotoVaultListView, VTOPhotoVaultCreateView, VTOPhotoVaultUpdateView
from .size_recommendations import SizeRecommendationListView, SizeRecommendationCreateView, SizeRecommendationUpdateView
from .subscriptions import BrandSubscriptionListView, BrandSubscriptionCreateView, BrandSubscriptionUpdateView
from .subscription_plans import SubscriptionPlanListView, SubscriptionPlanCreateView, SubscriptionPlanUpdateView
from .audit_logs import AuditLogListView
from .email_logs import EmailLogListView

app_name = 'admin'

urlpatterns = [
    # Notifications
    path('notifications/', include([
        path('', __import__('apps.admin.views.notifications', fromlist=['']).NotificationCampaignListView.as_view(), name='notification_list'),
        path('create/', __import__('apps.admin.views.notifications', fromlist=['']).NotificationCampaignCreateView.as_view(), name='notification_create'),
        path('test/', __import__('apps.admin.views.notifications', fromlist=['']).test_email_api, name='notification_test'),
        path('templates/', __import__('apps.admin.views.notifications', fromlist=['']).SystemEmailTemplateListView.as_view(), name='notification_template_list'),
        path('templates/<int:pk>/edit/', __import__('apps.admin.views.notifications', fromlist=['']).SystemEmailTemplateUpdateView.as_view(), name='notification_template_edit'),

    ])),

    # Auto-scaffolded
    path('brands/popupbanner/', popup_banner.PopupBannerListView.as_view(), name='popupbanner_list'),
    path('brands/popupbanner/create/', popup_banner.PopupBannerCreateView.as_view(), name='popupbanner_create'),
    path('brands/popupbanner/<int:pk>/edit/', popup_banner.PopupBannerUpdateView.as_view(), name='popupbanner_edit'),
    path('brands/coupon/', coupon.CouponListView.as_view(), name='coupon_list'),
    path('brands/coupon/create/', coupon.CouponCreateView.as_view(), name='coupon_create'),
    path('brands/coupon/<int:pk>/edit/', coupon.CouponUpdateView.as_view(), name='coupon_edit'),
    path('brands/newslettersubscriber/', newsletter_subscriber.NewsletterSubscriberListView.as_view(), name='newslettersubscriber_list'),
    path('brands/newslettersubscriber/create/', newsletter_subscriber.NewsletterSubscriberCreateView.as_view(), name='newslettersubscriber_create'),
    path('brands/newslettersubscriber/<int:pk>/edit/', newsletter_subscriber.NewsletterSubscriberUpdateView.as_view(), name='newslettersubscriber_edit'),
    path('brands/emailcampaign/', email_campaign.EmailCampaignListView.as_view(), name='emailcampaign_list'),
    path('brands/emailcampaign/create/', email_campaign.EmailCampaignCreateView.as_view(), name='emailcampaign_create'),
    path('brands/emailcampaign/<int:pk>/edit/', email_campaign.EmailCampaignUpdateView.as_view(), name='emailcampaign_edit'),
    path('brands/apikey/', api_key.APIKeyListView.as_view(), name='apikey_list'),
    path('brands/apikey/create/', api_key.APIKeyCreateView.as_view(), name='apikey_create'),
    path('brands/apikey/<int:pk>/edit/', api_key.APIKeyUpdateView.as_view(), name='apikey_edit'),
    path('brands/webhookendpoint/', webhook_endpoint.WebhookEndpointListView.as_view(), name='webhookendpoint_list'),
    path('brands/webhookendpoint/create/', webhook_endpoint.WebhookEndpointCreateView.as_view(), name='webhookendpoint_create'),
    path('brands/webhookendpoint/<int:pk>/edit/', webhook_endpoint.WebhookEndpointUpdateView.as_view(), name='webhookendpoint_edit'),
    path('brands/apilog/', api_log.APILogListView.as_view(), name='apilog_list'),
    path('brands/apilog/create/', api_log.APILogCreateView.as_view(), name='apilog_create'),
    path('brands/apilog/<int:pk>/edit/', api_log.APILogUpdateView.as_view(), name='apilog_edit'),
    path('shopping/giftcard/', gift_card.GiftCardListView.as_view(), name='giftcard_list'),
    path('shopping/giftcard/create/', gift_card.GiftCardCreateView.as_view(), name='giftcard_create'),
    path('shopping/giftcard/<int:pk>/edit/', gift_card.GiftCardUpdateView.as_view(), name='giftcard_edit'),
    path('shopping/giftcardtransaction/', gift_card_transaction.GiftCardTransactionListView.as_view(), name='giftcardtransaction_list'),
    path('shopping/giftcardtransaction/create/', gift_card_transaction.GiftCardTransactionCreateView.as_view(), name='giftcardtransaction_create'),
    path('shopping/giftcardtransaction/<int:pk>/edit/', gift_card_transaction.GiftCardTransactionUpdateView.as_view(), name='giftcardtransaction_edit'),
    path('catalog/collection/', collection.CollectionListView.as_view(), name='collection_list'),
    path('catalog/collection/create/', collection.CollectionCreateView.as_view(), name='collection_create'),
    path('catalog/collection/<int:pk>/edit/', collection.CollectionUpdateView.as_view(), name='collection_edit'),
    path('catalog/productreview/', product_review.ProductReviewListView.as_view(), name='productreview_list'),
    path('catalog/productreview/create/', product_review.ProductReviewCreateView.as_view(), name='productreview_create'),
    path('catalog/productreview/<int:pk>/edit/', product_review.ProductReviewUpdateView.as_view(), name='productreview_edit'),
    path('orders/deliveryprovince/', delivery_province.DeliveryProvinceListView.as_view(), name='deliveryprovince_list'),
    path('orders/deliveryprovince/create/', delivery_province.DeliveryProvinceCreateView.as_view(), name='deliveryprovince_create'),
    path('orders/deliveryprovince/<int:pk>/edit/', delivery_province.DeliveryProvinceUpdateView.as_view(), name='deliveryprovince_edit'),
    path('orders/deliverydistrict/', delivery_district.DeliveryDistrictListView.as_view(), name='deliverydistrict_list'),
    path('orders/deliverydistrict/create/', delivery_district.DeliveryDistrictCreateView.as_view(), name='deliverydistrict_create'),
    path('orders/deliverydistrict/<int:pk>/edit/', delivery_district.DeliveryDistrictUpdateView.as_view(), name='deliverydistrict_edit'),
    path('orders/deliverycity/', delivery_city.DeliveryCityListView.as_view(), name='deliverycity_list'),
    path('orders/deliverycity/create/', delivery_city.DeliveryCityCreateView.as_view(), name='deliverycity_create'),
    path('orders/deliverycity/<int:pk>/edit/', delivery_city.DeliveryCityUpdateView.as_view(), name='deliverycity_edit'),

    path('login/', AdminLoginView.as_view(), name='login'),
    path('logout/', AdminLogoutView.as_view(), name='logout'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('systemsetting/', SystemSettingListView.as_view(), name='systemsetting_list'),
    path('systemsetting/add/', SystemSettingCreateView.as_view(), name='systemsetting_add'),
    path('systemsetting/<str:pk>/', SystemSettingUpdateView.as_view(), name='systemsetting_edit'),
    path('brandsetting/', BrandSettingListView.as_view(), name='brandsetting_list'),
    path('brandsetting/add/', BrandSettingCreateView.as_view(), name='brandsetting_add'),
    path('brandsetting/<str:pk>/', BrandSettingUpdateView.as_view(), name='brandsetting_edit'),
    path('landingpageconfig/', LandingPageConfigUpdateView.as_view(), name='landingpageconfig_list'),
    path('page/', PageListView.as_view(), name='page_list'),
    path('page/add/', PageCreateView.as_view(), name='page_add'),
    path('page/<str:pk>/', PageUpdateView.as_view(), name='page_edit'),
    path('footersection/', FooterSectionListView.as_view(), name='footersection_list'),
    path('footersection/add/', FooterSectionCreateView.as_view(), name='footersection_add'),
    path('footersection/<str:pk>/', FooterSectionUpdateView.as_view(), name='footersection_edit'),
    path('testimonial/', TestimonialListView.as_view(), name='testimonial_list'),
    path('testimonial/add/', TestimonialCreateView.as_view(), name='testimonial_add'),
    path('testimonial/<str:pk>/', TestimonialUpdateView.as_view(), name='testimonial_edit'),
    path('blogpost/', BlogPostListView.as_view(), name='blogpost_list'),
    path('blogpost/add/', BlogPostCreateView.as_view(), name='blogpost_add'),
    path('blogpost/<str:pk>/', BlogPostUpdateView.as_view(), name='blogpost_edit'),
    path('blogpost/<str:pk>/delete/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
    path('contactmessage/', ContactMessageListView.as_view(), name='contactmessage_list'),
    path('contactmessage/<str:pk>/', ContactMessageDetailView.as_view(), name='contactmessage_edit'),
    path('contactmessage/<str:pk>/delete/', ContactMessageDeleteView.as_view(), name='contactmessage_delete'),
    # Landing Page Features
    path('landingpagefeature/', LandingPageFeatureListView.as_view(), name='landingpagefeature_list'),
    path('landingpagefeature/add/', LandingPageFeatureCreateView.as_view(), name='landingpagefeature_add'),
    path('landingpagefeature/<str:pk>/', LandingPageFeatureUpdateView.as_view(), name='landingpagefeature_edit'),
    path('landingpagefeature/<str:pk>/delete/', LandingPageFeatureDeleteView.as_view(), name='landingpagefeature_delete'),

    # FAQs
    path('faqs/', FAQItemListView.as_view(), name='faqitem_list'),
    path('faqs/create/', FAQItemCreateView.as_view(), name='faqitem_create'),
    path('faqs/<int:pk>/edit/', FAQItemUpdateView.as_view(), name='faqitem_update'),
    path('faqs/<int:pk>/delete/', FAQItemDeleteView.as_view(), name='faqitem_delete'),

    # Metrics
    path('metrics/', MetricListView.as_view(), name='metric_list'),
    path('metrics/create/', MetricCreateView.as_view(), name='metric_create'),
    path('metrics/<int:pk>/edit/', MetricUpdateView.as_view(), name='metric_update'),
    path('metrics/<int:pk>/delete/', MetricDeleteView.as_view(), name='metric_delete'),

    # Integration Platforms
    path('integrations/', IntegrationPlatformListView.as_view(), name='integrationplatform_list'),
    path('integrations/create/', IntegrationPlatformCreateView.as_view(), name='integrationplatform_create'),
    path('integrations/<int:pk>/edit/', IntegrationPlatformUpdateView.as_view(), name='integrationplatform_update'),
    path('integrations/<int:pk>/delete/', IntegrationPlatformDeleteView.as_view(), name='integrationplatform_delete'),
    path('featureflag/', FeatureFlagListView.as_view(), name='featureflag_list'),
    path('featureflag/add/', FeatureFlagCreateView.as_view(), name='featureflag_add'),
    path('featureflag/<str:pk>/', FeatureFlagUpdateView.as_view(), name='featureflag_edit'),
    path('platformintegration/', PlatformIntegrationListView.as_view(), name='platformintegration_list'),
    path('platformintegration/add/', PlatformIntegrationCreateView.as_view(), name='platformintegration_add'),
    path('platformintegration/<str:pk>/', PlatformIntegrationUpdateView.as_view(), name='platformintegration_edit'),
    path('globalsettings/', GlobalSettingsUpdateView.as_view(), name='globalsettings_edit'),
    path('globalsettings/test-email/', TestEmailView.as_view(), name='globalsettings_test_email'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/add/', UserCreateView.as_view(), name='user_add'),
    path('users/<str:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('roles/', GroupListView.as_view(), name='group_list'),
    path('roles/add/', GroupCreateView.as_view(), name='group_add'),
    path('roles/<str:pk>/', GroupUpdateView.as_view(), name='group_edit'),
    # VTO Features
    path('vto/queue/', VTOQueueDashboardView.as_view(), name='vto_queue'),
    path('vto/qa-moderation/', QAModerationView.as_view(), name='qa_moderation'),
    path('vto/qa-moderation/<int:pk>/<str:action>/', QAModerationActionView.as_view(), name='qa_moderation_action'),
    path('consumerprofile/', ConsumerProfileListView.as_view(), name='consumerprofile_list'),
    path('consumerprofile/add/', ConsumerProfileCreateView.as_view(), name='consumerprofile_add'),
    path('consumerprofile/<str:pk>/', ConsumerProfileUpdateView.as_view(), name='consumerprofile_edit'),
    path('userphotoprofile/', UserPhotoProfileListView.as_view(), name='userphotoprofile_list'),
    path('userphotoprofile/add/', UserPhotoProfileCreateView.as_view(), name='userphotoprofile_add'),
    path('userphotoprofile/<str:pk>/', UserPhotoProfileUpdateView.as_view(), name='userphotoprofile_edit'),
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/add/', BrandCreateView.as_view(), name='brand_add'),
    path('brands/<str:pk>/', BrandUpdateView.as_view(), name='brand_edit'),
    path('brands/<str:pk>/impersonate/', ImpersonateBrandView.as_view(), name='brand_impersonate'),
    path('impersonate/revert/', ImpersonateRevertView.as_view(), name='impersonate_revert'),
    path('brandintegration/', BrandIntegrationListView.as_view(), name='brandintegration_list'),
    path('brandintegration/add/', BrandIntegrationCreateView.as_view(), name='brandintegration_add'),
    path('brandintegration/<str:pk>/', BrandIntegrationUpdateView.as_view(), name='brandintegration_edit'),
    path('storetheme/', StoreThemeListView.as_view(), name='storetheme_list'),
    path('storetheme/add/', StoreThemeCreateView.as_view(), name='storetheme_add'),
    path('storetheme/<str:pk>/', StoreThemeUpdateView.as_view(), name='storetheme_edit'),
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product/<str:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('productvariant/', ProductVariantListView.as_view(), name='productvariant_list'),
    path('productvariant/add/', ProductVariantCreateView.as_view(), name='productvariant_add'),
    path('productvariant/<str:pk>/', ProductVariantUpdateView.as_view(), name='productvariant_edit'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_add'),
    path('category/<str:pk>/', CategoryUpdateView.as_view(), name='category_edit'),
    path('color/', ColorListView.as_view(), name='color_list'),
    path('color/add/', ColorCreateView.as_view(), name='color_add'),
    path('color/<str:pk>/', ColorUpdateView.as_view(), name='color_edit'),
    path('size/', SizeListView.as_view(), name='size_list'),
    path('size/add/', SizeCreateView.as_view(), name='size_add'),
    path('size/<str:pk>/', SizeUpdateView.as_view(), name='size_edit'),
    path('sizechart/', SizeChartListView.as_view(), name='sizechart_list'),
    path('sizechart/add/', SizeChartCreateView.as_view(), name='sizechart_add'),
    path('sizechart/<str:pk>/', SizeChartUpdateView.as_view(), name='sizechart_edit'),
    path('styletag/', StyleTagListView.as_view(), name='styletag_list'),
    path('styletag/add/', StyleTagCreateView.as_view(), name='styletag_add'),
    path('styletag/<str:pk>/', StyleTagUpdateView.as_view(), name='styletag_edit'),
    path('producttype/', ProductTypeListView.as_view(), name='producttype_list'),
    path('producttype/add/', ProductTypeCreateView.as_view(), name='producttype_add'),
    path('producttype/<str:pk>/', ProductTypeUpdateView.as_view(), name='producttype_edit'),
    path('productaiprofile/', ProductAIProfileListView.as_view(), name='productaiprofile_list'),
    path('productaiprofile/add/', ProductAIProfileCreateView.as_view(), name='productaiprofile_add'),
    path('productaiprofile/<str:pk>/', ProductAIProfileUpdateView.as_view(), name='productaiprofile_edit'),
    path('location/', LocationListView.as_view(), name='location_list'),
    path('location/add/', LocationCreateView.as_view(), name='location_add'),
    path('location/<str:pk>/', LocationUpdateView.as_view(), name='location_edit'),
    path('stocklevel/', StockLevelListView.as_view(), name='stocklevel_list'),
    path('stocklevel/add/', StockLevelCreateView.as_view(), name='stocklevel_add'),
    path('stocklevel/<str:pk>/', StockLevelUpdateView.as_view(), name='stocklevel_edit'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/add/', OrderCreateView.as_view(), name='order_add'),
    path('orders/<str:pk>/', OrderUpdateView.as_view(), name='order_edit'),
    path('cart/', CartListView.as_view(), name='cart_list'),
    path('cart/add/', CartCreateView.as_view(), name='cart_add'),
    path('cart/<str:pk>/', CartUpdateView.as_view(), name='cart_edit'),
    path('shippingzone/', ShippingZoneListView.as_view(), name='shippingzone_list'),
    path('shippingzone/add/', ShippingZoneCreateView.as_view(), name='shippingzone_add'),
    path('shippingzone/<str:pk>/', ShippingZoneUpdateView.as_view(), name='shippingzone_edit'),
    path('virtualtryon/', VirtualTryOnListView.as_view(), name='virtualtryon_list'),
    path('virtualtryon/add/', VirtualTryOnCreateView.as_view(), name='virtualtryon_add'),
    path('virtualtryon/<str:pk>/', VirtualTryOnDetailView.as_view(), name='virtualtryon_detail'),
    path('virtualtryon/<str:pk>/edit/', VirtualTryOnDetailView.as_view(), name='virtualtryon_edit'), # Alias for old link
    path('fitpassport/', FitPassportListView.as_view(), name='fitpassport_list'),
    path('fitpassport/add/', FitPassportCreateView.as_view(), name='fitpassport_add'),
    path('fitpassport/<str:pk>/', FitPassportUpdateView.as_view(), name='fitpassport_edit'),
    path('vtoproduct/', VTOProductListView.as_view(), name='vtoproduct_list'),
    path('vtoproduct/add/', VTOProductCreateView.as_view(), name='vtoproduct_add'),
    path('vtoproduct/<str:pk>/', VTOProductUpdateView.as_view(), name='vtoproduct_edit'),
    path('vtoproductassets/', VTOProductAssetsListView.as_view(), name='vtoproductassets_list'),
    path('vtoproductassets/add/', VTOProductAssetsCreateView.as_view(), name='vtoproductassets_add'),
    path('vtoproductassets/<str:pk>/', VTOProductAssetsUpdateView.as_view(), name='vtoproductassets_edit'),
    path('virtualwardrobelook/', VirtualWardrobeLookListView.as_view(), name='virtualwardrobelook_list'),
    path('virtualwardrobelook/add/', VirtualWardrobeLookCreateView.as_view(), name='virtualwardrobelook_add'),
    path('virtualwardrobelook/<str:pk>/', VirtualWardrobeLookUpdateView.as_view(), name='virtualwardrobelook_edit'),
    path('vtosession/', VTOSessionListView.as_view(), name='vtosession_list'),
    path('vtosession/add/', VTOSessionCreateView.as_view(), name='vtosession_add'),
    path('vtosession/<str:pk>/', VTOSessionDetailView.as_view(), name='vtosession_detail'),
    path('vtosession/<str:pk>/edit/', VTOSessionDetailView.as_view(), name='vtosession_edit'), # Alias for old link
    path('vtophotovault/', VTOPhotoVaultListView.as_view(), name='vtophotovault_list'),
    path('vtophotovault/add/', VTOPhotoVaultCreateView.as_view(), name='vtophotovault_add'),
    path('vtophotovault/<str:pk>/', VTOPhotoVaultUpdateView.as_view(), name='vtophotovault_edit'),
    path('sizerecommendation/', SizeRecommendationListView.as_view(), name='sizerecommendation_list'),
    path('sizerecommendation/add/', SizeRecommendationCreateView.as_view(), name='sizerecommendation_add'),
    path('sizerecommendation/<str:pk>/', SizeRecommendationUpdateView.as_view(), name='sizerecommendation_edit'),
    path('brandsubscription/', BrandSubscriptionListView.as_view(), name='brandsubscription_list'),
    path('brandsubscription/add/', BrandSubscriptionCreateView.as_view(), name='brandsubscription_add'),
    path('brandsubscription/<str:pk>/', BrandSubscriptionUpdateView.as_view(), name='brandsubscription_edit'),
    path('subscriptionplan/', SubscriptionPlanListView.as_view(), name='subscriptionplan_list'),
    path('subscriptionplan/add/', SubscriptionPlanCreateView.as_view(), name='subscriptionplan_add'),
    path('subscriptionplan/<str:pk>/', SubscriptionPlanUpdateView.as_view(), name='subscriptionplan_edit'),
    path('audit-logs/', AuditLogListView.as_view(), name='audit_log_list'),
    path('email-logs/', EmailLogListView.as_view(), name='email_log_list'),

    # Brand Staff
    path('brandstaff/', BrandStaffListView.as_view(), name='brandstaff_list'),
    path('brandstaff/<str:pk>/', BrandStaffUpdateView.as_view(), name='brandstaff_edit'),

    # Returns
    path('returnrequest/', ReturnRequestListView.as_view(), name='returnrequest_list'),
    path('returnrequest/<str:pk>/', ReturnRequestUpdateView.as_view(), name='returnrequest_edit'),

]

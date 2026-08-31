from django.urls import path
from . import views
from . import marketing_views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/settings/', views.brand_settings_view, name='brand_settings'),
    path('dashboard/settings/team/', views.team_management_view, name='team_management'),
    path('store/<slug:slug>/', views.storefront_view, name='storefront'),
    path('store/<slug:slug>/shop/', views.storefront_shop_view, name='storefront_shop'),
    path('store/<slug:slug>/collections/', views.storefront_collections_view, name='storefront_collections'),
    path('store/<slug:slug>/categories/', views.storefront_categories_view, name='storefront_categories'),
    path('store/<slug:slug>/product/<slug:product_slug>/', views.store_product_detail_view, name='store_product_detail'),
    path('store/<slug:slug>/account/', views.storefront_account_view, name='storefront_account'),
    path('store/<slug:slug>/customer-login/', views.storefront_login, name='storefront_login'),
    path('store/<slug:slug>/customer-register/', views.storefront_register, name='storefront_register'),
    path('store/<slug:slug>/customer-logout/', views.storefront_logout, name='storefront_logout'),
    path('dashboard/finance/', views.finance_view, name='finance'),
    path('dashboard/reports/', views.reports_view, name='reports'),
    path('dashboard/search/', views.global_search_view, name='global_search'),
    path('dashboard/media/', views.media_gallery_view, name='media_gallery'),
    path('dashboard/addons/', views.addons_view, name='addons'),
    path('dashboard/developer/', views.developer_api_view, name='developer_api'),
    path('dashboard/themes/', views.theme_gallery_view, name='theme_gallery'),
    path('dashboard/designer/', views.website_designer_view, name='website_designer'),
    path('dashboard/notifications/', views.notifications_view, name='notifications'),
    path('dashboard/notifications/mark-read/', views.mark_notifications_read, name='mark_notifications_read'),
    
    path('dashboard/marketing/', marketing_views.marketing_dashboard_view, name='marketing_dashboard'),
    path('dashboard/marketing/popups/', marketing_views.popup_list_view, name='popup_list'),
    path('dashboard/marketing/coupons/', marketing_views.coupon_list_view, name='coupon_list'),
    path('dashboard/marketing/popup/create/', marketing_views.popup_create_view, name='popup_create'),
    path('dashboard/marketing/popup/<int:popup_id>/edit/', marketing_views.popup_edit_view, name='popup_edit'),
    path('dashboard/marketing/popup/<int:popup_id>/delete/', marketing_views.popup_delete_view, name='popup_delete'),
    
    path('dashboard/marketing/coupon/create/', marketing_views.coupon_create_view, name='coupon_create'),
    path('dashboard/marketing/coupon/<int:coupon_id>/edit/', marketing_views.coupon_edit_view, name='coupon_edit'),
    path('dashboard/marketing/coupon/<int:coupon_id>/delete/', marketing_views.coupon_delete_view, name='coupon_delete'),
    
    path('dashboard/marketing/subscribers/', marketing_views.subscriber_list_view, name='subscriber_list'),
    path('dashboard/marketing/subscriber/<int:subscriber_id>/delete/', marketing_views.subscriber_delete_view, name='subscriber_delete'),
    
    path('dashboard/marketing/contact-messages/', marketing_views.contact_messages_list_view, name='contact_messages_list'),
    path('dashboard/marketing/contact-message/<int:message_id>/delete/', marketing_views.contact_message_delete_view, name='contact_message_delete'),
    path('dashboard/marketing/contact-message/<int:message_id>/toggle-read/', marketing_views.contact_message_toggle_read_view, name='contact_message_toggle_read'),
    path('dashboard/marketing/contact-message/<int:message_id>/reply/', marketing_views.contact_message_reply_view, name='contact_message_reply'),
    path('dashboard/marketing/contact-messages/mark-all-read/', marketing_views.contact_message_mark_all_read_view, name='contact_message_mark_all_read'),
    
    path('dashboard/marketing/campaigns/', marketing_views.campaign_list_view, name='campaign_list'),
    path('dashboard/marketing/campaign/create/', marketing_views.campaign_create_view, name='campaign_create'),
    path('dashboard/marketing/campaign/<int:campaign_id>/edit/', marketing_views.campaign_edit_view, name='campaign_edit'),
    path('dashboard/marketing/campaign/<int:campaign_id>/delete/', marketing_views.campaign_delete_view, name='campaign_delete'),
    path('dashboard/marketing/campaign/<int:campaign_id>/send/', marketing_views.campaign_send_view, name='campaign_send'),
    
    path('dashboard/marketing/blogs/', marketing_views.dashboard_blog_list_view, name='dashboard_blog_list'),
    path('dashboard/marketing/blog/create/', marketing_views.dashboard_blog_create_view, name='dashboard_blog_create'),
    path('dashboard/marketing/blog/<int:post_id>/edit/', marketing_views.dashboard_blog_edit_view, name='dashboard_blog_edit'),
    path('dashboard/marketing/blog/<int:post_id>/delete/', marketing_views.dashboard_blog_delete_view, name='dashboard_blog_delete'),
    
    path('store/<slug:brand_slug>/subscribe/', marketing_views.newsletter_subscribe_api, name='newsletter_subscribe'),
    path('store/<slug:brand_slug>/contact-submit/', marketing_views.contact_submit_api, name='contact_submit'),
    
    path('store/<slug:slug>/journal/', views.storefront_blog_list_view, name='storefront_blog_list'),
    path('store/<slug:slug>/journal/<slug:post_slug>/', views.storefront_blog_detail_view, name='storefront_blog_detail'),
]

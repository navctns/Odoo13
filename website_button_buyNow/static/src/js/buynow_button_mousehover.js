odoo.define('website_button_buyNow.buynow', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var core = require('web.core');
var _t = core._t;

var timeout;

//publicWidget.registry.BuyNowButton = publicWidget.Widget.extend({
//    selector: '#top_menu a[href$="/shop/cart"]',
//card oe_product_cart  action="/shop/cart/update"

//publicWidget.registry.WebsiteSale.include({ //this will also work//
publicWidget.registry.BuyNowButton= publicWidget.registry.WebsiteSale.extend({

/////////Method 1/////////////////
//    selector: '.card oe_product_cart',
//    events: {
//        'mouseenter .o_wsale_product_grid_wrapper': 'buynowButton',
//        'mouseleave .o_wsale_product_grid_wrapper': '_onMouseLeave',
////        'click': '_onClick',
//    },
    //////Method 1 end////////////////
    ////Method 2/////////////
    //change event selector
//            card-body p-1 oe_product_image
//        events: {
//        'mouseenter .card-body p-1 oe_product_image': 'buynowButton',
//        'mouseleave .card-body p-1 oe_product_image': '_onMouseLeave',
////        'click': '_onClick',
//    },
     //change event selector//////
     /////Method 2 end//////////
     /////////method 3////////////////
     events: {
        'mouseenter .oe_product': 'buynowButtonShow',
        'mouseleave .oe_product': 'buynowButtonHide',
//        'click': '_onClick',
   },
     ////////method 3 end////////////
//     start: function() {
//            console.log("pet store home page loaded");
//        },

//    console.log('mousehover button script');
//    this.$(".buynow").hide();

//        $(".card oe_product_cart").mouseover(function(){
//                $(".buynow").show();
//            });

//     _onMouseEnter: function (ev) {
//        var self = this;
////        this.$("#buynow").hide()
//          this.trigger(this.$("#buynow").style.display='inline');
//          this.$("#buynow").set('display','inline');
////        if ($(ev.currentTarget).attr('class') == 'card oe_product_cart'){
////            this.$(".buynow").show();
////            this.trigger('#products_item_buynow1', true);
////            style="display: none;"
//            alert();
//            console.log('enter')
////        }
//
//        },

        buynowButtonShow: function (ev) {
        var self = this;
//        this.$("#buynow").hide()
//          this.trigger(this.$("#buynow").style.display='inline');
//          this.$("#buynow").set('display','inline');
//            this.$("#buynow").style.display='inline';
//        if ($(ev.currentTarget).attr('class') == 'card oe_product_cart'){
//            this.$(".buynow").show();
//            this.trigger('#products_item_buynow1', true);
//            style="display: none;"

//            this.$el.find("#buynow").css('display':'inline');
//        timeout = setTimeout(function (){
            setTimeout(function (){
//            this.$("#buy_now").css('display','inline');//Previous ver
//            alert();
//            $(ev.currentTarget).find('#buy_now').css('display','inline');
            $(ev.currentTarget).find('#buynow').css('display','inline');
            console.log('enter')
//        }
         }, 300);
        },

        buynowButtonHide: function (ev) {
        setTimeout(function (){
            var self = this;
    //        if ($(ev.currentTarget).attr('class') != 'card oe_product_cart'){
    //            this.$(".buynow").hide();
    //        }
    //            this.$("#buy_now").css('display','none');//Prev ver
//                  $(ev.currentTarget).find('#buy_now').css('display','none');
                    $(ev.currentTarget).find('#buynow').css('display','none');

            },300);
        },


//          ////Sample
//            * @param {MouseEvent} event
//     * @private
//     */
//    _onMouseOver: function (event) {
//        clearTimeout(this.hoverTimer);
//        this.$('.o_priority_star').removeClass('fa-star-o').addClass('fa-star');
//        });
        ////sample

//        _onMouseEnter
//        clearTimeout(timeout);
//        $(this.selector).not(ev.currentTarget).buynow('hide');
//        timeout = setTimeout(function () {
//            if (!self.$el.is(':hover') || $('.mycart-popover:visible').length) {
//                return;
//            }
//            self._popoverRPC = $.get("/shop/cart", {
//                type: 'popover',
//            }).then(function (data) {
//                self.$el.data("bs.popover").config.content = data;
//                self.$el.popover("show");
//                $('.popover').on('mouseleave', function () {
//                    self.$el.trigger('mouseleave');
//                });
//            });
//        }, 300);
//    },

});

});
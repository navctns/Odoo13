odoo.define('website_button_buyNow.buynow', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var core = require('web.core');
var _t = core._t;

var timeout;

publicWidget.registry.BuyNowButton = publicWidget.Widget.extend({
//    selector: '#top_menu a[href$="/shop/cart"]',
//card oe_product_cart  action="/shop/cart/update"
    selector: '.card oe_product_cart',
    events: {
        'mouseenter': '_onMouseEnter',
        'mouseleave': '_onMouseLeave',
//        'click': '_onClick',
    },

    this.$(".buynow").hide();

//     _onMouseEnter: function (ev) {
//        var self = this;
//        if ($(ev.currentTarget).attr('class') === 'card oe_product_cart'){
//            this.$(".buynow").show();
//            this.trigger('#products_item_buynow1', true);
//        }
//        },
//
//        _onMouseLeave: function (ev) {
//        var self = this;
//        if ($(ev.currentTarget).attr('class') !== 'card oe_product_cart'){
//            this.$(".buynow").hide();
//        }
//        },
//          ////Sample
//            * @param {MouseEvent} event
//     * @private
//     */
//    _onMouseOver: function (event) {
//        clearTimeout(this.hoverTimer);
//        this.$('.o_priority_star').removeClass('fa-star-o').addClass('fa-star');
//        });
        ////sample

        _onMouseEnter
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
    },



});
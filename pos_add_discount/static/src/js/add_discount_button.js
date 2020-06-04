//alert("Loaded")
//console.log("loaded again")

odoo.define('pos_add_discount.pos_add_discount', function (require) {
"use strict";

var core = require('web.core');
var screens = require('point_of_sale.screens');
var models = require('point_of_sale.models');

console.log("screens", screens)

//var AddDiscountButton = screens.ActionButtonWidget.include({
var AddDiscountButton = screens.NumpadWidget.extend({
    template: 'AddDiscountButton',

    button_click: function(){
//    var self = this;
//    this.discount_button();
//    },
//
//    discount_button(){
//    var order = this.pos.get_order();
////    order.remove_orderline(order.get_selected_orderline())
//    console.log("order",order);
//    },
//     var order = this.pos.get_order();
     console.log("Test order");
       }
    });
    screens.define_action_button({'name': 'pos_add_discount','widget': AddDiscountButton,});
//    screens.define_action_button({
//    'name': 'pos_add_discount',
//    'widget': AddDiscountButton,
//    'condition': function(){
//        return this.pos.config.module_pos_add_discount;
//    },

 return {
    AddDiscountButton: DiscountButton,
}

});




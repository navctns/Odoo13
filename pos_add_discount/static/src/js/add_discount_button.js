//alert("Loaded")
//console.log("loaded again")

odoo.define('pos_add_discount.discount', function (require) {
"use strict";

var core = require('web.core');
var screens = require('point_of_sale.screens');
var models = require('point_of_sale.models');

console.log("screens", screens)
///Order line model

var _super_orderline = models.Orderline.prototype;

models.Orderline = models.Orderline.extend({
    initialize: function(attr, options) {
        _super_orderline.initialize.call(this,attr,options);
        this.discount = this.discount || "";
    },
    set_discount: function(discount){
        this.discount = discount;
        this.trigger('change',this);
    },
    get_discount: function(discount){
        return this.discount;
    },
     can_be_merged_with: function(orderline) {
        if (orderline.get_discount() !== this.get_discount()) {
            return false;
        } else {
            return _super_orderline.can_be_merged_with.apply(this,arguments);
        }
    },
    clone: function(){
        var orderline = _super_orderline.clone.call(this);
        orderline.discount = this.discount;
        return orderline;
    },
    export_as_JSON: function(){
        var json = _super_orderline.export_as_JSON.call(this);
        json.discount = this.discount;
        return json;
    },
    init_from_JSON: function(json){
        _super_orderline.init_from_JSON.apply(this,arguments);
        this.discount = json.discount;
    },
});
//Order line model

var AddDiscountButton = screens.ActionButtonWidget.extend({
//var AddDiscountButton = screens.NumpadWidget.extend({
    template: 'AddDiscountButton',
//------------------------------
    button_click: function(){
//        var self = this;
          var line = this.pos.get_order().get_selected_orderline();
          if (line){
    //        this.gui.show_popup('textarea',{
            this.gui.show_popup('number',{
                    'title': ('Add Discount'),
                    'value': line.get_discount(),
                    'body': 'Opening popup after clicking on the button',
                    confirm: function(discount) {
//                    line.set_note(discount);
//                      discount = Math.round(Math.max(0,Math.min(100,discount)));
//                      self.apply_discount(discount);
                        var order    = this.pos.get_order();
                        var product  = this.pos.db.get_product_by_id(this.pos.config.discount_product_id[0]);
                        var price_without_tax = line.get_price_without_tax()//product_price
                        var base_to_discount = order.get_total_without_tax();
                        var discount_calc = - discount / 100.0 * base_to_discount;
                        console.log('total without tax :', base_to_discount)
                        console.log('discount calc :', discount_calc)
//                        line.set_amount(base_to_discount+discount_calc)
                        var amt_change = 0
                        var discount_type = this.pos.config.discount_type_perc_amount;
                          if (discount_type=='perc'){
//                          discount = Math.round(Math.max(0,Math.min(100,discount)));
                          line.set_discount(discount)
                          line.price_manually_set = true;
//                          this.pos.config.discount_perc_amount = discount_calc
                          }else if (discount_type=='amount'){
//                            line.price = 10;
                              console.log('product_unit_price', line.get_unit_price())
                              console.log('product price',line.get_price_without_tax())
                              var unit_price = line.get_unit_price();
//                              var price = line.price_unit
//                              console.log('price',price)
                              var updated_price = unit_price-discount;//add discount for the product
                              var current_price = price_without_tax//defined outside
//                              var updated_price = current_price-discount;//to apply discount for subtotal of the orderline/order
                              line.set_unit_price(updated_price)
                              line.price_manually_set = true;
//                              base_to_discount = 10
//                               amt_change = 1//flag that price changed with discount can be used to limit setting discount only once
                          }
                        console.log('orderline',line)
                        console.log('subtotal',order.price_subtotal)
                         console.log('amount',line.amount)
                          console.log('amount_total',line.amount_total)
                        },
                    });
          }
//                console.log("button click");
        var order = this.pos.get_order()
        console.log("button click discount_type :", this.pos.config.discount_type_perc_amount);
//                return;
         console.log("order discount",line.get_discount());
         console.log("order",order);
    },

    apply_discount: function(pc){
        var order    = this.pos.get_order();
        var product  = this.pos.db.get_product_by_id(this.pos.config.discount_product_id[0]);

        var base_to_discount = order.get_total_without_tax();
        var discount = - pc / 100.0 * base_to_discount;
        console.log('total without tax :', base_to_discount)
        return;
//        if( discount < 0 ){
////                order.add_product(product, {
////                    price: discount,
////                    lst_price: discount,
////                    extras: {
////                        price_manually_set: true,
////                    },
////                });
//                  order.get_selected_orderline().set_discount(discount);
//            }
       },
    });
//------------------------------
//    var self = this;
//    this.discount_button();
//    },
//
//    discount_button(){
//    var order = this.pos.get_order();
//    order.remove_orderline(order.get_selected_orderline())
//    console.log("order",order);

//     var order = this.pos.get_order();

//------second---------
//    button_click: function () {
//  this.gui.show_popup('confirm', {
//    'title': 'Popup',
//    'body': 'Opening popup after clicking on the button',
//    });
//    }
//  });
//
//screens.define_action_button({
//  'name': 'add_discount_button',
//  'widget': AddDiscountButton,
////  'condition': function () {
////  return this.pos.config.add_discount_button;
////    },
//     });

  screens.define_action_button({'name': 'pos_add_discount','widget': AddDiscountButton,});
  return AddDiscountButton;
   });
//------second---------

    //-------------------------
//    screens.define_action_button({
//        'name': 'discount_button',
//        'widget': AddDiscountButton,
    //----------------------------
//        'condition': function(){
//            return this.pos.config.discount_perc
//        },

//    screens.define_action_button({
//    'name': 'pos_add_discount',
//    'widget': AddDiscountButton,
//    'condition': function(){
//        return this.pos.config.module_pos_add_discount;
//    },

// return {
//    AddDiscountButton: AddDiscountButton,
//}
//-------------------------
//    return AddDiscountButton;






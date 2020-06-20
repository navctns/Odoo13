odoo.define('pos_add_discount.pos_discount', function (require) {
"use strict";

var core = require('web.core');
var screens = require('point_of_sale.screens');
var models = require('point_of_sale.models');

var _t = core._t;

var existing_models = models.PosModel.prototype.models;
var product_index = _.findIndex(existing_models, function (model) {
    return model.model === "product.product";
});
var product_model = existing_models[product_index];


models.load_models([{
  model:  product_model.model,
  fields: product_model.fields,
  order:  product_model.order,
  domain: function(self) {return [['id', '=', self.config.discount_product_add[0]]];},
  context: product_model.context,
  loaded: product_model.loaded,
}]);


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

var AddDiscountButton = screens.ActionButtonWidget.extend({
    template: 'AddDiscountButton',
    //sample code/////
//    button_click: function(){
//        var self = this;
//        this.gui.show_popup('number',{
//            'title': _t('Add Discount'),
//                'value': this.pos.config.discount_pc,
//            'confirm': function(val) {
//                val = Math.round(Math.max(0,Math.min(100,val)));
//                self.apply_discount(val);
//            },
//        });
//    },
 //sample code/////
    button_click: function(){
//        var self = this;

          var line = this.pos.get_order().get_selected_orderline();
//          if (line){

    //        this.gui.show_popup('textarea',{
            this.gui.show_popup('number',{
                    'title': ('Add Discount'),
                    'value': line.get_discount(),
                    'body': 'Opening popup after clicking on the button',
                    confirm: function(discount) {
                        var value = this.$('#number-input').val();
                        console.log('input value,discount',value,discount)
//                    line.set_note(discount);
//                      discount = Math.round(Math.max(0,Math.min(100,discount)));
//                      self.apply_discount(discount);
                        var order    = this.pos.get_order();
                        var product  = this.pos.db.get_product_by_id(this.pos.config.discount_product_add[0]);
//                        var price_without_tax = line.get_price_without_tax()//product_price
                        var base_to_discount = order.get_total_without_tax();
                        var discount_calc = - discount / 100.0 * base_to_discount;
                        console.log('total without tax :', base_to_discount)
                        console.log('discount calc :', discount_calc)
//                        line.set_amount(base_to_discount+discount_calc)
                        var amt_change = 0

                        var order    = this.pos.get_order();
                            var lines    = order.get_orderlines();
                            var product  = this.pos.db.get_product_by_id(this.pos.config.discount_product_add[0]);
                            if (product === undefined) {
                                this.gui.show_popup('error', {
                                    title : _t("No discount product found"),
                                    body  : _t("The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
                                });
                                }

                                                               // Add discount
                                    // We add the price as manually set to avoid recomputation when changing customer.
                                    var base_to_discount = order.get_total_without_tax();
                                    ///avoiding the total with tax
//                                    if (product.taxes_id.length){
//                                        var first_tax = this.pos.taxes_by_id[product.taxes_id[0]];
//                                        if (first_tax.price_include) {
//                                            base_to_discount = order.get_total_with_tax();
//                                        }
//                                    }
                                      ///avoiding the total with tax
                        var discount_type = this.pos.config.discount_type_perc_amount;
                          if (discount_type=='perc'){
//                          discount = Math.round(Math.max(0,Math.min(100,discount)));
//                          line.set_discount(discount)///comment for now
//                              line.price_manually_set = true;
//                          this.pos.config.discount_perc_amount = discount_calc
//                           self.apply_discount(value);
                            ///Moved out
//                            var order    = this.pos.get_order();
//                            var lines    = order.get_orderlines();
//                            var product  = this.pos.db.get_product_by_id(this.pos.config.discount_product_add[0]);
//                            if (product === undefined) {
//                                this.gui.show_popup('error', {
//                                    title : _t("No discount product found"),
//                                    body  : _t("The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
//                                });
//                                }
//
//                                                               // Add discount
//                                    // We add the price as manually set to avoid recomputation when changing customer.
//                                    var base_to_discount = order.get_total_without_tax();
//                                    if (product.taxes_id.length){
//                                        var first_tax = this.pos.taxes_by_id[product.taxes_id[0]];
//                                        if (first_tax.price_include) {
//                                            base_to_discount = order.get_total_with_tax();
//                                        }
//                                    }
                                    ////// moved out////////////////////
                                    var discount_amt = - discount / 100.0 * base_to_discount;
//                                        ////on sample code//////////
//
                                    if( discount_amt < 0 ){
                                        order.add_product(product, {
                                            price: discount_amt,
                                            lst_price: discount_amt,
                                            extras: {
                                                price_manually_set: true,
                                            },
                                        });
                                    }

                          }else if (discount_type=='amount'){
//                            line.price = 10;
//                              console.log('product_unit_price', line.get_unit_price())
//                              console.log('product price',line.get_price_without_tax())
//                              var unit_price = line.get_unit_price();
//                              var price = line.price_unit
//                              console.log('price',price)
//                              var updated_price = unit_price-discount;//add discount for the product
//                              var current_price = price_without_tax//defined outside
//                              var updated_price = current_price-discount;//to apply discount for subtotal of the orderline/order
                                //#  line.set_unit_price(updated_price)
                                //#  line.price_manually_set = true;
//                              base_to_discount = 10
//                               amt_change = 1//flag that price changed with discount can be used to limit setting discount only once
                                var discount_amt = - discount;
//                                        ////on sample code//////////
//
                                    if( discount_amt < 0 ){
                                        order.add_product(product, {
                                            price: discount_amt,
                                            lst_price: discount_amt,
                                            extras: {
                                                price_manually_set: true,
                                            },
                                        });
                                    }
                          }
//                        console.log('orderline',line)
//                        console.log('subtotal',order.price_subtotal)
//                         console.log('amount',line.amount)
//                          console.log('amount_total',line.amount_total)
                        },
                    });
//          }
//                console.log("button click");
        var order = this.pos.get_order()
        console.log("button click discount_type :", this.pos.config.discount_type_perc_amount);
//                return;
//         console.log("order discount",line.get_discount());
         console.log("order",order);
    },



    apply_discount: function(pc) {
        var order    = this.pos.get_order();
        var lines    = order.get_orderlines();
        var product  = this.pos.db.get_product_by_id(this.pos.config.discount_product_add[0]);
        if (product === undefined) {
            this.gui.show_popup('error', {
                title : _t("No discount product found"),
                body  : _t("The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
            });
            return;
        }

        // Remove existing discounts
        var i = 0;
        while ( i < lines.length ) {
            if (lines[i].get_product() === product) {
                order.remove_orderline(lines[i]);
            } else {
                i++;
            }
        }


            ////on sample code//////////
        // Add discount
        // We add the price as manually set to avoid recomputation when changing customer.
//        var base_to_discount = order.get_total_without_tax();
//        if (product.taxes_id.length){
//            var first_tax = this.pos.taxes_by_id[product.taxes_id[0]];
//            if (first_tax.price_include) {
//                base_to_discount = order.get_total_with_tax();
//            }
//        }
//        var discount = - pc / 100.0 * base_to_discount;
            ////on sample code//////////

        if( discount < 0 ){
            order.add_product(product, {
                price: discount,
                lst_price: discount,
                extras: {
                    price_manually_set: true,
                },
            });
        }
    },
});

screens.define_action_button({
    'name': 'discount',
    'widget': AddDiscountButton,
    'condition': function(){
//        return this.pos.config.module_pos_discount && this.pos.config.discount_product_id;
        return this.pos.config.discount_type_perc_amount && this.pos.config.discount_product_add;

    },
});
//screens.define_action_button({'name': 'pos_add_discount','widget': AddDiscountButton,});
return {
    AddDiscountButton: AddDiscountButton,
}

});

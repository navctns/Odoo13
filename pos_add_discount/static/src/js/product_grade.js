odoo.define('pos_add_discount.product_grade', function (require) {
"use strict";

var core = require('web.core');
//var order    = this.pos.get_order();
var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var gui = require('point_of_sale.gui');
var model = models.PosModel.prototype.models;
models.load_fields('product.product','product_grade');
//console.log('order',order)

//var _super_PosModel = models.PosModel.prototype;
//    models.PosModel = models.PosModel.extend({
//        initialize: function (session, attributes) {
//            var product_model = _.find(this.models, function (model) {
//                return model.model === 'product.product';
//            });
//            product_model.fields.push('product_grade');
//            _super_PosModel.initialize.apply(this, arguments);
//        }
//    });

//push custom field to model
for(var i=0; i<models.length; i++){
    var model=models[i];
        if(model.model === 'product.product'){
            model.fields.push('product_grade');

        }
    }

//console.log(models)
 // save original class
var _super_posmodel = models.PosModel.prototype;
  // override original class with extended one
  models.PosModel = models.PosModel.extend({
    initialize: function (session, attributes) {
      var self = this;
      // some new code in this method
      models.load_fields('product.product',['product_grade']);
      // call original method via "apply"
      _super_posmodel.initialize.apply(this, arguments);
  },
});

//screens.PaymentScreenWidget.include({
//var order = self.pos.get_order();
//console.log('orderlines',order.get_orderlines());
//send_receipt_to_customer: function(order_server_ids) {
//        var order = this.pos.get_order();
//        var data = {
//            widget: this,
//            pos: order.pos,
//            order: order,
//            receipt: order.export_for_printing(),
//            orderlines: order.get_orderlines(),
//            paymentlines: order.get_paymentlines(),
//        };
//        console.log("data",data);
//
//
//    },
////    this.$('.next').click(function(){
////            self.validate_order();
////            console.log("data",data);
////        });
//
//});

//Modify orderline model and pass product_grade to receipt

var _super_orderline = models.Orderline.prototype;

models.Orderline = models.Orderline.extend({
    initialize: function(attr, options) {
        _super_orderline.initialize.call(this,attr,options);
        this.product_grade = this.product_grade || "";
    },

    export_for_printing: function(){
//        this._super(this);
        return {
            quantity:           this.get_quantity(),
            unit_name:          this.get_unit().name,
            price:              this.get_unit_display_price(),
            discount:           this.get_discount(),
            product_name:       this.get_product().display_name,
            product_grade:      this.get_product().product_grade,
            product_name_wrapped: this.generate_wrapped_product_name(),
            price_lst:          this.get_lst_price(),
            display_discount_policy:    this.display_discount_policy(),
            price_display_one:  this.get_display_price_one(),
            price_display :     this.get_display_price(),
            price_with_tax :    this.get_price_with_tax(),
            price_without_tax:  this.get_price_without_tax(),
            price_with_tax_before_discount:  this.get_price_with_tax_before_discount(),
            tax:                this.get_tax(),
            product_description:      this.get_product().description,
            product_description_sale: this.get_product().description_sale,
        };
    },

});
});
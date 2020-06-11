odoo.define('pos_add_discount.product_grade', function (require) {
"use strict";

var core = require('web.core');
//var order    = this.pos.get_order();
var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var gui = require('point_of_sale.gui');
var model = models.PosModel.prototype.models;
models.load_fields('product.product','product_grade');
models.load_fields('pos.order.line','product_grade');

console.log('models', models)
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

//////////////////////////////////////////////////////////////

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
            product_grade:      this.get_product().product_grade,//modification
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
////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////
//extend model product
//models.Product = models.Product.extend({
//    initialize: function(attr, options) {
//        _super_orderline.initialize.call(this,attr,options);
//        this.product_grade = this.product_grade || "";
//    },
////get_: function(pricelist, quantity){
////        var self = this;
////var self = this;
////var product_grade = this.product_grade;not working
//});
//////////////////////////////////////////
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

//var _super_orderline = models.Orderline.prototype;
//
//models.Orderline = models.Orderline.extend({
//    initialize: function(attr, options) {
//        _super_orderline.initialize.call(this,attr,options);
//        this.product_grade = this.product_grade || "";
//    },
////    var _super_orderline = models.Orderline.prototype;
//    export_for_printing: function(){
////        this._super(this);
//        _super_orderline.export_for_printing.apply(this);//super this
//         console.log('export_for_printing-orderline')
//        return {
//            quantity:           this.get_quantity(),
//            unit_name:          this.get_unit().name,
//            price:              this.get_unit_display_price(),
//            discount:           this.get_discount(),
//            product_name:       this.get_product().display_name,
////            product_grade:      this.get_product().product_grade,
////            product_grade_wrapped:      this.generate_wrapped_product_grade(),
//            product_grade_wrapped:this.get_product().product_grade,
//            product_name_wrapped: this.generate_wrapped_product_name(),
//            price_lst:          this.get_lst_price(),
//            display_discount_policy:    this.display_discount_policy(),
//            price_display_one:  this.get_display_price_one(),
//            price_display :     this.get_display_price(),
//            price_with_tax :    this.get_price_with_tax(),
//            price_without_tax:  this.get_price_without_tax(),
//            price_with_tax_before_discount:  this.get_price_with_tax_before_discount(),
//            tax:                this.get_tax(),
//            product_description:      this.get_product().description,
//            product_description_sale: this.get_product().description_sale,
//        };
//    },
//
//    generate_wrapped_product_grade: function() {
//        _super_orderline.generate_wrapped_product_grade.apply(this);//super this
//        var MAX_LENGTH = 24; // 40 * line ratio of .6
//        var wrapped = [];
//        var name = this.get_product().product_grade;
//        var current_line = "";
//
//        while (name.length > 0) {
//            var space_index = name.indexOf(" ");
//
//            if (space_index === -1) {
//                space_index = name.length;
//            }
//
//            if (current_line.length + space_index > MAX_LENGTH) {
//                if (current_line.length) {
//                    wrapped.push(current_line);
//                }
//                current_line = "";
//            }
//
//            current_line += name.slice(0, space_index + 1);
//            name = name.slice(space_index + 1);
//        }
//
//        if (current_line.length) {
//            wrapped.push(current_line);
//        }
//
//        return wrapped;
//    },
//
//});
//
////modify order
//var _super = models.Order;
//models.Order = models.Order.extend({
//
//
//export_for_printing: function(){
////        this._super(this);
////        _super_orderline.export_for_printing.apply(this);//super this
////         _super.prototype.export_for_printing.call(this);
//         _super.prototype.export_for_printing.apply(this);
//        var product_grade_wrapped;
//        console.log('export_for_printing-order')
//        return {
//            quantity:           this.get_quantity(),
//            unit_name:          this.get_unit().name,
//            price:              this.get_unit_display_price(),
//            discount:           this.get_discount(),
//            product_name:       this.get_product().display_name,
////            product_grade:      this.get_product().product_grade,
////            product_grade_wrapped:      this.generate_wrapped_product_grade(),
//            product_grade
//            product_name_wrapped: this.generate_wrapped_product_name(),
//            price_lst:          this.get_lst_price(),
//            display_discount_policy:    this.display_discount_policy(),
//            price_display_one:  this.get_display_price_one(),
//            price_display :     this.get_display_price(),
//            price_with_tax :    this.get_price_with_tax(),
//            price_without_tax:  this.get_price_without_tax(),
//            price_with_tax_before_discount:  this.get_price_with_tax_before_discount(),
//            tax:                this.get_tax(),
//            product_description:      this.get_product().description,
//            product_description_sale: this.get_product().description_sale,
//        };
//    },
//
//    get_product_grade : function(){
//        _super.prototype.get_product_grade.apply(this);
//
//        return this.get_product().product_grade;
//    }
//    }
//    }
//    generate_wrapped_product_grade: function() {
//        _super.prototype.generate_wrapped_product_grade.apply(this);
////        _super_orderline.generate_wrapped_product_grade.apply(this);//super this
//        var MAX_LENGTH = 24; // 40 * line ratio of .6
//        var wrapped = [];
//        var name = this.get_product().product_grade;
//        var current_line = "";
//        console.log('product grade', name)
//        while (name.length > 0) {
//            var space_index = name.indexOf(" ");
//
//            if (space_index === -1) {
//                space_index = name.length;
//            }
//
//            if (current_line.length + space_index > MAX_LENGTH) {
//                if (current_line.length) {
//                    wrapped.push(current_line);
//                }
//                current_line = "";
//            }
//
//            current_line += name.slice(0, space_index + 1);
//            name = name.slice(space_index + 1);
//        }
//
//        if (current_line.length) {
//            wrapped.push(current_line);
//        }
//
//        return wrapped;
//    },
//
//
//});
//
////extend order again
//
//var _super_order = models.Order.prototype;
//models.Order = models.Order.extend({
//    build_line_resume: function(){
//        _super_order.generate_build_line_resume.apply(this);
//        var resume = {};
//        this.orderlines.each(function(line){
//            if (line.mp_skip) {
//                return;
//            }
//            var line_hash = line.get_line_diff_hash();
//            var qty  = Number(line.get_quantity());
//            var note = line.get_note();
//            var product_id = line.get_product().id;
//            var product_grade_wrapped;
//
//            if (typeof resume[line_hash] === 'undefined') {
//                resume[line_hash] = {
//                    qty: qty,
//                    note: note,
//                    product_id: product_id,
//                    product_name_wrapped: line.generate_wrapped_product_name(),
//                    product_grade_wrapped:line.generate_wrapped_product_grade(),
//                };
//            } else {
//                resume[line_hash].qty += qty;
//            }
//
//        });
//        return resume;
//    },

});
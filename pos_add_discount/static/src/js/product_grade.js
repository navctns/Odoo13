odoo.define('pos_add_discount.pos_add_product_grade', function (require) {
"use strict";


var order    = this.pos.get_order();
var models = require('point_of_sale.models');
models.load_fields('product.template','product_grade');
console.log('order',order)

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


for(var i=0; i<models.length; i++){
    var model=models[i];
        if(model.model === 'product.product'){
            model.fields.push('product_grade');

        }
    }

});
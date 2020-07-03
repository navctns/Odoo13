odoo.define('payment_gaeway.paytrail_payment_form', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var _t = core._t;
    var qweb = core.qweb;
    var PaymentForm = require('payment.payment_form');
    ajax.loadXML('/payment_gateway/static/src/xml/paytrail_templates.xml', qweb);

    PaymentForm.include({

    willStart: function () {
        return this._super.apply(this, arguments).then(function () {
            return ajax.loadJS("https://payment.paytrail.com/e2/");
        })
    },

      //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * called when clicking on pay now or add payment event to create token for credit card/debit card.
     *
     * @private
     * @param {Event} ev
     * @param {DOMElement} checkedRadio
     * @param {Boolean} addPmEvent
     */

     _createPaytrailToken: function (ev, $checkedRadio, addPmEvent) {
        var self = this;
        if (ev.type === 'submit') {
            var button = $(ev.target).find('*[type="submit"]')[0]
        } else {
            var button = ev.target;
        }
        this.disableButton(button);
        var acquirerID = this.getAcquirerIdFromRadio($checkedRadio);
        var acquirerForm = this.$('#o_payment_add_token_acq_' + acquirerID);
        var inputsForm = $('input', acquirerForm);
        if (this.options.partnerId === undefined) {
            console.warn('payment_form: unset partner_id when adding new token; things could go wrong');
        }

        var formData = self.getFormData(inputsForm);
        var stripe = this.stripe;
        var card = this.stripe_card_element;
        if (card._invalid) {
            return;
        }
        return this._rpc({
            route: '/payment/paytrail/s2s/create_setup_intent',
            params: {'acquirer_id': formData.acquirer_id}
        }).then(function(intent_secret){
            return stripe.handleCardSetup(intent_secret, card);
        }).then(function(result) {
            if (result.error) {
                return Promise.reject({"message": {"data": { "arguments": [result.error.message]}}});
            } else {
                _.extend(formData, {"payment_method": result.setupIntent.payment_method});
                return self._rpc({
                    route: formData.data_set,
                    params: formData,
                })
            }
        }).then(function(result) {
            if (addPmEvent) {
                if (formData.return_url) {
                    window.location = formData.return_url;
                } else {
                    window.location.reload();
                }
            } else {
                $checkedRadio.val(result.id);
                self.el.submit();
            }
        }).guardedCatch(function (error) {
            // We don't want to open the Error dialog since
            // we already have a container displaying the error
            error.event.preventDefault();
            // if the rpc fails, pretty obvious
            self.enableButton(button);
            self.displayError(
                _t('Unable to save card'),
                _t("We are not able to add your payment method at the moment. ") +
                    self._parseError(error)
            );
        });
    },



//    require('web.dom_ready');
//    if (!$('.o_payment_form').length) {
//        return $.Deferred().reject("DOM doesn't contain '.o_payment_form'");
//    }
//
////    var observer = new MutationObserver(function(mutations, observer) {
////        for(var i=0; i<mutations.length; ++i) {
////            for(var j=0; j<mutations[i].addedNodes.length; ++j) {
////                if(mutations[i].addedNodes[j].tagName.toLowerCase() === "form" && mutations[i].addedNodes[j].getAttribute('provider') == 'razorpay') {
////                    display_razorpay_form($(mutations[i].addedNodes[j]));
////                }
////            }
////        }
////    });
//
//    function paytrail_show_error(msg) {
//        var wizard = $(qweb.render('paytrail.error', {'msg': msg || _t('Payment error')}));
//        wizard.appendTo($('body')).modal({'keyboard': true});
//    };
//
//    function razorpay_handler(resp) {
//        if (resp.razorpay_payment_id) {
//            $.post('/payment/paytrail/capture',{
//                payment_id: resp.razorpay_payment_id,
//            }).done(function (data) {
//                window.location.href = data;
//            }).fail(function (data) {
//                razorpay_show_error(data && data.data && data.data.message);
//            });
//        }
//    };

//    function display_razorpay_form(provider_form) {
//        // Open Checkout with further options
//        var payment_form = $('.o_payment_form');
//        if(!payment_form.find('i').length)
//        {
//            payment_form.append('<i class="fa fa-spinner fa-spin"/>');
//            payment_form.attr('disabled','disabled');
//        }
//
//        var get_input_value = function (name) {
//            return provider_form.find('input[name="' + name + '"]').val();
//        }
//        var primaryColor = getComputedStyle(document.body).getPropertyValue('--primary');
//        var options = {
//            "key": get_input_value('key'),
//            "amount": get_input_value('amount'),
//            "name": get_input_value('merchant_name'),
//            "description": get_input_value('description'),
//            "handler": razorpay_handler,
//            "modal": {
//                "ondismiss": function() { window.location.reload(); },
//                'backdropclose': function() { window.location.reload(); }
//            },
//            'prefill': {
//                'name': get_input_value('name'),
//                'contact': get_input_value('contact'),
//                'email': get_input_value('email')
//            },
//            'notes': {
//                'order_id': get_input_value('order_id'),
//            },
//            "theme": {
//                "color": primaryColor
//            },
//        }
//        var rzp1 = new Razorpay(options);
//        rzp1.open();
//    };
//
//    $.getScript("https://checkout.razorpay.com/v1/checkout.js", function (data, textStatus, jqxhr) {
//        observer.observe(document.body, {childList: true});
//        display_razorpay_form($('form[provider="razorpay"]'));
//    });
});

});
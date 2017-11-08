//module declaration
openerp.fgcmedia_prospectleads = function(instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    local.Share = instance.Widget.extend({
        start: function() {
            console.log("share facebook page loaded");
        },
    });

    instance.web.client_actions.add('getleads.share', 'instance.fgcmedia_prospectleads.share');
}
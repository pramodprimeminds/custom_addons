odoo.define('eenadu_reta.reta_dashboard', function (require){
   "use strict";
   var AbstractAction = require('web.AbstractAction');
   var core = require('web.core');
   var QWeb = core.qweb;
   var rpc = require('web.rpc');
   var ajax = require('web.ajax');
   var reta_dashboard_main = AbstractAction.extend({
      template: 'reta_dashboard',
   
      init: function(parent, context) {
          this._super(parent, context);
          this.dashboards_templates = ['reta_dashboard_data'];
      },
   
      willStart: function() {
         var self = this;
         return $.when(this._super()).then(function() {
            return self.fetch_data();
         });
      },
   
   
      start: function() {
         var self = this;
         return this._super().then(function() {
            self.render_dashboards();
         });
      },
   
      render_dashboards: function(){
         var self = this;
         _.each(this.dashboards_templates, function(template) {
            self.$('.o_reta_main_dashboard').append(QWeb.render(template, {widget: self}));
         });
      },
   
      fetch_data: function() {
         var self = this;
         var user_id = this.getSession().uid
         var def1 =  this._rpc({
               model: 'reta.dashboard.data',
               method: 'get_display_data',
               args: [[1],user_id],
      }).then(function(result){
            self.user = result['user'],
            self.cio = result['cio'],
            self.scheduling = result['scheduling'],
            self.waiting_for_approval = result['waiting_for_approval'],
            self.release_orders = result['release_orders'],
            self.invoices = result['invoices'],
            self.deposit_amt = result['deposit_amt'],
            self.outstanding_amt = result['outstanding_amt'],
            self.total_payment_received = result['total_payment_received'],
            self.total_commission_received = result['total_commission_received'],
            self.target_lines = result['target_lines']
        });
        return $.when(def1);
    },
   
   
   });
   core.action_registry.add('reta_dashboard_tags', reta_dashboard_main);
   return reta_dashboard_main;
   });
   
   $(document).ready(function(){
      $('body').delegate('.display_cio_div','click',function() {
         window.open($(".display_cio_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_scheduling_div','click',function() {
         window.open($(".display_scheduling_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_waiting_for_approval_div','click',function() {
         window.open($(".display_release_orders_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_release_orders_div','click',function() {
         window.open($(".display_release_orders_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_invoices_div','click',function() {
         window.open($(".display_invoices_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_deposits_div','click',function() {
         window.open($(".display_deposits_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_commission_div','click',function() {
         window.open($(".display_commission_div").attr("test"),'_blank');
      });
   });
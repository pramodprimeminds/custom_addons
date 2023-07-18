odoo.define('sales_circulation.sales_circulation_dashboard', function (require){
"use strict";
var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var QWeb = core.qweb;
var rpc = require('web.rpc');
var ajax = require('web.ajax');
var SalesCirculationDashBoard = AbstractAction.extend({
   template: 'sales_circulation_dashboards',
   init: function(parent, context) {
       this._super(parent, context);
       this.dashboards_templates = ['sales_circulation_dashboard_data'];
       this.today_sale = [];
   },
       willStart: function() {
       var self = this;
       return $.when(this._super()).then(function() {
           return self.fetch_data();
       });
   },
   start: function() {
           var self = this;
           this.set("title", 'Dashboard');
           return this._super().then(function() {
               self.render_dashboards();
           });
       },
       render_dashboards: function(){
       var self = this;
       _.each(this.dashboards_templates, function(template) {
               self.$('.o_pj_dashboard').append(QWeb.render(template, {widget: self}));
           });
   },
fetch_data: function() {
       var self = this;
       var def1 =  this._rpc({
               model: 'sales.circulation.dashboard.data',
               method: 'get_display_data'
   }).then(function(result)
    {
      self.total_amount_inv = result['total_amount_inv'],
      self.total_due_amount = result['total_due_amount'],
      self.deposit_amt = result['deposit_amt'],
      self.outstanding_amt = result['outstanding_amt'],
      self.returns = result['returns'],
      self.total_indent_copies = result['total_indent_copies'],
      self.indent_lines = result['indent_lines']
   });
       return $.when(def1);
   },
})
core.action_registry.add('sales_circulation_dashboard_tags', SalesCirculationDashBoard);
return SalesCirculationDashBoard;
});
$(document).ready(function(){
      $('body').delegate('.display_cio_div','click',function() {
         window.open($(".display_cio_div").attr("test"),'_blank');
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
   });

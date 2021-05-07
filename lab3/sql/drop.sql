use bank;

alter table 储蓄开户 
	drop constraint FK_储蓄开户_储蓄开户_客户;

alter table 储蓄开户
   drop constraint FK_储蓄开户_储蓄开户2_支行;

alter table 储蓄开户
   drop constraint FK_储蓄开户_储蓄开户3_储蓄账户;

alter table 储蓄账户
   drop constraint FK_储蓄账户_INHERITAN_账户;

alter table 员工
   drop constraint FK_员工_领导_员工;

alter table 客户
   drop constraint FK_客户_负责_员工;

alter table 拥有5
   drop constraint FK_拥有5_拥有5_贷款;

alter table 拥有5
   drop constraint FK_拥有5_拥有6_客户;

alter table 支付情况
   drop constraint FK_支付情况_支付情况_贷款;

alter table 支付情况
   drop constraint FK_支付情况_支付情况2_客户;

alter table 贷款
   drop constraint FK_贷款_拥有贷款_支行;

alter table 贷款开户
   drop constraint FK_贷款开户_贷款开户_客户;

alter table 贷款开户
   drop constraint FK_贷款开户_贷款开户2_支行;

alter table 贷款开户
   drop constraint FK_贷款开户_贷款开户3_贷款账户;

alter table 贷款账户
   drop constraint FK_贷款账户_INHERITAN_账户;

drop table 储蓄开户;

drop table 储蓄账户;

drop table 员工;

drop table 客户;

drop table 拥有5;

drop table 支付情况;

drop table 支行;

drop table 账户;

drop table 贷款;

drop table 贷款开户;

drop table 贷款账户;
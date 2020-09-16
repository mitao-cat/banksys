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

drop index 储蓄开户3_FK;

drop index 储蓄开户2_FK;

drop index 储蓄开户_FK;

drop table 储蓄开户 cascade constraints;

drop table 储蓄账户 cascade constraints;

drop index 领导_FK;

drop table 员工 cascade constraints;

drop index 负责_FK;

drop table 客户 cascade constraints;

drop index 拥有6_FK;

drop index 拥有5_FK;

drop table 拥有5 cascade constraints;

drop index 支付情况2_FK;

drop index 支付情况_FK;

drop table 支付情况 cascade constraints;

drop table 支行 cascade constraints;

drop table 账户 cascade constraints;

drop index 拥有贷款_FK;

drop table 贷款 cascade constraints;

drop index 贷款开户3_FK;

drop index 贷款开户2_FK;

drop index 贷款开户_FK;

drop table 贷款开户 cascade constraints;

drop table 贷款账户 cascade constraints;

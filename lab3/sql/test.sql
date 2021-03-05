select * from 储蓄账户;
select * from 贷款账户

delete from 储蓄账户 where 账户号 = 2365 and 开户日期 = to_date('2015/03/26', 'yyyy/MM/dd') and 余额 = 12036.0 and 利率 = 0.015 and 货币类型 = '人民币'

select from 账户 where 账户号 = 2365 and 开户日期 = to_date('2015/03/26', 'yyyy/MM/dd') and 余额 = 12036.0;

delete from 储蓄账户 where 账户号 = 2365 and 开户日期 = to_date('2015/03/26', 'yyyy/MM/dd') and 余额 = 12036.0 and 利率 = 0.015 and 货币类型 = '人民币';

delete from 储蓄开户 where 账户号 = 2365
delete from 储蓄账户 where 账户号 = 2365 and 开户日期 = to_date('2015/03/26', 'yyyy/MM/dd') and 余额 = 12036.0 and 1 = 1 and 货币类型 = '人民币'
delete from 账户 where 账户号 = 2365

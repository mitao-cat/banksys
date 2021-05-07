#-*-coding:utf-8 -*- 
from ui_bank import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTreeWidgetItem
from PyQt5.QtCore import QDate
from PyQt5 import QtCore
import sys

#----------------------------------------------#
#              包装函数部分                     #
#----------------------------------------------#
def wrap_condition(left, right, isString = True):
	if right == '':
		return '1 = 1'
	else:
		return left + ' = ' + wrap_value(right, isString)

def wrap_value(value, isString = True):
	if isString:
		return  '\'' + value + '\''
	else:
		return value

def get_date(string):
	date = str(string).split('-')
	y=date[0]
	m=date[1]
	d=date[2][0:2]
	return y + '/' + m + '/' + d

#----------------------------------------------#
#              界面逻辑部分                     #
#----------------------------------------------#
class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super().__init__(parent) #初始化QMainWindows类
		self.setupUi(self)
		self.bind_up()
		self.query = ""
		self.before = ""
		self.before2 = ""
		self.op = [' = ', ' != ', ' > ', ' < '] 
		self.comboBox_2.setCurrentIndex(1)
		self.comboBox_3.setCurrentIndex(1)
		self.comboBox_4.setCurrentIndex(1)
		self.comboBox_5.setCurrentIndex(1)
		self.comboBox_6.setCurrentIndex(1)
	def bind_up(self):
		##This function bind up all the signal with relative slot function
		self.pushButton.clicked.connect(self.insert_bank)
		self.pushButton_2.clicked.connect(self.delete_bank)
		self.pushButton_3.clicked.connect(self.update_bank)
		self.pushButton_4.clicked.connect(self.select_bank)
		self.pushButton_9.clicked.connect(self.clear_bank)
		self.treeWidget.itemDoubleClicked.connect(self.double_click_bank)

		self.pushButton_11.clicked.connect(self.insert_staff)
		self.pushButton_12.clicked.connect(self.delete_staff)
		self.pushButton_13.clicked.connect(self.update_staff)
		self.pushButton_14.clicked.connect(self.select_staff)
		self.pushButton_10.clicked.connect(self.clear_staff)
		self.treeWidget_2.itemDoubleClicked.connect(self.double_click_staff)


		self.pushButton_16.clicked.connect(self.insert_client)
		self.pushButton_17.clicked.connect(self.delete_client)
		self.pushButton_18.clicked.connect(self.update_client)
		self.pushButton_19.clicked.connect(self.select_client)
		self.pushButton_15.clicked.connect(self.clear_client)
		self.treeWidget_3.itemDoubleClicked.connect(self.double_click_client)

		self.pushButton_21.clicked.connect(self.insert_account)
		self.pushButton_22.clicked.connect(self.delete_account)
		self.pushButton_23.clicked.connect(self.update_account)
		self.pushButton_24.clicked.connect(self.select_account)
		self.pushButton_20.clicked.connect(self.clear_account)
		self.treeWidget_4.itemDoubleClicked.connect(self.double_click_account)


		self.pushButton_26.clicked.connect(self.insert_loan)
		self.pushButton_27.clicked.connect(self.delete_loan)
		self.pushButton_28.clicked.connect(self.update_loan)
		self.pushButton_29.clicked.connect(self.select_loan)
		self.pushButton_25.clicked.connect(self.clear_loan)
		self.treeWidget_5.itemDoubleClicked.connect(self.double_click_loan)
		self.pushButton_30.clicked.connect(self.pay_loan)
		

		self.pushButton_32.clicked.connect(self.store_statistic)
		self.pushButton_35.clicked.connect(self.clear_store_statistic)
		self.pushButton_34.clicked.connect(self.loan_statistic)
		self.pushButton_36.clicked.connect(self.clear_loan_statistic)
	
	def get_query(self, need_fetch):
		global db
		#print(self.query)
		result = []
		if host == 0:
			cursor = db.cursor()
			try:
				cursor.execute(self.query)
			except:
				self.error_input('SQL query denied, please check your input!')
				return
			if need_fetch:
				result = cursor.fetchall()
			
			db.commit()
			cursor.close()
		
		self.before = '' #每进行一次操作需要刷新 doubleclicked item时记录的待更改值
		return result

	def error_input(self, err_msg):
		QMessageBox.information(self, "消息", err_msg, QMessageBox.Yes | QMessageBox.No) 

	# ---------------------------------------------------#
	#                Main Part code                      #
	#----------------------------------------------------#

	# ----------------- bank ----------------------------#
	def insert_bank(self):
		if self.lineEdit_1.text() == '' or self.lineEdit_2.text() == '' or self.lineEdit_3.text() == '':
			self.error_input('输入信息不足!')
			return
		#确认插入
		self.comboBox_5.setCurrentIndex(0)
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No: 
			return

		self.query = 'insert into 支行(城市, 名字, 资产) Values(' + wrap_value(self.lineEdit_1.text()) + ', '+ wrap_value(self.lineEdit_2.text()) + ', '+ wrap_value(self.lineEdit_3.text(), False) + ')'
		#query_result = self.get_query(False)
	
	def delete_bank(self):
		self.select_bank()
		#确认删除
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No: 
			return
		
		if self.lineEdit_3.text() == '':
			money = '1 = 1'
		else:
			money = '资产' + self.op[self.comboBox_5.currentIndex()] + self.lineEdit_3.text()

		self.query = 'delete from 支行 where ' + wrap_condition('城市', self.lineEdit_1.text()) + ' and ' + wrap_condition('名字', self.lineEdit_2.text()) + ' and ' + money
		self.get_query(False)
		self.treeWidget.clear()
	
	def update_bank(self):
		if self.lineEdit_1.text() == '' or self.lineEdit_2.text() == '' or self.lineEdit_3.text() == '':
			self.error_input('输入数据不足!')
			return
		if self.before == '': #update 输入信息不足
			self.error_input('注意修改之前需要双击待修改项目哦！')
			return
		setting = wrap_condition('城市', self.lineEdit_1.text()) + ', ' + wrap_condition('名字', self.lineEdit_2.text()) + ', ' + wrap_condition('资产', self.lineEdit_3.text(), False)
		self.query = 'update 支行 set ' + setting + ' where ' + self.before
		#确认更新
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
		if reply == QMessageBox.No: 
			return
		self.get_query(False)

	def select_bank(self):
		if self.lineEdit_3.text() == '':
			money = '1 = 1'
		else:
			money = '资产' + self.op[self.comboBox_5.currentIndex()] + self.lineEdit_3.text()

		self.query = 'select * from 支行 where ' + wrap_condition('城市', self.lineEdit_1.text()) + ' and ' + wrap_condition('名字', self.lineEdit_2.text()) + ' and ' + money
		query_result = self.get_query(True)
		if host == 0 and query_result is not None:
			self.feed_table_bank(query_result)
		
	def double_click_bank(self, item, column):
		self.lineEdit_1.setText(item.text(0))
		self.lineEdit_2.setText(item.text(1))
		self.lineEdit_3.setText(item.text(2))
		self.comboBox_5.setCurrentIndex(0)
		self.before =  wrap_condition('城市', item.text(0)) + ' and ' + wrap_condition('名字', item.text(1)) + ' and ' + wrap_condition('资产', item.text(2), False)
	
	def clear_bank(self):
		self.lineEdit_1.setText('')
		self.lineEdit_2.setText('')
		self.lineEdit_3.setText('')
		self.comboBox_5.setCurrentIndex(1)

	def feed_table_bank(self, result):
		self.treeWidget.clear()
		L=[]
		for row in result:
			L.append(QTreeWidgetItem([str(row[0]), str(row[1]), str(row[2])]))
		self.treeWidget.addTopLevelItems(L)
	
	# ------------------ staff --------------------------#	
	def insert_staff(self):
		if self.lineEdit_4.text() == '':
			self.error_input('输入信息不足!')
			return
		#确认插入
		self.comboBox_3.setCurrentIndex(0)
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No: 
			return
		self.query = 'insert into 员工(身份证号Y, 员工_身份证号Y, 姓名Y, 电话号码Y, 家庭住址Y, 开始工作日期) Values(' + wrap_value(self.lineEdit_4.text()) + ', '+ wrap_value(self.lineEdit_22.text()) + ', ' +  wrap_value(self.lineEdit_5.text()) + ', '+ wrap_value(self.lineEdit_6.text()) +', ' + wrap_value(self.lineEdit_7.text()) + ', ' 'str_to_date('+ wrap_value(self.dateEdit.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d')  + ')' +')'
		self.get_query(False)
		
	def delete_staff(self):
		self.select_staff()
		#确认删除
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No: 
			return
		self.query = 'delete from 员工 where ' + wrap_condition('身份证号Y', self.lineEdit_4.text()) + ' and ' + wrap_condition('员工_身份证号Y', self.lineEdit_22.text()) + ' and ' + wrap_condition('姓名Y', self.lineEdit_5.text()) + ' and ' + wrap_condition('电话号码Y', self.lineEdit_6.text()) + ' and ' + wrap_condition('家庭住址Y', self.lineEdit_7.text()) + ' and ' + '开始工作日期' + self.op[self.comboBox_3.currentIndex()] + 'str_to_date('+ wrap_value(self.dateEdit.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d')  + ')'
		self.get_query(False)
		self.treeWidget_2.clear()
	
	def update_staff(self):
		if self.lineEdit_4.text() == '':
			self.error_input('输入数据不足!')
			return
		if self.before == '': #update 输入信息不足
			self.error_input('注意修改之前需要双击待修改项目哦！')
			return
		self.comboBox_3.setCurrentIndex(0)  #更新时只能使用日期 = 操作符
		setting = wrap_condition('身份证号Y', self.lineEdit_4.text()) + ', ' + wrap_condition('员工_身份证号Y', self.lineEdit_22.text()) + ', ' + wrap_condition('姓名Y', self.lineEdit_5.text()) + ', ' + wrap_condition('电话号码Y', self.lineEdit_6.text()) + ', '+ wrap_condition('家庭住址Y', self.lineEdit_7.text()) + ', ' + '开始工作日期 = str_to_date('+ wrap_value(self.dateEdit.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')'
		
		self.query = 'update 员工 set ' + setting + ' where ' + self.before
		#确认更新
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
		if reply == QMessageBox.No: 
			return
		self.get_query(False)

	def select_staff(self):
		self.query = 'select * from 员工 where ' + wrap_condition('身份证号Y', self.lineEdit_4.text()) + ' and ' + wrap_condition('身份证号Y', self.lineEdit_22.text()) + ' and ' + wrap_condition('姓名Y', self.lineEdit_5.text()) + ' and ' + wrap_condition('电话号码Y', self.lineEdit_6.text()) + ' and ' + wrap_condition('家庭住址Y', self.lineEdit_7.text()) + ' and ' + '开始工作日期' + self.op[self.comboBox_3.currentIndex()] +'str_to_date('+ wrap_value(self.dateEdit.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')'
		query_result = self.get_query(True)
		if host == 0 and query_result is not None:
			self.feed_table_staff(query_result)
		
	def double_click_staff(self, item, column):
		self.lineEdit_4.setText(item.text(0))
		self.lineEdit_22.setText(item.text(2))
		self.lineEdit_5.setText(item.text(3))
		self.lineEdit_6.setText(item.text(4))
		self.lineEdit_7.setText(item.text(5))
		self.dateEdit.setDate(QDate.fromString(item.text(6), 'yyyy/MM/dd'))
		self.comboBox_3.setCurrentIndex(0)  #更新时只能使用日期 = 操作符
		
		self.dateEdit.setDate(QDate.fromString(item.text(5), 'yyyy/MM/dd'))
		self.before =  wrap_condition('身份证号Y', item.text(0)) + ' and ' + wrap_condition('员工_身份证号Y', item.text(2)) + ' and ' + wrap_condition('姓名Y', item.text(3)) + ' and ' + wrap_condition('电话号码Y', item.text(4)) + ' and ' + wrap_condition('家庭住址Y', item.text(5)) + ' and ' + '开始工作日期 = str_to_date('+ wrap_value(item.text(6)) + ', ' + wrap_value('%Y/%m/%d') + ')'
	
	def clear_staff(self):
		self.lineEdit_4.setText('')
		self.comboBox_3.setCurrentIndex(1)
		self.lineEdit_5.setText('')
		self.lineEdit_6.setText('')
		self.lineEdit_7.setText('')
		self.lineEdit_22.setText('')
		self.dateEdit.setDate(QDate.fromString('2000/01/01', 'yyyy/MM/dd'))
	
	def feed_table_staff(self, result):
		self.treeWidget_2.clear()
		L=[]
		for row in result:
			if row[1] == row[0]:
				manager = '是'
			else :
				manager = '否'
			date = get_date(row[5])
			L.append(QTreeWidgetItem([str(row[0]), manager, str(row[1]), str(row[2]), str(row[3]), str(row[4]), date]))
		self.treeWidget_2.addTopLevelItems(L)
	
	# ----------------- client ----------------------------#
	def insert_client(self):
		if self.lineEdit_8.text() == '' or self.lineEdit_16.text() == '' or self.lineEdit_12.text() == '':
			self.error_input('输入信息不足!')
			return
		#确认插入
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No: 
			return
		self.query = 'insert into 客户(身份证号, 身份证号Y, 姓名, 联系电话, 家庭住址, 联系人姓名, 联系人手机号, 联系人Email, 联系人与客户关系) Values(' + wrap_value(self.lineEdit_8.text()) + ', '+ wrap_value(self.lineEdit_16.text()) + ', '+ wrap_value(self.lineEdit_9.text()) + ', '+ wrap_value(self.lineEdit_10.text())  + ', '+ wrap_value(self.lineEdit_11.text()) +  ', '+ wrap_value(self.lineEdit_12.text()) + ', '+ wrap_value(self.lineEdit_13.text()) + ', '+ wrap_value(self.lineEdit_14.text()) + ', '+ wrap_value(self.lineEdit_15.text()) + ')'
		self.get_query(False)

	def delete_client(self):
		self.select_client()
		#确认删除
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No: 
			return

		self.query = 'delete from 客户 where ' + wrap_condition('身份证号', self.lineEdit_8.text()) + ' and ' + wrap_condition('身份证号Y', self.lineEdit_16.text()) + ' and ' + wrap_condition('姓名', self.lineEdit_9.text()) + ' and ' + wrap_condition('联系电话 ', self.lineEdit_10.text()) + ' and ' + wrap_condition('家庭住址', self.lineEdit_11.text()) + ' and ' + wrap_condition('联系人姓名', self.lineEdit_12.text()) + ' and ' + wrap_condition('联系人手机号', self.lineEdit_13.text()) + ' and ' + wrap_condition('联系人Email', self.lineEdit_14.text()) + ' and ' + wrap_condition('联系人与客户关系', self.lineEdit_15.text())

		self.get_query(False)
		self.treeWidget_3.clear()
	
	def update_client(self):
		if self.lineEdit_8.text() == '' or self.lineEdit_16.text() == '' or self.lineEdit_12.text() == '':
			self.error_input('输入数据不足!')
			return
		if self.before == '': #update 输入信息不足
			self.error_input('注意修改之前需要双击待修改项目哦！')
			return

		setting = wrap_condition('身份证号', self.lineEdit_8.text()) + ', ' + wrap_condition('身份证号Y', self.lineEdit_16.text()) + ', ' + wrap_condition('姓名', self.lineEdit_9.text()) + ', ' + wrap_condition('联系电话 ', self.lineEdit_10.text()) + ', ' + wrap_condition('家庭住址', self.lineEdit_11.text()) + ', ' + wrap_condition('联系人姓名', self.lineEdit_12.text()) + ', ' + wrap_condition('联系人手机号', self.lineEdit_13.text()) + ', ' + wrap_condition('联系人Email', self.lineEdit_14.text()) + ', ' + wrap_condition('联系人与客户关系', self.lineEdit_15.text())

		self.query = 'update 客户 set ' + setting + ' where ' + self.before
		#确认更新
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
		if reply == QMessageBox.No : 
			return
		self.get_query(False)

	def select_client(self):

		self.query = 'select * from 客户 where ' + wrap_condition('身份证号', self.lineEdit_8.text()) + ' and ' + wrap_condition('身份证号Y', self.lineEdit_16.text()) + ' and ' + wrap_condition('姓名', self.lineEdit_9.text()) + ' and ' + wrap_condition('联系电话 ', self.lineEdit_10.text()) + ' and ' + wrap_condition('家庭住址', self.lineEdit_11.text()) + ' and ' + wrap_condition('联系人姓名', self.lineEdit_12.text()) + ' and ' + wrap_condition('联系人手机号', self.lineEdit_13.text()) + ' and ' + wrap_condition('联系人Email', self.lineEdit_14.text()) + ' and ' + wrap_condition('联系人与客户关系', self.lineEdit_15.text())

		query_result = self.get_query(True)
		if host == 0 and query_result is not None:
			self.feed_table_client(query_result)
		
	def double_click_client(self, item, column):
		self.lineEdit_8.setText(item.text(0))
		self.lineEdit_16.setText(item.text(1))
		self.lineEdit_9.setText(item.text(2))
		self.lineEdit_10.setText(item.text(3))
		self.lineEdit_11.setText(item.text(4))
		self.lineEdit_12.setText(item.text(5))
		self.lineEdit_13.setText(item.text(6))
		self.lineEdit_14.setText(item.text(7))
		self.lineEdit_15.setText(item.text(8))

		self.before =  wrap_condition('身份证号', self.lineEdit_8.text()) + ' and ' + wrap_condition('身份证号Y', self.lineEdit_16.text()) + ' and ' + wrap_condition('姓名', self.lineEdit_9.text()) + ' and ' + wrap_condition('联系电话 ', self.lineEdit_10.text()) + ' and ' + wrap_condition('家庭住址', self.lineEdit_11.text()) + ' and ' + wrap_condition('联系人姓名', self.lineEdit_12.text()) + ' and ' + wrap_condition('联系人手机号', self.lineEdit_13.text()) + ' and ' + wrap_condition('联系人Email', self.lineEdit_14.text()) + ' and ' + wrap_condition('联系人与客户关系', self.lineEdit_15.text())
	
	def clear_client(self):
		self.lineEdit_8.setText('')
		self.lineEdit_16.setText('')
		self.lineEdit_9.setText('')
		self.lineEdit_10.setText('')
		self.lineEdit_11.setText('')
		self.lineEdit_12.setText('')
		self.lineEdit_13.setText('')
		self.lineEdit_14.setText('')
		self.lineEdit_15.setText('')
		self.comboBox_3.setCurrentIndex(0)

	def feed_table_client(self, result):
		self.treeWidget_3.clear()
		L=[]
		for row in result:
			L.append(QTreeWidgetItem([str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]),str(row[6]), str(row[7]), str(row[8]), str(row[9])]))
		self.treeWidget_3.addTopLevelItems(L)

	# ----------------- account ----------------------------#
	def insert_account(self):
		if self.lineEdit_17.text() == '':
			self.error_input('输入信息不足!')
			return
		#确认插入
		self.comboBox_4.setCurrentIndex(0)
		self.comboBox_2.setCurrentIndex(0) #插入操作强制设置日期 = op
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No: 
			return
		
		self.query = 'insert into 账户(账户号, 开户日期, 余额) Values(' + wrap_value(self.lineEdit_17.text(), False) + ', '+ 'str_to_date('+ wrap_value(self.dateEdit_2.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ', '+ wrap_value(self.lineEdit_19.text(), False) + ')'
		self.get_query(False)
		if self.comboBox_7.currentIndex() == 0 :
			self.query = 'insert into 储蓄账户(账户号, 开户日期, 余额, 利率, 货币类型) Values(' + wrap_value(self.lineEdit_17.text(), False) + ', '+ 'str_to_date('+ wrap_value(self.dateEdit_2.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ', '+ wrap_value(self.lineEdit_19.text(), False) + ', ' + wrap_value(self.lineEdit_25.text(), False) + ', ' + wrap_value(self.lineEdit_26.text()) + ')'
		else:
			self.query = 'insert into 贷款账户(账户号, 开户日期, 余额, 透支额) Values(' + wrap_value(self.lineEdit_17.text(), False) + ', '+ 'str_to_date('+ wrap_value(self.dateEdit_2.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ', '+ wrap_value(self.lineEdit_19.text(), False) +  ', ' + wrap_value(self.lineEdit_27.text(), False) + ')'
		self.get_query(False)
		
	def delete_account(self):
		if self.lineEdit_17.text() == '':
			self.error_input('请给定销户账号！')
			return
		self.select_account()
		#确认删除
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No: 
			return
		
		if self.lineEdit_19.text() == '':
			money = '1 = 1'
		else:
			money = '余额' + self.op[self.comboBox_4.currentIndex()] + self.lineEdit_19.text()
		if self.comboBox_7.currentIndex() == 0 :
			self.query = 'delete from 储蓄开户 where ' + wrap_condition('账户号', self.lineEdit_17.text(), False) 
			self.get_query(False)
			self.query = 'delete from 储蓄账户 where ' + wrap_condition('账户号', self.lineEdit_17.text(), False) + ' and ' + '开户日期' + self.op[self.comboBox_2.currentIndex()] + 'str_to_date('+ wrap_value(self.dateEdit_2.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ' and ' + money + ' and ' + wrap_condition('利率', self.lineEdit_25.text(), False) + ' and ' + wrap_condition('货币类型', self.lineEdit_26.text())
		else :
			self.query = 'delete from 贷款开户 where ' + wrap_condition('账户号', self.lineEdit_17.text(), False)
			self.get_query(False)
			self.query = 'delete from 贷款账户 where ' + wrap_condition('账户号', self.lineEdit_17.text(), False) + ' and ' + '开户日期' + self.op[self.comboBox_2.currentIndex()] + 'str_to_date('+ wrap_value(self.dateEdit_2.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ' and ' + money + ' and ' + wrap_condition('透支额', self.lineEdit_27.text(), False)
		self.get_query(False)
		self.query = 'delete from 账户 where ' + wrap_condition('账户号', self.lineEdit_17.text(), False)
		
		self.get_query(False)
		self.treeWidget.clear()
	
	def update_account(self):
		if self.lineEdit_17.text() == '':
			self.error_input('输入数据不足!')
			return
		if self.before == '': #update 输入信息不足
			self.error_input('注意修改之前需要双击待修改项目！')
			return
		
		self.comboBox_2.setCurrentIndex(0) #更新操作强制设置日期 = op
		self.comboBox_4.setCurrentIndex(0)
		if self.comboBox_7.currentIndex() == 0 :
			setting = wrap_condition('账户号', self.lineEdit_17.text(), False) + ', ' + '开户日期 = str_to_date('+ wrap_value(self.dateEdit_2.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ', ' + wrap_condition('余额', self.lineEdit_19.text(), False) +  ', ' + wrap_condition('利率', self.lineEdit_25.text(), False) + ', ' + wrap_condition('货币类型', self.lineEdit_26.text())
			self.query = 'update 储蓄账户 set ' + setting + ' where ' + self.before
		else:
			setting = wrap_condition('账户号', self.lineEdit_17.text(), False) + ', ' + '开户日期 = str_to_date('+ wrap_value(self.dateEdit_2.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ', ' + wrap_condition('余额', self.lineEdit_19.text(), False) +  ', ' + wrap_condition('透支额', self.lineEdit_27.text(), False)
			self.query = 'update 贷款账户 set ' + setting + ' where ' + self.before
		#确认更新
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
		if reply == QMessageBox.No: 
			return
		self.get_query(False)
		setting = wrap_condition('账户号', self.lineEdit_17.text(), False) + ', ' + '开户日期 = str_to_date('+ wrap_value(self.dateEdit_2.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ', ' + wrap_condition('余额', self.lineEdit_19.text(), False)
		self.query = 'update 账户 set ' + setting + ' where ' + self.before2
		self.get_query(False)
		self.before2 = ""
		
	def select_account(self):
		if self.lineEdit_19.text() == '':
			money = '1 = 1'
		else:
			money = '余额' + self.op[self.comboBox_4.currentIndex()] + self.lineEdit_19.text()
		if self.comboBox_7.currentIndex() == 0 :
			self.query = 'select * from 储蓄账户 where ' + wrap_condition('账户号', self.lineEdit_17.text(), False) + ' and ' + '开户日期' + self.op[self.comboBox_2.currentIndex()] + 'str_to_date('+ wrap_value(self.dateEdit_2.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ' and ' + money + ' and ' + wrap_condition('利率', self.lineEdit_25.text(), False) + ' and ' + wrap_condition('货币类型', self.lineEdit_26.text())
		else:
			self.query = 'select * from 贷款账户 where ' + wrap_condition('账户号', self.lineEdit_17.text(), False) + ' and ' + '开户日期' + self.op[self.comboBox_2.currentIndex()] + 'str_to_date('+ wrap_value(self.dateEdit_2.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ' and ' + money + ' and ' + wrap_condition('透支额', self.lineEdit_27.text(), False)
		query_result = self.get_query(True) 
		if host == 0 and query_result is not None:
			self.feed_table_account(query_result)
		
	def double_click_account(self, item, column):
		self.lineEdit_17.setText(item.text(0))
		self.comboBox_2.setCurrentIndex(0)
		self.comboBox_4.setCurrentIndex(0)
		self.dateEdit_2.setDate(QDate.fromString(item.text(1), 'yyyy/MM/dd'))
		self.lineEdit_19.setText(item.text(2))
		self.before2 = wrap_condition('账户号', item.text(0), False) + ' and ' + '开户日期 = str_to_date('+ wrap_value(self.dateEdit_2.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ' and ' + wrap_condition('余额', item.text(2), False)
		if self.comboBox_7.currentIndex() == 0 :
			self.lineEdit_25.setText(item.text(3))
			self.lineEdit_26.setText(item.text(4))
			self.before =  wrap_condition('账户号', item.text(0), False) + ' and ' + '开户日期 = str_to_date('+ wrap_value(self.dateEdit_2.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ' and ' + wrap_condition('余额', item.text(2), False) + ' and ' + wrap_condition('利率', item.text(3), False) +  ' and ' + wrap_condition('货币类型', item.text(4))
		else:
			self.lineEdit_27.setText(item.text(3))
			self.before =  wrap_condition('账户号', item.text(0), False) + ' and ' + '开户日期 = str_to_date('+ wrap_value(self.dateEdit_2.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ' and ' + wrap_condition('余额', item.text(2), False) +' and ' + wrap_condition('透支额', item.text(3), False)
	
	def clear_account(self):
		self.lineEdit_17.setText('')
		self.comboBox_2.setCurrentIndex(1)
		self.comboBox_4.setCurrentIndex(1)
		self.dateEdit_2.setDate(QDate.fromString('2000/01/01', 'yyyy/MM/dd'))
		self.lineEdit_19.setText('')
		
		self.comboBox_7.setCurrentIndex(0)
		self.lineEdit_25.setText('')
		self.lineEdit_26.setText('')
		self.lineEdit_27.setText('')

	def feed_table_account(self, result):
		_translate = QtCore.QCoreApplication.translate
		self.treeWidget_4.clear()
		L=[]
		if self.comboBox_7.currentIndex() == 0 :
			self.treeWidget_4.headerItem().setText(0, _translate("MainWindow", "账户号"))
			self.treeWidget_4.headerItem().setText(1, _translate("MainWindow", "开户日期"))
			self.treeWidget_4.headerItem().setText(2, _translate("MainWindow", "余额"))
			self.treeWidget_4.headerItem().setText(3, _translate("MainWindow", "利率"))
			self.treeWidget_4.headerItem().setText(4, _translate("MainWindow", "货币类型"))
			for row in result:
				date = get_date(row[1])
				L.append(QTreeWidgetItem([str(row[0]), date, str(row[2]),str(row[4]),str(row[3])]))
			self.treeWidget_4.addTopLevelItems(L)
		else:
			self.treeWidget_4.headerItem().setText(0, _translate("MainWindow", "账户号"))
			self.treeWidget_4.headerItem().setText(1, _translate("MainWindow", "开户日期"))
			self.treeWidget_4.headerItem().setText(2, _translate("MainWindow", "余额"))
			self.treeWidget_4.headerItem().setText(3, _translate("MainWindow", "透支额"))
			self.treeWidget_4.headerItem().setText(4, _translate("MainWindow", ""))
			for row in result:
				date = get_date(row[1])
				L.append(QTreeWidgetItem([str(row[0]), date, str(row[2]), str(row[3])]))
			self.treeWidget_4.addTopLevelItems(L)

	#------------------------loan ----------------------------#
	def insert_loan(self):
		if self.lineEdit_20.text() == '':
			self.error_input('输入信息不足!')
			return
		self.comboBox_6.setCurrentIndex(0)
		#确认插入
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No: 
			return
		self.query = 'insert into 贷款(金额1, 贷款号, 名字) Values(' + wrap_value(self.lineEdit_18.text(), False) + ', '+ wrap_value(self.lineEdit_20.text(), False) + ', '+ wrap_value(self.lineEdit_21.text()) + ')'
		#query_result = self.get_query(False)

	def delete_loan(self):
		self.select_loan()
		#确认删除
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No: 
			return
		if self.lineEdit_18.text() == '':
			money = '1 = 1'
		else:
			money = '金额1' + self.op[self.comboBox_6.currentIndex()] + self.lineEdit_18.text()
		self.query  = 'delete from 贷款 where ' + money + ' and ' + wrap_condition('贷款号', self.lineEdit_20.text(), False) + ' and ' + wrap_condition('名字', self.lineEdit_21.text())

		self.get_query(False)
		self.treeWidget.clear()
	
	def update_loan(self):
		if self.lineEdit_20.text() == '':
			self.error_input('输入数据不足!')
			return
		if self.before == '': #update 输入信息不足
			self.error_input('没有选中更新对象!')
			return
		self.comboBox_6.setCurrentIndex(0)
		setting = wrap_condition('金额1', self.lineEdit_18.text(), False) + ' and ' + wrap_condition('贷款号', self.lineEdit_20.text(), False) + ' and ' + wrap_condition('名字', self.lineEdit_21.text())

		self.query = 'update 账户 set ' + setting + ' where ' + self.before
		#确认更新
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
		if reply == QMessageBox.No: 
			return
		self.get_query(False)

	def select_loan(self): 
		if self.lineEdit_18.text() == '':
			money = '1 = 1'
		else:
			money = '金额1' + self.op[self.comboBox_6.currentIndex()] + self.lineEdit_18.text()
		self.query  = 'select * from 贷款 where ' + money + ' and ' + wrap_condition('贷款号', self.lineEdit_20.text(), False) + ' and ' + wrap_condition('名字', self.lineEdit_21.text())
		query_result = self.get_query(True)
		if host == 0 and query_result is not None:
			self.feed_table_loan(query_result)
		
	def double_click_loan(self, item, column):
		self.lineEdit_18.setText(item.text(1))
		self.comboBox_6.setCurrentIndex(0)
		self.lineEdit_20.setText(item.text(0))
		self.lineEdit_21.setText(item.text(2))
		self.before = wrap_condition('金额1', self.lineEdit_18.text(), False) + ' and ' + wrap_condition('贷款号', self.lineEdit_20.text(), False) + ' and ' + wrap_condition('名字', self.lineEdit_21.text())
	
	def clear_loan(self):
		self.lineEdit_18.setText('')
		self.comboBox_6.setCurrentIndex(1)
		self.lineEdit_20.setText('')
		self.lineEdit_21.setText('')

	def feed_table_loan(self, result):
		self.treeWidget_5.clear()
		L=[]
		for row in result:
			money = row[0]
			self.query = 'select 贷款.贷款号, sum(支付情况.金额1) from 贷款, 支付情况 where 贷款.贷款号 = 支付情况.贷款号 and 贷款.贷款号 = ' + str(row[1]) +' group by 贷款.贷款号'
			result = self.get_query(True)
			if result == [] or result[0][1] == 0:
				status = '未发放'
			elif result[0][1] < money:
				status = '发放中'
			else:
				status = '已全部发放'
			L.append(QTreeWidgetItem([str(row[1]), str(row[0]), str(row[2]), status]))
		self.treeWidget_5.addTopLevelItems(L)
	def pay_loan(self):
		if self.lineEdit_24.text() == '' or self.lineEdit_23.text() == '':
			self.error_input('输入发放贷款信息不足！')
			return 
		self.query = 'insert into 支付情况(贷款号, 身份证号, 金额1, 日期付款) values('+ wrap_value(self.lineEdit_20.text(), False) + ', ' + wrap_value(self.lineEdit_24.text()) + ', '  + wrap_value(self.lineEdit_23.text(), False) + ', str_to_date(' + wrap_value(QDate.currentDate().toString('yyyy/MM/dd')) + ', ' + wrap_value('%Y/%m/%d') + '))'
		#确认发放
		reply = QMessageBox.question(self, '确认', "确定执行操作?", QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
		if reply == QMessageBox.No: 
			return
		self.get_query(False)
	
	#------------------------statistic ----------------------------#
	def store_statistic(self):
		time_interval = '储蓄账户.开户日期 > str_to_date('+ wrap_value(self.dateEdit_3.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ' and 储蓄账户.开户日期 < str_to_date('+ wrap_value(self.dateEdit_4.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')'
		self.query = 'select 支行.名字,  COUNT(*), SUM(余额) from 支行, 储蓄开户, 储蓄账户 where 支行.名字 = 储蓄开户.名字 and 储蓄开户.账户号 = 储蓄账户.账户号' + ' and ' + time_interval + ' group by 支行.名字'
		query_result = self.get_query(True)
		if query_result is not None:
			self.treeWidget_6.clear()
			L = []
			for row in query_result:
				L.append(QTreeWidgetItem([str(row[0]), str(row[1]), str(row[2])]))
			self.treeWidget_6.addTopLevelItems(L)

	def clear_store_statistic(self):
		self.treeWidget_6.clear()
		
	def loan_statistic(self):
		time_interval = '贷款账户.开户日期 > str_to_date('+ wrap_value(self.dateEdit_6.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')' + ' and 贷款账户.开户日期 < str_to_date('+ wrap_value(self.dateEdit_7.date().toString("yyyy/MM/dd")) + ', ' + wrap_value('%Y/%m/%d') + ')'
		self.query = 'select 支行.名字,  COUNT(*), SUM(余额) from 支行, 贷款开户, 贷款账户 where 支行.名字 = 贷款开户.名字 and 贷款开户.账户号 = 贷款账户.账户号' + ' and ' + time_interval + ' group by 支行.名字'
		query_result = self.get_query(True)
		if query_result is not None:
			self.treeWidget_7.clear()
			L = []
			for row in query_result:
				L.append(QTreeWidgetItem([str(row[0]), str(row[1]), str(row[2])]))
			self.treeWidget_7.addTopLevelItems(L)

	def clear_loan_statistic(self):
		self.treeWidget_7.clear()
	
	
if __name__ == "__main__":
	try:
		import MySQLdb
	except:
		print("MySQLdb not installed!")
	
	try:
		db = MySQLdb.connect("localhost","lyp1234","1234","bank", charset = "utf8")
		cursor = db.cursor()
		print("Connected successfully!")
		host = 0
	except:
		host = 1
		print("Failed to connect the database!")
	
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = MainWindow()
	MainWindow.show()
	sys.exit(app.exec_())
	
	if host == 0:
		db.close()
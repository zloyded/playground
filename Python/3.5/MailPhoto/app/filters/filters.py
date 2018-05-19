'''Фильтры для шаблонов

    :param Date: дата
    :type Date: string
    :param Time: Время
    :type Time: string
    :param Phone: Номер телефона
    :type Phone: string
'''
from app import app
class Filters:
  @app.template_filter('timeTime')
  def time(time):
    ''' На входе стринг с неотформатированной датой
    
    :param str time: Неотформатированная дата
    :returns: str -- Часы в формате **часы:минуты:секунды** (str)
    '''
    time = str(time)
    res = time[0:2]+':'+time[2:4]+':'+time[4:6]
    return res
  
  @app.template_filter('date')
  def date(date):
    ''' На входе стринг с неотформатированной датой
  
    :param str date: Неотформатированная дата
    :returns: str -- Дата в формате **День/Месяц/Год (str)**
    '''
    date = str(date)
    res = date[0:4]+'/'+date[4:6]+'/'+date[6:8]
    return res

  @app.template_filter('phone')
  def phone(phone):
    ''' На входе стринг с неотформатированным номером телефонв
        
    :param str phone: Неотформатированный номер
    :returns: str -- Номер в формате: **+7 (123) 234-12-21**
    '''
    phone = str(phone)
    if len(phone) == 12:
      rephone = '+7 ('+phone[2:5] + ') ' + phone[5:8] +'-'+ phone[8:10] + '-' + phone[10:12]
    else: 
      rephone = '+7 ('+phone[1:4] + ') ' + phone[4:7] +'-'+ phone[7:9] + '-' + phone[9:11]
    return rephone

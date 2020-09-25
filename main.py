import datetime
import sqlite3


# convert miladi to shamsi
def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if gm > 2:
        gy2 = gy + 1
    else:
        gy2 = gy
    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) //
                                                     100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    jy = -1595 + (33 * (days // 12053))
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm = 1 + (days // 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + ((days - 186) // 30)
        jd = 1 + ((days - 186) % 30)
    return [jy, jm, jd]


def jalali_to_gregorian(jy, jm, jd):
    jy += 1595
    days = -355668 + (365 * jy) + ((jy // 33) * 8) + \
        (((jy % 33) + 3) // 4) + jd
    if (jm < 7):
        days += (jm - 1) * 31
    else:
        days += ((jm - 7) * 30) + 186
    gy = 400 * (days // 146097)
    days %= 146097
    if (days > 36524):
        days -= 1
        gy += 100 * (days // 36524)
        days %= 36524
        if (days >= 365):
            days += 1
    gy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        gy += ((days - 1) // 365)
        days = (days - 1) % 365
    gd = days + 1
    if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        kab = 29
    else:
        kab = 28
    sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    while (gm < 13 and gd > sal_a[gm]):
        gd -= sal_a[gm]
        gm += 1
    return [gy, gm, gd]


def diffNowDate(DateStr):
    from datetime import datetime
    fmt = '%Y-%m-%d'
    d2 = datetime.strptime(str(datetime.now().year)+'-' +
                           str(datetime.now().month)+'-'+str(datetime.now().day), fmt)
    d1 = datetime.strptime(DateStr, fmt)
    return (d2-d1).days


def calc_diff(d, m, y):
    greg = jalali_to_gregorian(y, m, d)
    form = str(greg[0])+'-'+str(greg[1])+'-'+str(greg[2])
    rm = diffNowDate(form)
    return -rm


conn = sqlite3.connect('data/hw.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS hw (
	day integer ,
	month integer ,
	year integer ,
	name char
)""")


current_time = datetime.datetime.now()
year = current_time.year
month = current_time.month
day = current_time.day

date_now = gregorian_to_jalali(year, month, day)

print('------------------------------------------{0}/{1}/{2}------------------------------------------\n\n\n'.format(
    date_now[0], date_now[1], date_now[2]))


selec = input('read or write or delete (r/w/d)')


if selec == 'w':
    homework_name = input('esm taklifet chie:  ')
    hw_day = input('che roozi baiad tahvil bedi:  ')
    hw_month = input('che mahy baiad tahvil bedi(n = this month):  ')
    hw_year = input('che sali mikhay tahvil bedi(n = this year):  ')
    hw_day = int(hw_day)
    hw_month = date_now[1] if hw_month == 'n' else int(hw_month)
    hw_year = date_now[0] if hw_year == 'n' else int(hw_year)
    c.execute("INSERT INTO hw VALUES ({0},{1},{2},'{3}')".format(
        hw_day, hw_month, hw_year, homework_name))
    conn.commit()


elif selec == 'r':
    c.execute("SELECT * FROM hw")
    hws = c.fetchall()
    conn.commit()
    for hw in hws:
        remain = calc_diff(hw[0], hw[1], hw[2])
        print('name:  {0}   Delivery Date:  {1}/{2}/{3}   remaining days:  {4}'.format(
            hw[3], hw[2], hw[1], hw[0], remain))
else:
    c.execute("SELECT * FROM hw")
    hws = c.fetchall()
    conn.commit()
    for hw in hws:
        remain = calc_diff(hw[0], hw[1], hw[2])
        print('name:  {0}   Delivery Date:  {1}/{2}/{3}   remaining days:  {4}\n\n\n\n'.format(
            hw[3], hw[2], hw[1], hw[0], remain))
    rm_name = input("enter name u want delete:  ")
    c.execute("DELETE FROM hw WHERE name='{0}'".format(rm_name))
    conn.commit()
    print('done!')
conn.close()
input()

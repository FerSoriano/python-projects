import gspread
import service_account

servie_account = service_account.get_service_account()

gc = gspread.service_account(servie_account)

wb = gc.open('Price Tracking')
ws = wb.worksheet('app')

print(ws.get_all_records())


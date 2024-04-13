from price_tracking import PriceTracking
import config

app = PriceTracking(service_account=config.get_service_account(), workbook='Price Tracking', worksheet='app')

if __name__ == '__main__':
    app.setConnection()
    app.getRecords()
    app.getPrices()
    app.transformPrices()
    app.updateWorksheet()

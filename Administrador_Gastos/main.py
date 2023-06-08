from class_file import AdminGastos
import clear_downloads as cd

conceptos_debito = {
            "Ingresos": ['abono/nomina', 'pago recibido', 'traspaso', 
                         'deposito en ventanilla', 'deposito por devolucion', 'disponible banamex'],
            "Gastos Fijos": ['pago de servicio', 'deposito inversion perfiles', 'microsoft', 'banco invex']
            }

conceptos_credito = {
            "Streaming": ['disney','spotify'],
            "Amazon": ['amazon'],
            "Mercado Libre": ['merpago', 'mercado pago'],
            "TicketMaster": ['ticketmaster'],
            "Pago Tarjeta": ['su abono']
            }

# cd.clear_downloads()
# tarjeta_debito = AdminGastos(nombre_tarjeta='debito', sheet_name='test',conceptos=conceptos_debito)
# tarjeta_debito.move_pdf()
# tarjeta_debito.extract_pdf_debito()
# tarjeta_debito.update_excel()

#TODO: Correr el proceso para todos los Edos de Cuenta.
#TODO: Validar y acomodar que los PDFs se vayan a su ruta correcta.
pdf_path_bsmart = 'C:\\Users\\fer8f\\Downloads\\Edos B_Smart\\EstadodeCuenta 20230501.pdf'
tarjeta_bsmart = AdminGastos(nombre_tarjeta='bsmart', sheet_name='records_bsmart'
                             ,conceptos=conceptos_credito, pdf_path= pdf_path_bsmart, year= '')
tarjeta_bsmart.extract_pdf_bsmart()
tarjeta_bsmart.update_excel()

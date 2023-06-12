from class_file import AdminGastos
import clear_downloads as cd

conceptos_debito = {
            "Ingresos": ['abono/nomina', 'pago recibido', 'traspaso', 
                         'deposito en ventanilla', 'deposito por devolucion', 'disponible banamex'],
            "Gastos Fijos": ['pago de servicio', 'deposito inversion perfiles', 'microsoft', 'banco invex']
            }

conceptos_credito = {
            "Streaming": ['disney','spotify','netflix'],
            "Amazon": ['amazon'],
            "Mercado Libre": ['merpago', 'mercado pago'],
            "TicketMaster": ['ticketmaster'],
            "Pago Tarjeta": ['su abono'],
            "QuickLearning": ['ql del'],
            "Prestamo Credito":['disponible citibanamex'],
            "Intereses":['interes', 'iva', 'comision ext']
            }


cd.clear_downloads()

# TARJETA DEBITO
tarjeta_debito = AdminGastos(nombre_tarjeta='debito', sheet_name='records_debito',conceptos=conceptos_debito)
tarjeta_debito.move_pdf()
tarjeta_debito.extract_pdf_debito()
tarjeta_debito.update_excel()


# TARJETA B-SMART
tarjeta_bsmart = AdminGastos(nombre_tarjeta='bsmart', sheet_name='records_bsmart'
                             ,conceptos=conceptos_credito, pdf_name='EstadodeCuenta_BSmart.pdf', year= '')
tarjeta_bsmart.move_pdf()
tarjeta_bsmart.extract_pdf_credito()
tarjeta_bsmart.update_excel()


# TARJETA SIMPLICITY
tarjeta_simplicity = AdminGastos(nombre_tarjeta='simplicity',sheet_name='records_simplicity'
                                 ,conceptos=conceptos_credito, pdf_name='EstadodeCuenta_Simplicity.pdf' ,year='')
tarjeta_simplicity.move_pdf()
tarjeta_simplicity.extract_pdf_credito()
tarjeta_simplicity.update_excel()



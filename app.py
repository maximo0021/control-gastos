
import os
import datetime

def mostrar_menu():
    print("\n--- CONTROL DE GASTOS PERSONALES ---")
    print("1. Registrar nuevos gastos (Modo Continuo)")
    print("2. Ver historial de gastos")
    print("3. Ver total gastado por categoría")
    print("4. Borrar un gasto")
    print("5. Salir")

def cargar_gastos():
    lista_gastos = []
    if not os.path.exists("gastos.csv"):
        return lista_gastos
    
    try:
        with open("gastos.csv", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    partes = linea.split(",")
                    if len(partes) == 4:
                        fecha, concepto, monto_str, categoria = partes
                        gasto = {
                            "fecha": fecha,
                            "concepto": concepto,
                            "monto": float(monto_str),
                            "categoria": categoria
                        }
                        lista_gastos.append(gasto)
    except Exception as e:
        print(f"⚠️ Error al cargar los datos: {e}")
        
    return lista_gastos

def guardar_gastos(lista_gastos):
    try:
        with open("gastos.csv", "w", encoding="utf-8") as archivo:
            for gasto in lista_gastos:
                linea = f"{gasto['fecha']},{gasto['concepto']},{gasto['monto']},{gasto['categoria']}\n"
                archivo.write(linea)
    except Exception as e:
        print(f"❌ Error al guardar los datos: {e}")

def registrar_gastos_multiples(lista_gastos):
    print("\n-- Registro de Gastos (Modo Continuo) --")
    print("Escribe 'salir' en cualquier concepto cuando termines.\n")
    
    contador_nuevos = 0
    while True:
        concepto = input("Ingrese el concepto (Nafta, steam, comida, etc.) (o 'salir'): ").strip()
        
        if concepto.lower() == "salir":
            print("Saliendo del registro de gastos...")
            break
        
        try:
            monto = float(input("Ingrese el monto: $"))
        except ValueError:
            print("❌ Error: Ingrese un número válido para el monto. Intente este gasto de nuevo.\n")
            continue 

        print("Categorías sugeridas: comida, transporte, servicios, salidas, otros")
        categoria = input("Ingrese la categoría: ").strip().lower()

        fecha_actual = datetime.date.today().strftime("%Y-%m-%d")

        gasto = {
            "fecha": fecha_actual,
            "concepto": concepto,
            "monto": monto,
            "categoria": categoria
        }

        lista_gastos.append(gasto)
        contador_nuevos += 1
        print(f"✅ Gasto '{concepto}' agregado a la lista temporal.\n")
    
    # Si cargó al menos uno, guardamos todo de golpe en el CSV
    if contador_nuevos > 0:
        guardar_gastos(lista_gastos)
        print(f"💾 Se guardaron {contador_nuevos} nuevos gastos en el archivo.")

def mostrar_historial(lista_gastos):
    print("\n-- Historial de Gastos --")
    if not lista_gastos:
        print("⚠️ No hay gastos registrados aún.")
        return

    total = 0
    for i, gasto in enumerate(lista_gastos, 1):
        print(f"{i}. [{gasto['fecha']}] {gasto['concepto']} | Categ: {gasto['categoria']} | ${gasto['monto']:.2f}")
        total += gasto["monto"]
    
    print("-" * 45)
    print(f"TOTAL GASTADO: ${total:.2f}")

def borrar_gasto(lista_gastos):
    print("\n-- Borrar un Gasto --")
    if not lista_gastos:
        print("⚠️ No hay gastos para borrar.")
        return

    mostrar_historial(lista_gastos)
    try:
        indice = int(input("\nIngrese el número del gasto que desea eliminar: ")) - 1
        if 0 <= indice < len(lista_gastos):
            gasto_eliminado = lista_gastos.pop(indice)
            guardar_gastos(lista_gastos)
            print(f"🗑️ Gasto '{gasto_eliminado['concepto']}' eliminado con éxito.")
        else:
            print("❌ Número de gasto inválido.")
    except ValueError:
        print("❌ Por favor, ingrese un número válido.")

def reporte_por_categoria(lista_gastos):
    print("\n-- Gastos por Categoría --")
    if not lista_gastos:
        print("⚠️ No hay gastos registrados aún.")
        return

    totales_cat = {}
    for gasto in lista_gastos:
        cat = gasto["categoria"]
        monto = gasto["monto"]
        totales_cat[cat] = totales_cat.get(cat, 0) + monto

    for cat, total in totales_cat.items():
        print(f"* {cat.capitalize()}: ${total:.2f}")

def main():
    gastos = cargar_gastos()
    print(f"📂 Se cargaron {len(gastos)} gastos previos.")
    
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-5): ")

        if opcion == "1":
            registrar_gastos_multiples(gastos)
        elif opcion == "2":
            mostrar_historial(gastos)
            input("\nPresiona ENTER para volver al menú...")
        elif opcion == "3":
            reporte_por_categoria(gastos)
            input("\nPresiona ENTER para volver al menú...")
        elif opcion == "4":
            borrar_gasto(gastos)
            input("\nPresiona ENTER para volver al menú...")
        elif opcion == "5":
            print("\n¡Gracias por usar el Control de Gastos! Hasta luego.")
            break
        else:
            print("❌ Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
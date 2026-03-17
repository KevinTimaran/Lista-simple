class NodoTarea:
    def __init__(self, identificador, descripcion):
        self.id = identificador
        self.descripcion = descripcion
        self.completada = False
        self.siguiente = None


class ListaEnlazadaTareas:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamano = 0
        self._id_actual = 1

    def agregar_tarea(self, descripcion):
        nueva_tarea = NodoTarea(self._id_actual, descripcion)
        self._id_actual += 1

        if self.cabeza is None:
            self.cabeza = nueva_tarea
            self.cola = nueva_tarea
        else:
            self.cola.siguiente = nueva_tarea
            self.cola = nueva_tarea

        self.tamano += 1
        return nueva_tarea

    def marcar_completada(self, identificador):
        actual = self.cabeza

        while actual is not None:
            if actual.id == identificador:
                actual.completada = True
                return True
            actual = actual.siguiente

        return False

    def construir_texto_tareas(self):
        if self.cabeza is None:
            return "No hay tareas en la lista."

        actual = self.cabeza
        salida = ""

        while actual is not None:
            estado = "Completada" if actual.completada else "Pendiente"
            salida += f"ID: {actual.id} | {actual.descripcion} | Estado: {estado}\n"
            actual = actual.siguiente

        return salida

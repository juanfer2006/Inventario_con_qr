class CampoVacioError(Exception):
    def __init__(self, mensaje="Todos los campos son obligatorios."):
        super().__init__(mensaje)


class CantidadInvalidaError(Exception):
    def __init__(self, mensaje="La cantidad debe ser un número positivo."):
        super().__init__(mensaje)

class BaseModule:
    name: str = "anonymous"

    def __init__(self, params: dict):
        self.params = params

    def process(self, ssh_client):
        """Applique l'action à `ssh_client` en utilisant `params`."""
        raise NotImplementedError(
            "La méthode 'process' doit être implémentée dans la classe dérivée.")

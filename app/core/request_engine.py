import requests

class Request:
    """Classe qui encapsule une requête HTTP"""
    def __init__(self):
        self.url = ""
        self.method = "GET"
        self.params = {}
        self.headers = {}
        self.cookies = {}
        self.last_response = None
        self.content_type = None
        self.status_code = None
        
    def set_url(self, url):
        self.url = url
        
    def set_method(self, method):
        self.method = method
        
    def set_params(self, params):
        self.params = params
        
    def set_headers(self, headers):
        self.headers = headers

    def set_cookies(self, cookies):
        self.cookies = cookies 
        
    def send(self):
        """Envoie la requête HTTP et retourne la réponse"""
        try:
            # Préparer les headers et les cookies
            headers = self.headers if self.headers else {}
            cookies = self.cookies if self.cookies else {}

            # Envoi de la requête selon la méthode
            if self.method == "GET":
                r = requests.get(self.url, params=self.params, headers=headers, cookies=cookies, timeout=10)
            elif self.method == "POST":
                r = requests.post(self.url, data=self.params, headers=headers, cookies=cookies, timeout=10)
            elif self.method == "PUT":
                r = requests.put(self.url, data=self.params, headers=headers, cookies=cookies, timeout=10)
            elif self.method == "DELETE":
                r = requests.delete(self.url, data=self.params, headers=headers, cookies=cookies, timeout=10)
            elif self.method == "PATCH":
                r = requests.patch(self.url, data=self.params, headers=headers, cookies=cookies, timeout=10)
            elif self.method == "HEAD":
                r = requests.head(self.url, params=self.params, headers=headers, cookies=cookies, timeout=10)
            else:
                raise ValueError("Méthode HTTP non supportée")
            
            # Stockage des résultats
            self.last_response = r.text
            self.content_type = r.headers.get('Content-Type', '')
            self.status_code = r.status_code
            
            return r
        
        except Exception as e:
            self.last_response = f"Erreur: {str(e)}"
            self.content_type = "text/plain"
            self.status_code = None
            raise e
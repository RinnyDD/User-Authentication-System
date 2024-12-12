ord):
            return False
        if not re.search(r'[a-z]', password) or not re.search(r'\d', password):
            return False
        if not re.search(r'[@$!%*?&#]', password):
            return False
        return True
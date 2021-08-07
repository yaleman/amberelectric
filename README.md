# Archived

This project is no longer in development, I transferred ownership of the `amberelectric` Python package to Amber themselves.

# amberelectric 

Basic Amber Electric API munger, pulls usage data and pricing from your account.

Check out `example.py` for how to use this, or example code here:

    import json
    from amberelectric import AmberElectric

    API = AmberElectric(username='frank@example.com', password='hunter2')
    API.auth()

    pricelist = API.getpricelist()
    print(json.dumps(pricelist, indent=2))

import requests
from django.conf import settings
from supabase import create_client, Client
from django.utils.http import urlencode

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_KEY
headers = {
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SUPABASE_KEY}",
}
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_from_supabase(endpoint):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    response = requests.get(url, headers=headers)
    return response.json()

def new_insert_to_supabase(table, data):
    try:
        response = supabase.table(table).insert(data).execute()
        # Supabase's .execute() typically returns a dict with a 'data' key
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Supabase insertion error: {e}")
        return None

def insert_to_supabase(endpoint, data):
    try:
        url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
        response = requests.post(url, json=data, headers=headers)
        print(response)
        response.raise_for_status()
        return data  # Return the inserted data if successful
    except Exception as e:
        print(f"Supabase insertion error: {e}")
        raise 
    
def update_to_supabase(endpoint, data):
    try:
        url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
        response = requests.put(url, json=data, headers=headers)
        return data
    
    except Exception as e:
        print(f"Supabase update error: {e}")
        raise 
    
def delete_from_supabase(endpoint, data):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}?email=eq.{data['email']}"
    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
        return {"error": f"Failed to delete user. Status code: {response.status_code}", "details": data}
    return {"success": f"Succed to delete user. Status code: {response.status_code}", "details": data}
   
def getuserby_Id_from_supabase(endpoint, data):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}?id=eq.{data['id']}"
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code != 200:
        return {"error": f"Failed to get user. Status code: {response.status_code}", "details": response.json()}
    return {"success": f"Succed to get user. Status code: {response.status_code}", "details": response.json()}
   
def getuserPost_by_Id_from_supabase(endpoint, data):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}?user_id=eq.{data['user_id']}"
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code != 200:
        return {"error": f"Failed to get user. Status code: {response.status_code}", "details": response.json()}
    return {"success": f"Succed to get user. Status code: {response.status_code}", "details": response.json()}
   
def updateuser_profil_by_Id_from_supabase(endpoint, data):
    print(f"voici le user_id de la fonction PutUser {data['profil_id']}")
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}?profil_id=eq.{data['profil_id']}"
    response = requests.put(url, json=data, headers=headers)
    return response.json()




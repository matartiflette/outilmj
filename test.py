import asyncio
import websockets

async def send_message():
    uri = "ws://192.168.0.72:8765"  # Remplace 'adresse_ip_serveur' par l'IP du serveur
    async with websockets.connect(uri) as websocket:
        message = "Joueur sélectionné"  # Le message que tu veux envoyer
        await websocket.send(message)  # Envoie du message au serveur

        # Attente de la réponse du serveur
        response = await websocket.recv()
        print(f"Réponse du serveur: {response}")

asyncio.get_event_loop().run_until_complete(send_message())

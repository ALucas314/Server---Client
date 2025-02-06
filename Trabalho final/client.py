import socket

# Configurações do cliente
HOST = "127.0.0.1"
PORT = 5001

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    while True:
        # Exibir menu de opções
        voto = input("Digite '1' para votar em Elon Musk, '2' para votar em Steve Jobs ou 'sair' para encerrar: ")
        
        # Enviar voto ao servidor
        client.send(voto.encode())
        
        # Receber resposta do servidor
        resposta = client.recv(1024).decode()
        print(resposta)
        
        if voto.lower() == "sair":
            print("Saindo do sistema...")
            break
    
    client.close()

if __name__ == "__main__":
    main()

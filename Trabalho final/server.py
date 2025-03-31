import socket
import threading

# Configurações do servidor
HOST = "127.0.0.1"
PORT = 5001

# Dicionário para armazenar votos
votos = {"Elon Musk": 0, "Steve Jobs": 0}

# Lock para proteger o acesso ao dicionário de votos em ambiente multi-thread
voto_lock = threading.Lock()

# Função para gerenciar as conexões
def handle_connection(conn, addr):
    print(f"Conexão estabelecida com {addr}")
    
    while True:
        # Enviar as opções de votação
        conn.send("Escolha um candidato para votar: \n1. Elon Musk\n2. Steve Jobs\nDigite 'sair' para encerrar.\n".encode())
        
        # Receber o voto
        voto = conn.recv(1024).decode().strip()
        
        if voto.lower() == "sair":
            print(f"Conexão encerrada com {addr}")
            break

        with voto_lock:
            if voto == "1":
                votos["Elon Musk"] += 1
                resposta = "Voto registrado para Elon Musk!"
            elif voto == "2":
                votos["Steve Jobs"] += 1
                resposta = "Voto registrado para Steve Jobs!"
            else:
                resposta = "\nOpção inválida. Voto não registrado.\n"

        print(f"Resultado parcial da votação: {votos}" if voto in ["1", "2"] else f"Opção inválida recebida: {voto}")
        
        # Enviar resposta para o cliente
        conn.send(resposta.encode())

    conn.close()
    
    print("\nResultado final da votação:")
    print(f"Elon Musk: {votos['Elon Musk']} votos")
    print(f"Steve Jobs: {votos['Steve Jobs']} votos")

# Função principal do servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Servidor de votação iniciado em {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_connection, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()

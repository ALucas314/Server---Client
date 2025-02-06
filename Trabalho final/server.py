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
        
        # Verificar o voto e registrar com lock para evitar condições de corrida
        if voto == "1":
            with voto_lock:
                votos["Elon Musk"] += 1
            resposta = "Voto registrado para Elon Musk!"
        elif voto == "2":
            with voto_lock:
                votos["Steve Jobs"] += 1
            resposta = "Voto registrado para Steve Jobs!"
        else:
            resposta = "Opção inválida. Voto não registrado."
        # Exibir o resultado parcial ou inválido
        print(f"Resultado parcial da votação: {votos}" if voto in ["1", "2"] else f"Opção inválida: {votos}")
        
        # Enviar resposta para o cliente
        conn.send(resposta.encode())

    conn.close()
    
    # Exibir o resultado final quando a conexão for encerrada
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
        # Aguardar uma nova conexão
        conn, addr = server.accept()
        # Criar uma nova thread para cada conexão
        threading.Thread(target=handle_connection, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()

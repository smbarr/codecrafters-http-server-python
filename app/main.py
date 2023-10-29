# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client

    with conn:
        _bytes = conn.recv(144)
        data = _bytes.decode("utf-8")
        path = data.split("\n")[0].split()[1]

        resp_code = "200 OK" if path == "/" else "404 Not Found"
        resp = f"HTTP/1.1 {resp_code}\r\n\r\n"
        conn.sendall(resp.encode('utf-8'))


if __name__ == "__main__":
    main()

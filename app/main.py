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
        page = path.split("/")[-1].strip()

        # resp_code = "200 OK" if path == "/" else "404 Not Found"
        resp_code = "200 OK"
        contentLength = len(page)

        resp = "\r\n".join([
            f"HTTP/1.1 {resp_code}",
            "Content-Type: text/plain",
            f"Content-Length: {contentLength}",
            "",
            page
        ])
        print(resp)

        conn.sendall(resp.encode('utf-8'))


if __name__ == "__main__":
    main()

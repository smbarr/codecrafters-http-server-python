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

        echo = False
        rngStr = ""
        if "/" in path:
            if len(path.split("/")) > 1:
                head = path.split("/")[1].strip()
                if head == "echo":
                    echo  = True
                    rngStr = path.split("/")[2].strip()

        resp_code = "200 OK" if (path == "/" or echo) else "404 Not Found"
        contentLength = 0
        if echo:
            contentLength = len(rngStr)

        resp = "\r\n".join([
            f"HTTP/1.1 {resp_code}",
            "Content-Type: text/plain",
            f"Content-Length: {contentLength}",
            "",
            rngStr
        ])
        print(resp)

        conn.sendall(resp.encode('utf-8'))


if __name__ == "__main__":
    main()

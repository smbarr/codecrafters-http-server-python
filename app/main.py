# Uncomment this to pass the first stage
import os
import socket
import threading

def handle_client(conn):
        _bytes = conn.recv(144)
        data = _bytes.decode("utf-8")
        dataLines = data.split("\n")
        path = dataLines[0].split()[1]

        def getResp():
            if "/" in path:
                if len(path.split("/")) > 1:
                    head = path.split("/")[1].strip()
                    if head == "echo":
                        rngStr = "/".join(path.split("/")[2:])
                        contentLength = len(rngStr)
                        resp = "\r\n".join([
                            f"HTTP/1.1 200 OK",
                            ""
                            "Content-Type: text/plain",
                            f"Content-Length: {contentLength}",
                            "",
                            rngStr
                        ])
                        return resp
                    elif head == "user-agent":
                        user_agent = None
                        for line in dataLines:
                            if "User-Agent" in line:
                                user_agent = line.split(":")[1].strip()
                        contentLength = len(user_agent)
                        resp = "\r\n".join([
                            f"HTTP/1.1 200 OK",
                            ""
                            "Content-Type: text/plain",
                            f"Content-Length: {contentLength}",
                            "",
                            user_agent
                        ])
                        return resp
                    elif head == "files":
                        filePath = "/".join(path.split("/")[2:])
                        print(filePath)
                        if os.path.isfile(filePath):
                            with open(filePath) as f:
                                fileData = f.read()
                            resp = "\r\n".join([
                                f"HTTP/1.1 200 OK",
                                ""
                                "Content-Type: application/octet-stream",
                                f"Content-Length: {len(fileData)}",
                                "",
                                fileData
                            ])
                            print(resp)
                        else:
                            resp = "\r\n".join([
                                f"HTTP/1.1 404 Not Found",
                                ""
                                "Content-Type: application/octet-stream"
                            ])
                            print(resp)
                        return resp


                    
            resp_code = "200 OK" if path == "/" else "404 Not Found"
            resp = "\r\n".join([
                f"HTTP/1.1 {resp_code}",
                ""
                "Content-Type: text/plain",
                "", ""
            ])
                    
            return resp

        resp = getResp()
        conn.send(resp.encode('utf-8'))
        conn.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        conn, addr = server_socket.accept() # wait for client
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()


if __name__ == "__main__":
    main()

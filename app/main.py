# Uncomment this to pass the first stage
import os
import sys
import socket
import threading

def handle_client(conn, directory):
        _bytes = conn.recv(1024)
        data = _bytes.decode("utf-8")
        dataLines = data.split("\r\n")
        method = dataLines[0].split()[0].strip()
        path = dataLines[0].split()[1].strip()

        def getResp():
            if "/" in path:
                if len(path.split("/")) > 1:
                    head = path.split("/")[1].strip()
                    if head == "echo":
                        rngStr = "/".join(path.split("/")[2:])
                        contentLength = len(rngStr)
                        resp = "\r\n".join([
                            f"HTTP/1.1 200 OK",
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
                            "Content-Type: text/plain",
                            f"Content-Length: {contentLength}",
                            "",
                            user_agent
                        ])
                        return resp
                    elif head == "files":
                        fileName = directory+path.split("/")[2]
                        if method == "GET":
                            if os.path.isfile(fileName):
                                with open(fileName) as f:
                                    fileData = f.read()
                                resp = "\r\n".join([
                                    f"HTTP/1.1 200 OK",
                                    "Content-Type: application/octet-stream",
                                    f"Content-Length: {len(fileData)}",
                                    "",
                                    fileData
                                ])
                                print(resp)
                            else:
                                resp = "\r\n".join([
                                    f"HTTP/1.1 404 Not Found",
                                    "Content-Type: text/plain",
                                    "Content-Length: 0",
                                    "", ""
                                ])
                                print(resp)
                            return resp
                        elif method == "POST":
                            body = dataLines[-1]
                            print(body)
                            print(dataLines)
                            with open(fileName, 'w') as f:
                                f.write(body)
                            resp = "\r\n".join([
                                f"HTTP/1.1 201",
                                "Content-Type: text/plain",
                                "Content-Length: 0",
                                "", ""
                            ])    
                            return resp
                    
            resp_code = "200 OK" if path == "/" else "404 Not Found"
            resp = "\r\n".join([
                f"HTTP/1.1 {resp_code}",
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

    directory = None
    if len(sys.argv) > 0:
        for n in range(len(sys.argv)):
            if sys.argv[n] == "--directory":
                directory = sys.argv[n+1]

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        conn, addr = server_socket.accept() # wait for client
        client_thread = threading.Thread(target=handle_client, args=(conn,directory,))
        client_thread.start()


if __name__ == "__main__":
    main()

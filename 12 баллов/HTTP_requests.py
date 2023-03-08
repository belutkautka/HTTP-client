import socket

class request:
    def __init__(self):
        self.text=""
    def get(self,url,dict:dict):
        self.make_request("GET",url,dict)
    def post(self,url,dict:dict):
        self.make_request("POST", url, dict)
    def request(self,host,msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            port = 80
            s.connect((host, port))
            msg = bytearray(msg.encode(errors='ignore'))
            s.sendall(msg)
            answer=bytearray()
            while True:
                answ = s.recv(4028)
                if not answ:
                    break
                answer.extend(answ)
            all=str(bytes(answer).decode(errors='ignore'))
            start=all.find('<html>')
            self.text=all[start+6:]

    def format_params(self,params:dict):
        return '?' + self.format("&",params)
    def format_cookies(self,cookies:dict):
        return "Cookie: "+self.format("; ",cookies)
    def format(self,symbol,dict:dict):
            return symbol.join([f'{key}={dict[key]}' for key in dict])
    def format_file(self,name,value,boundary):
        return f'\r\nContent-Disposition: form-data; name="{name}"; filename="{name}"'\
               + f'\r\n\r\n{value}\r\n--{boundary}'
    def make_request(self,type,url,dict):
        request_data=[]
        request_line = type + " "
        index = url.find("/")
        if index==-1:
            Host=url
            request_line += "/"
        else:
            Host, pages = url[:index], url[index:]
            request_line +=pages

        if 'params' in dict.keys():
            request_line+=self.format_params(dict['params'])
        request_line += " HTTP/1.1"
        request_data.append(request_line)
        host=f"Host: {Host}"
        request_data.append(host)
        conection="Connection: close"
        request_data.append(conection)
        if 'cookies' in dict.keys():
            request_data.append(self.format_cookies(dict['cookies']))
        if 'headers' in dict.keys():
            for header in dict['headers']:
                request_data.append(header+": "+dict['headers'][header])
        if 'data' in dict.keys():
            request_data.append("Content-Type: application/x-www-form-urlencoded")
            data=self.format("&",dict['data'])
            request_data.append(f"Content-Length: {len(bytearray(data.encode(errors='ignore')))}"+"\r\n")
            request_data.append(data)
        if 'files' in dict.keys():
            boundary=str(7373737373737)
            request_data.append(f"Content-Type: multipart/form-data; boundary={boundary}")
            files=f"--{boundary}"
            for file in dict['files'].keys():
                files+=self.format_file(file,dict['files'][file],boundary)
            files+="--"
            request_data.append(f"Content-Length: {len(bytearray(files.encode(errors='ignore')))}"+"\r\n")
            request_data.append(files)
        self.request(Host,"\r\n".join(request_data)+"\r\n\r\n")

var arguments = process.argv.splice(2);
var socketPort = Number(arguments[0]); //minicap websocket port
var pcPort = Number(arguments[1]);  // minicap pc port

var WebSocketServer = require('ws').Server
    , http = require('http')
    , express = require('express')
    , path = require('path')
    , net = require('net')
    , app = express();

//minicap websocketServer
var PORT = process.env.PORT || pcPort;
app.use(express.static(path.join(__dirname, '/public')));
var server = http.createServer(app);
var wss = new WebSocketServer({server: server});
wss.on('connection', function (ws) {

    console.info('Got a minitouch client');

    // connect minitouch
    var stream = net.connect({
        port: socketPort
    });

    stream.on('error', function () {
        console.error('Be sure to run `adb forward tcp:PcTouchPort localabstract:minitouch`');
        process.exit(1)
    });

    // send message to minitouch
    ws.on('message', function (message) {
        stream.write(message);
        stream.write('c\n');
    });

    ws.on('close', function () {
        console.info('Lost a client');
        stream.end()
    })
});

server.listen(PORT);
console.info('Listening on minitouchPC port %d', PORT);


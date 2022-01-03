
var ws = new WebSocket("ws://127.0.0.1:8003/ws");

var container = document.getElementById('container')

ws.onmessage = function(event) {
    console.log(event.data)
    obj = JSON.parse(event.data)

    var e = document.createElement('div');
    var t = document.createTextNode(obj.account + ' ' + obj.balance + ' EUR (' + obj.modeloutput + ')');

    e.appendChild(t);

    if (obj.account != undefined) {
      container.appendChild(e);
    }
    // if(!(obj.name in lines)) {
    //   lines[obj.name] = {"latlon": []};
    //   lines[obj.name]["latlon"].push([obj.lat, obj.lon]);
    //   lines[obj.name]["config"] = {"color": colors[Math.floor(Math.random()*colors.length)]};
    // }
    // else {
    //   lines[obj.name]["latlon"].push([obj.lat, obj.lon]);
    // }

    // line = L.polyline(lines[obj.name]["latlon"], {color: lines[obj.name]["config"]["color"]})
    // linesLayer.addLayer(line)
    // map.addLayer(linesLayer);

};
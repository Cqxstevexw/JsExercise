function get_data_video(video_str) {
    var d = "jquery"
        , e = "support"
        , f = "constants"
        , g = "base64"
        , h = "substring"
        , i = "split"
        , j = "replace"
        , k = "substr";

    this.getHex = function (a) {
        return {
            str: a[h](4),
            hex: a[h](0, 4)[i]("").reverse().join("")
        }
    };

    this.getDec = function (a) {
        var b = parseInt(a, 16).toString();
        return {
            pre: b[h](0, 2)[i](""),
            tail: b[h](2)[i]("")
        }
    };
    this.substr = function (a, b) {
        var c = a[h](0, b[0])
            , d = a[k](b[0], b[1]);
        return c + a[h](b[0])[j](d, "")
    };
    this.getPos = function (a, b) {
        b[0] = a.length - b[0] - b[1];
        return b
    };

    this.atob = function (a) {
        var e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
        if (a = a.replace(/=+$/, ""), a.length % 4 == 1)
            throw f;
        for (var b, c, d = 0, g = 0, h = ""; c = a.charAt(g++); ~c && (b = d % 4 ? 64 * b + c : c,
        d++ % 4) ? h += String.fromCharCode(255 & b >> (-2 * d & 6)) : 0)
            c = e.indexOf(c);
        return h
    };

    this.decode = function (a) {
        var b = this.getHex(a)
            , c = this.getDec(b.hex)
            , d = this[k](b.str, c.pre);
        var zz = this[k](d, this.getPos(d, c.tail));
        console.log(zz);
        var src = this.atob(zz);
        console.log(src);
        return src
    };
    return this.decode(video_str)
}

// video_str = "8050aE5HR0cDovL212dmlkZW8xMS5tZWl0dWRhdGEuY29tLzVjZjUxYjllMzU3ZTcyNDM2X0gyNjRfTVA1Y2Y1NDYubXA0P2s9ZDlkZjU2MDQ5MzMzNzhjNGI1MmNlZGRmMzc2MTljOGUmdD01ZDFkT8vRLEK6YjQxZQ=="
// aHR0cDovL212dmlkZW8xMS5tZWl0dWRhdGEuY29tLzVjZjUxYjllMzU3ZTcyNDM2X0gyNjRfTVA1Y2Y1NDYubXA0P2s9ZDlkZjU2MDQ5MzMzNzhjNGI1MmNlZGRmMzc2MTljOGUmdD01ZDFkYjQxZQ==
// http://mvvideo11.meitudata.com/5cf51b9e357e72436_H264_MP5cf546.mp4?k=d9df5604933378c4b52ceddf37619c8e&t=5d1db41e


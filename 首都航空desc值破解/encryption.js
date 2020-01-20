var a_obj = {
    init: function (e, r) {
        e = this.words = e || [];
        if (r != null) {
            this.sigBytes = r
        } else {
            this.sigBytes = e.length * 4
        }
    }
};

function parse_l_parse(e) {
    return l_parse(unescape(encodeURIComponent(e)))
}

function l_parse(e) {
    for (var t = e.length, r = [], i = 0; i < t; i++)
        r[i >>> 2] |= (e.charCodeAt(i) & 255) << 24 - 8 * (i % 4);
    return new a_obj.init(r, t)
}

function doReset_finalize(_key, _e) {
    this._xformMode = 1;
    this._key = _key;
    this._data = new a_obj.init();
    this._nDataBytes = 0;
    this.blockSize = 4;
    this._keySchedule = [];

    for (var i = [], n = [], o = [], a = [], s = [], c = [], l = [], h = [], u = [], f = [], p = [], d = 0; 256 > d; d++)
        p[d] = 128 > d ? d << 1 : d << 1 ^ 283;
    for (var y = 0, g = 0, d = 0; 256 > d; d++) {
        var v = g ^ g << 1 ^ g << 2 ^ g << 3 ^ g << 4
            , v = v >>> 8 ^ v & 255 ^ 99;
        i[y] = v;
        n[v] = y;
        var _ = p[y]
            , m = p[_]
            , k = p[m]
            , w = 257 * p[v] ^ 16843008 * v;
        o[y] = w << 24 | w >>> 8;
        a[y] = w << 16 | w >>> 16;
        s[y] = w << 8 | w >>> 24;
        c[y] = w;
        w = 16843009 * k ^ 65537 * m ^ 257 * _ ^ 16843008 * y;
        l[v] = w << 24 | w >>> 8;
        h[v] = w << 16 | w >>> 16;
        u[v] = w << 8 | w >>> 24;
        f[v] = w;
        y ? (y = _ ^ p[p[p[k ^ _]]],
            g ^= p[p[g]]) : y = g = 1
    }
    var S = [0, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54];

    this._doReset = function () {
        for (var e = this._key, t = e.words, r = e.sigBytes / 4, e = 4 * ((this._nRounds = r + 6) + 1), n = this._keySchedule = [], o = 0; o < e; o++)
            if (o < r)
                n[o] = t[o];
            else {
                var a = n[o - 1];
                o % r ? 6 < r && 4 == o % r && (a = i[a >>> 24] << 24 | i[a >>> 16 & 255] << 16 | i[a >>> 8 & 255] << 8 | i[a & 255]) : (a = a << 8 | a >>> 24,
                    a = i[a >>> 24] << 24 | i[a >>> 16 & 255] << 16 | i[a >>> 8 & 255] << 8 | i[a & 255],
                    a ^= S[o / r | 0] << 24);
                n[o] = n[o - r] ^ a
            }
        t = this._invKeySchedule = [];
        for (r = 0; r < e; r++)
            o = e - r,
                a = r % 4 ? n[o] : n[o - 4],
                t[r] = 4 > r || 4 >= o ? a : l[i[a >>> 24]] ^ h[i[a >>> 16 & 255]] ^ u[i[a >>> 8 & 255]] ^ f[i[a & 255]]
    };

    this._data.concat = function (e) {
        var t = this.words
            , r = e.words
            , i = this.sigBytes;
        e = e.sigBytes;
        this.clamp = function () {
            var t = this.words
                , r = this.sigBytes;
            t[r >>> 2] &= 4294967295 << 32 - 8 * (r % 4);
            t.length = Math.ceil(r / 4)
        };
        this.clamp();
        if (i % 4)
            for (var n = 0; n < e; n++)
                t[i + n >>> 2] |= (r[n >>> 2] >>> 24 - 8 * (n % 4) & 255) << 24 - 8 * ((i + n) % 4);
        else if (65535 < r.length)
            for (n = 0; n < e; n += 4)
                t[i + n >>> 2] = r[n >>> 2];
        else
            t.push.apply(t, r);
        this.sigBytes += e;
        return this
    };

    this._append = function (e) {
        "string" == typeof e && (e = parse_l_parse(e));
        this._data.concat(e);
        this._nDataBytes += e.sigBytes
    };

    this.pad = function (e, t) {
        for (var r = 4 * t, r = r - e.sigBytes % r, i = r << 24 | r << 16 | r << 8 | r, o = [], a = 0; a < r; a += 4)
            o.push(i);
        r = new a_obj.init(o, r);
        e.concat(r)
    };

    this._process = function (t) {
        this._minBufferSize = 0;
        var r = this._data
            , i = r.words
            , n = r.sigBytes
            , o = this.blockSize
            , s = n / (4 * o)
            , s = t ? Math.ceil(s) : Math.max((s | 0) - this._minBufferSize, 0);
        t = s * o;
        n = Math.min(4 * t, n);
        if (t) {
            for (var c = 0; c < t; c += o)
                this._doProcessBlock(i, c);
            c = i.splice(0, t);
            r.sigBytes -= n
        }
        return new a_obj.init(c, n)
    };

    this._doProcessBlock = function (e, t) {
        this._doCryptBlock(e, t, this._keySchedule, o, a, s, c, i)
    };
    this._doCryptBlock = function (e, t, r, i, n, o, a, s) {
        for (var c = this._nRounds, l = e[t] ^ r[0], h = e[t + 1] ^ r[1], u = e[t + 2] ^ r[2], f = e[t + 3] ^ r[3], p = 4, d = 1; d < c; d++)
             var y = i[l >>> 24] ^ n[h >>> 16 & 255] ^ o[u >>> 8 & 255] ^ a[f & 255] ^ r[p++]
                 , g = i[h >>> 24] ^ n[u >>> 16 & 255] ^ o[f >>> 8 & 255] ^ a[l & 255] ^ r[p++]
                 , v = i[u >>> 24] ^ n[f >>> 16 & 255] ^ o[l >>> 8 & 255] ^ a[h & 255] ^ r[p++]
                 , f = i[f >>> 24] ^ n[l >>> 16 & 255] ^ o[h >>> 8 & 255] ^ a[u & 255] ^ r[p++]
                 , l = y
                 , h = g
                 , u = v;
        y = (s[l >>> 24] << 24 | s[h >>> 16 & 255] << 16 | s[u >>> 8 & 255] << 8 | s[f & 255]) ^ r[p++];
        g = (s[h >>> 24] << 24 | s[u >>> 16 & 255] << 16 | s[f >>> 8 & 255] << 8 | s[l & 255]) ^ r[p++];
        v = (s[u >>> 24] << 24 | s[f >>> 16 & 255] << 16 | s[l >>> 8 & 255] << 8 | s[h & 255]) ^ r[p++];
        f = (s[f >>> 24] << 24 | s[l >>> 16 & 255] << 16 | s[h >>> 8 & 255] << 8 | s[u & 255]) ^ r[p++];
        e[t] = y;
        e[t + 1] = g;
        e[t + 2] = v;
        e[t + 3] = f
    };

    this._doFinalize = function () {
        this.pad(this._data, this.blockSize);
        var t = this._process(!0);
        return t
    };

    this.finalize = function (e) {
        this._doReset();
        e && this._append(e);
        return this._doFinalize()
    };

    return this.finalize(_e);
}


stringify = function (e) {
    this._map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var t = e.words
        , r = e.sigBytes
        , i = this._map;
    e.clamp = function () {
        var t = this.words
            , r = this.sigBytes;
        t[r >>> 2] &= 4294967295 << 32 - 8 * (r % 4);
        t.length = Math.ceil(r / 4)
    };
    e.clamp();
    e = [];
    for (var n = 0; n < r; n += 3)
        for (var o = (t[n >>> 2] >>> 24 - 8 * (n % 4) & 255) << 16 | (t[n + 1 >>> 2] >>> 24 - 8 * ((n + 1) % 4) & 255) << 8 | t[n + 2 >>> 2] >>> 24 - 8 * ((n + 2) % 4) & 255, a = 0; 4 > a && n + .75 * a < r; a++)
            e.push(i.charAt(o >>> 6 * (3 - a) & 63));
    if (t = i.charAt(64))
        for (; e.length % 4;)
            e.push(t);
    return e.join("")
};


function eq_u(e, t) {
    // e: "{"xy":[],"fingerprint":3827967540}"
    // t: "52D2841A3485DFFBCF2EA6A0515077CD"
    var r = parse_l_parse(t);// r: init {words: Array(8), sigBytes: 32}
    var data = doReset_finalize(r, e);
    return stringify(data);
}

function getParams(fingerprint) {
    var desc = eq_u(JSON.stringify({"xy": [], "fingerprint": fingerprint}), "52D2841A3485DFFBCF2EA6A0515077CD");
    console.log('desc', desc);
    desc = del_html_tags(desc, "\\+", "%2B");
    console.log('desc', desc);
    return desc
}

function del_html_tags(e, t, r) {
    var i = new RegExp(t, "g");
    words = e.replace(i, r);
    return words
}


getParams(3827967540);
// 3827967540：coBPtm4BZy5Ly7E1arnljwxtqjbEC6bDB76RJZCdIPBo2tz7GPiCNecjXPa7Jydt
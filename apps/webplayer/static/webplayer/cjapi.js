/**
 The MIT License

 Copyright (c) 2010 Daniel Park (http://metaweb.com, http://postmessage.freebaseapps.com)

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
 **/

var NO_JQUERY = {};
(function (e, t, n) {
    if (!("console" in e)) {
        var r = e.console = {};
        r.log = r.warn = r.error = r.debug = function () {}
    }
    t === NO_JQUERY && (t = {
        fn: {},
        extend: function () {
            var e = arguments[0];
            for (var t = 1, n = arguments.length; t < n; t++) {
                var r = arguments[t];
                for (var i in r) e[i] = r[i]
            }
            return e
        }
    }), t.fn.pm = function () {
        return console.log("usage: \nto send:    $.pm(options)\nto receive: $.pm.bind(type, fn, [origin])"), this
    }, t.pm = e.pm = function (e) {
        i.send(e)
    }, t.pm.bind = e.pm.bind = function (e, t, n, r, s) {
        i.bind(e, t, n, r, s === !0)
    }, t.pm.unbind = e.pm.unbind = function (e, t) {
        i.unbind(e, t)
    }, t.pm.origin = e.pm.origin = null, t.pm.poll = e.pm.poll = 200;
    var i = {
        send: function (e) {
            var n = t.extend({}, i.defaults, e),
                r = n.target;
            if (!n.target) {
                console.warn("postmessage target window required");
                return
            }
            if (!n.type) {
                console.warn("postmessage type required");
                return
            }
            var s = {
                data: n.data,
                type: n.type
            };
            n.success && (s.callback = i._callback(n.success)), n.error && (s.errback = i._callback(n.error)), "postMessage" in r && !n.hash ? (i._bind(), r.postMessage(JSON.stringify(s), n.origin || "*")) : (i.hash._bind(), i.hash.send(n, s))
        },
        bind: function (e, t, n, r, s) {
            i._replyBind(e, t, n, r, s)
        },
        _replyBind: function (n, r, s, o, u) {
            "postMessage" in e && !o ? i._bind() : i.hash._bind();
            var a = i.data("listeners.postmessage");
            a || (a = {}, i.data("listeners.postmessage", a));
            var f = a[n];
            f || (f = [], a[n] = f), f.push({
                fn: r,
                callback: u,
                origin: s || t.pm.origin
            })
        },
        unbind: function (e, t) {
            var n = i.data("listeners.postmessage");
            if (n)
                if (e)
                    if (t) {
                        var r = n[e];
                        if (r) {
                            var s = [];
                            for (var o = 0, u = r.length; o < u; o++) {
                                var a = r[o];
                                a.fn !== t && s.push(a)
                            }
                            n[e] = s
                        }
                    } else delete n[e];
                    else
                        for (var o in n) delete n[o]
        },
        data: function (e, t) {
            return t === n ? i._data[e] : (i._data[e] = t, t)
        },
        _data: {},
        _CHARS: "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".split(""),
        _random: function () {
            var e = [];
            for (var t = 0; t < 32; t++) e[t] = i._CHARS[0 | Math.random() * 32];
            return e.join("")
        },
        _callback: function (e) {
            var t = i.data("callbacks.postmessage");
            t || (t = {}, i.data("callbacks.postmessage", t));
            var n = i._random();
            return t[n] = e, n
        },
        _bind: function () {
            i.data("listening.postmessage") || (e.addEventListener ? e.addEventListener("message", i._dispatch, !1) : e.attachEvent && e.attachEvent("onmessage", i._dispatch), i.data("listening.postmessage", 1))
        },
        _dispatch: function (e) {
            try {
                var t = JSON.parse(e.data)
            } catch (n) {
                console.warn("postmessage data invalid json: ", n);
                return
            }
            if (!t.type) {
                console.warn("postmessage message type required");
                return
            }
            var r = i.data("callbacks.postmessage") || {}, s = r[t.type];
            if (s) s(t.data);
            else {
                var o = i.data("listeners.postmessage") || {}, u = o[t.type] || [];
                for (var a = 0, f = u.length; a < f; a++) {
                    var l = u[a];
                    if (l.origin && l.origin !== "*" && e.origin !== l.origin) {
                        console.warn("postmessage message origin mismatch", e.origin, l.origin);
                        if (t.errback) {
                            var c = {
                                message: "postmessage origin mismatch",
                                origin: [e.origin, l.origin]
                            };
                            i.send({
                                target: e.source,
                                data: c,
                                type: t.errback
                            })
                        }
                        continue
                    }

                    function h(n) {
                        t.callback && i.send({
                            target: e.source,
                            data: n,
                            type: t.callback
                        })
                    }
                    try {
                        l.callback ? l.fn(t.data, h, e) : h(l.fn(t.data, e))
                    } catch (n) {
                        if (!t.errback) throw n;
                        i.send({
                            target: e.source,
                            data: n,
                            type: t.errback
                        })
                    }
                }
            }
        }
    };
    i.hash = {
        send: function (t, n) {
            var r = t.target,
                s = t.url;
            if (!s) {
                console.warn("postmessage target window url is required");
                return
            }
            s = i.hash._url(s);
            var o, u = i.hash._url(e.location.href);
            if (e == r.parent) o = "parent";
            else try {
                for (var a = 0, f = parent.frames.length; a < f; a++) {
                    var l = parent.frames[a];
                    if (l == e) {
                        o = a;
                        break
                    }
                }
            } catch (c) {
                o = e.name
            }
            if (o == null) {
                console.warn("postmessage windows must be direct parent/child windows and the child must be available through the parent window.frames list");
                return
            }
            var h = {
                "x-requested-with": "postmessage",
                source: {
                    name: o,
                    url: u
                },
                postmessage: n
            }, p = "#x-postmessage-id=" + i._random();
            r.location = s + p + encodeURIComponent(JSON.stringify(h))
        },
        _regex: /^\#x\-postmessage\-id\=(\w{32})/,
        _regex_len: "#x-postmessage-id=".length + 32,
        _bind: function () {
            i.data("polling.postmessage") || (setInterval(function () {
                var t = "" + e.location.hash,
                    n = i.hash._regex.exec(t);
                if (n) {
                    var r = n[1];
                    i.hash._last !== r && (i.hash._last = r, i.hash._dispatch(t.substring(i.hash._regex_len)))
                }
            }, t.pm.poll || 200), i.data("polling.postmessage", 1))
        },
        _dispatch: function (t) {
            if (!t) return;
            try {
                t = JSON.parse(decodeURIComponent(t));
                if (!(t["x-requested-with"] === "postmessage" && t.source && t.source.name != null && t.source.url && t.postmessage)) return
            } catch (n) {
                return
            }
            var r = t.postmessage,
                s = i.data("callbacks.postmessage") || {}, o = s[r.type];
            if (o) o(r.data);
            else {
                var u;
                t.source.name === "parent" ? u = e.parent : u = e.frames[t.source.name];
                var a = i.data("listeners.postmessage") || {}, f = a[r.type] || [];
                for (var l = 0, c = f.length; l < c; l++) {
                    var h = f[l];
                    if (h.origin) {
                        var p = /https?\:\/\/[^\/]*/.exec(t.source.url)[0];
                        if (h.origin !== "*" && p !== h.origin) {
                            console.warn("postmessage message origin mismatch", p, h.origin);
                            if (r.errback) {
                                var d = {
                                    message: "postmessage origin mismatch",
                                    origin: [p, h.origin]
                                };
                                i.send({
                                    target: u,
                                    data: d,
                                    type: r.errback,
                                    hash: !0,
                                    url: t.source.url
                                })
                            }
                            continue
                        }
                    }

                    function v(e) {
                        r.callback && i.send({
                            target: u,
                            data: e,
                            type: r.callback,
                            hash: !0,
                            url: t.source.url
                        })
                    }
                    try {
                        h.callback ? h.fn(r.data, v) : v(h.fn(r.data))
                    } catch (n) {
                        if (!r.errback) throw n;
                        i.send({
                            target: u,
                            data: n,
                            type: r.errback,
                            hash: !0,
                            url: t.source.url
                        })
                    }
                }
            }
        },
        _url: function (e) {
            return ("" + e).replace(/#.*$/, "")
        }
    }, t.extend(i, {
        defaults: {
            target: null,
            url: null,
            type: null,
            data: null,
            success: null,
            error: null,
            origin: "*",
            hash: !1
        }
    })
})(this, typeof jQuery == "undefined" ? NO_JQUERY : jQuery), "JSON" in window && window.JSON || (JSON = {}),
function () {
    function f(e) {
        return e < 10 ? "0" + e : e
    }

    function quote(e) {
        return escapable.lastIndex = 0, escapable.test(e) ? '"' + e.replace(escapable, function (e) {
            var t = meta[e];
            return typeof t == "string" ? t : "\\u" + ("0000" + e.charCodeAt(0).toString(16)).slice(-4)
        }) + '"' : '"' + e + '"'
    }

    function str(e, t) {
        var n, r, i, s, o = gap,
            u, a = t[e];
        a && typeof a == "object" && typeof a.toJSON == "function" && (a = a.toJSON(e)), typeof rep == "function" && (a = rep.call(t, e, a));
        switch (typeof a) {
        case "string":
            return quote(a);
        case "number":
            return isFinite(a) ? String(a) : "null";
        case "boolean":
        case "null":
            return String(a);
        case "object":
            if (!a) return "null";
            gap += indent, u = [];
            if (Object.prototype.toString.apply(a) === "[object Array]") {
                s = a.length;
                for (n = 0; n < s; n += 1) u[n] = str(n, a) || "null";
                return i = u.length === 0 ? "[]" : gap ? "[\n" + gap + u.join(",\n" + gap) + "\n" + o + "]" : "[" + u.join(",") + "]", gap = o, i
            }
            if (rep && typeof rep == "object") {
                s = rep.length;
                for (n = 0; n < s; n += 1) r = rep[n], typeof r == "string" && (i = str(r, a), i && u.push(quote(r) + (gap ? ": " : ":") + i))
            } else
                for (r in a) Object.hasOwnProperty.call(a, r) && (i = str(r, a), i && u.push(quote(r) + (gap ? ": " : ":") + i));
            return i = u.length === 0 ? "{}" : gap ? "{\n" + gap + u.join(",\n" + gap) + "\n" + o + "}" : "{" + u.join(",") + "}", gap = o, i
        }
    }
    typeof Date.prototype.toJSON != "function" && (Date.prototype.toJSON = function (e) {
        return this.getUTCFullYear() + "-" + f(this.getUTCMonth() + 1) + "-" + f(this.getUTCDate()) + "T" + f(this.getUTCHours()) + ":" + f(this.getUTCMinutes()) + ":" + f(this.getUTCSeconds()) + "Z"
    }, String.prototype.toJSON = Number.prototype.toJSON = Boolean.prototype.toJSON = function (e) {
        return this.valueOf()
    });
    var cx = /[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,
        escapable = /[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,
        gap, indent, meta = {
            "\b": "\\b",
            "	": "\\t",
            "\n": "\\n",
            "\f": "\\f",
            "\r": "\\r",
            '"': '\\"',
            "\\": "\\\\"
        }, rep;
    typeof JSON.stringify != "function" && (JSON.stringify = function (e, t, n) {
        var r;
        gap = "", indent = "";
        if (typeof n == "number")
            for (r = 0; r < n; r += 1) indent += " ";
        else typeof n == "string" && (indent = n);
        rep = t;
        if (!t || typeof t == "function" || typeof t == "object" && typeof t.length == "number") return str("", {
            "": e
        });
        throw new Error("JSON.stringify")
    }), typeof JSON.parse != "function" && (JSON.parse = function (text, reviver) {
        function walk(e, t) {
            var n, r, i = e[t];
            if (i && typeof i == "object")
                for (n in i) Object.hasOwnProperty.call(i, n) && (r = walk(i, n), r !== undefined ? i[n] = r : delete i[n]);
            return reviver.call(e, t, i)
        }
        var j;
        cx.lastIndex = 0, cx.test(text) && (text = text.replace(cx, function (e) {
            return "\\u" + ("0000" + e.charCodeAt(0).toString(16)).slice(-4)
        }));
        if (/^[\],:{}\s]*$/.test(text.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, "@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]").replace(/(?:^|:|,)(?:\s*\[)+/g, ""))) return j = eval("(" + text + ")"), typeof reviver == "function" ? walk({
            "": j
        }, "") : j;
        throw new SyntaxError("JSON.parse")
    })
}(),
function () {
    window.CJApiStats = function () {
        function t() {}
        var e;
        return e = void 0, t.getInstance = function () {
            return e != null ? e : e = new t
        }, t.prototype.submit = function (e, t, n) {
            return $.pm({
                target: window.parent,
                type: "submitStat",
                data: {
                    statName: e,
                    value: t,
                    salt: n
                }
            })
        }, t
    }(), window.CJApiUsers = function () {
        function t() {}
        var e;
        return e = void 0, t.getInstance = function () {
            return e != null ? e : e = new t
        }, t.prototype.getUsername = function (e) {
            return $.pm({
                target: window.parent,
                type: "getUsername",
                data: {
                    salt: e
                }
            })
        }, t
    }(), window.CJApiServices = function () {
        function t() {}
        var e;
        return e = void 0, t.getInstance = function () {
            return e != null ? e : e = new t
        }, t.prototype.showRegistrationBox = function (e) {
            return $.pm({
                target: window.parent,
                type: "showRegistrationBox"
            })
        }, t.prototype.showSignInBox = function (e) {
            return $.pm({
                target: window.parent,
                type: "showSignInBox"
            })
        }, t.prototype.isSignedIn = function (e) {
            return $.pm({
                target: window.parent,
                type: "isSignedIn",
                data: {
                    salt: e
                }
            })
        }, t
    }(), window.CJApiUtils = function () {
        function e() {}
        return e.isFlashGame = function () {
            return false;
            return document.getElementById("game_src").data !== void 0
        }, e.game = function () {
            return document.getElementById("game_src")
        }, e
    }(), window.CJApi = function () {
        function e() {}
        return e.users = CJApiUsers.getInstance(), e.stats = CJApiStats.getInstance(), e.services = CJApiServices.getInstance(), e
    }(), $.pm.bind("onLoggedOut", function () {
        return CJApiUtils.isFlashGame() ? CJApiUtils.game().loggedOut() : $(CJApi.services).trigger("loggedOut")
    }), $.pm.bind("onLoggedIn", function () {
        return CJApiUtils.isFlashGame() ? CJApiUtils.game().logged() : $(CJApi.services).trigger("logged")
    }), $.pm.bind("onGetUsername", function (e) {
        return CJApiUtils.isFlashGame() ? CJApiUtils.game().onGetUsername(e.username) : $(CJApi.users).trigger("onGetUsername", e)
    }), $.pm.bind("onGetUsernameError", function (e) {
        return CJApiUtils.isFlashGame() ? CJApiUtils.game().onGetUsernameError(e.error) : $(CJApi.users).trigger("onGetUsernameError", e.error)
    }), $.pm.bind("onIsSignedIn", function (e) {
        return CJApiUtils.isFlashGame() ? CJApiUtils.game().isSignedIn(e.isSignedIn) : $(CJApi.services).trigger("onIsSignedIn", e)
    }), $.pm.bind("isSignedInError", function (e) {
        return CJApiUtils.isFlashGame() ? CJApiUtils.game().isSignedInError(e.error) : $(CJApi.services).trigger("isSignedInError", e.error)
    }), $.pm.bind("onSubmitStat", function (e) {
        return CJApiUtils.isFlashGame() ? CJApiUtils.game().onSubmitStat(e.stat) : $(CJApi.stats).trigger("onSubmit", e.stat)
    }), $.pm.bind("onSubmitError", function (e) {
        return CJApiUtils.isFlashGame() ? CJApiUtils.game().onSubmitStatError(e.error) : $(CJApi.stats).trigger("onSubmitError", e.error)
    })
}.call(this),
function () {}.call(this);
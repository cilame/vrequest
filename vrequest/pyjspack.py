
comment = r'''
// 功能：
// 将需要的文件压缩打包成 es5 语法的，可以打包库文件，这样使用起来就方便很多了。

// 安装：
// 选择或创建一个空文件夹，然后在文件夹路径打开命令行使用下面的命令安装环境和打包js脚本。
// npm install -g cnpm --registry=https://registry.npm.taobao.org
// npm init -y
// cnpm install webpack-cli webpack -S
// cnpm install babel-cli babel-preset-env -S
// 一行安装
// npm install -g cnpm --registry=https://registry.npm.taobao.org && npm init -y && cnpm install webpack-cli webpack -S && cnpm install babel-cli babel-preset-env -S

// 打包：
// npx webpack --entry="./index.js"
// npx babel dist/main.js -d es5 --presets=babel-preset-env
// 一行打包
// npx webpack --entry="./index.js" && npx babel dist/main.js -d es5 --presets=babel-preset-env

// 在 es5/dist 文件夹下找 main.js 就是目标文件了。
// 可以新建一个文件夹命名为 index.js 输入下面两行内容。用上面的方式打包，后续可直接作单脚本使用。
// const CryptoJS = require('crypto-js')
// window.CryptoJS = CryptoJS








// 额外的常用的一些工具代码
// sublime 工具配置
{
    "shell": true,
    "encoding": "utf8",
    "cmd": ["taskkill", "/F", "/IM", "node.exe", "&", "node", "$file"],
    "variants":[
        { "name": "node inspect",
          "shell_cmd":"taskkill /F /IM \"node.exe\" & node --inspect-brk \"$file\"",
        },
    ]
}

// 快捷挂钩 js 代码
_window = typeof global=='undefined'?window:global
_window._vPxy = _window._vPxy?_window._vPxy:function(G, M, F, prefix){
    var util = typeof global=='undefined'?undefined:require('util');
    _window._vLine = _window._vLine?_vLine:function _vLine(o, lines){
        if (util){
            var lines = lines || 5
            var v = util.inspect(o)
            var c = `        ... <DONT SHOW MORE OVER ${lines} LINES IN ONE OBJECT>`
            function make_space_gap(num){
                return _spacearr[num]
            }
            function weak_output(v, num){
                return ('\n' + v + '\n').split('\n').slice(0, num).concat(c).map(function(e, i){return make_space_gap(_global_gap)+e}).join('\n')
            }
            function count_lines(v){
                return (v.match(/\n/g)||'').length
            }
            if (count_lines(v) > lines){
                return weak_output(v, lines)
            }else{
                return v
            }
        }else{
            if (typeof o == 'symbol'){
                return o.toString()
            }
            return o
        }
    }
    _window._global_gap = _window._global_gap?_window._global_gap:80
    _window._print      = _window._print?_window._print:console.log
    _window.start       = _window.start?_window.start:1
    _window.ostart      = _window.ostart?_window.ostart:0
    _window.ret_detail  = _window.ret_detail?_window.ret_detail:1
    _window._isArray    = _window._isArray?_window._isArray:Array.isArray
    _window._stringify  = _window._stringify?_window._stringify:JSON.stringify
    _window._spacearr   = _window._spacearr?_window._spacearr:Array(100).fill(0).map(function(e,i){return Array(i).fill(' ').join('')})
    _window._ignore_log = _window._ignore_log?_window._ignore_log:[]
    _window._vLog       = _window._vLog?_window._vLog:function _vLog(F, O, P){ 
        if (start){
            for (var i = 0; i < _ignore_log.length; i++) {
                var ig = _ignore_log[i]
                if (ig[0] == F && ig[1] == O && (ig[2]===undefined || (ig[2]===P && P !== undefined))){
                    return
                }
            }
            _print.apply(_print, [].slice.call(arguments, 3))
        }
    }
    _window.myparselog  = _window.myparselog?_window.myparselog:function myparselog(V){
        ostart = start
        start = 0
        var r = typeof V=='string'?
            _stringify(V.length > 200?V.slice(0,200) + '... <DONSHOW MORETHAN 200 LENGTH>':V)
        :
        typeof V=='number'?V:
        typeof V=='function'?V:
        typeof V=='undefined'?undefined:
        typeof V=='boolean'?V:
        V===null?null:
        ret_detail?_vLine(V):
        _isArray(V)?_stringify(V):
        `<DONTSHOW TYPE:${typeof V}>`
        start = ostart
        return r
    }
    _window._v_hidden_Inject = _window._v_hidden_Inject?_window._v_hidden_Inject:function(){return _vDoDefault}
    _window._vDoDefault      = _window._vDoDefault?_window._vDoDefault:Symbol('undefined')
    _window._vInject         = _window._vInject?_window._vInject:function(){return _vDoDefault}
    var prefix = prefix?_spacearr[prefix]:''
    var _vLog = (typeof global=='undefined'?window:global)._vLog || _print
    function LS(T, M, F, L){ 
        var pr = prefix + `[Proxy] ${M}[${T.constructor.name}].(Prxoy)${F} ==>> ${L?L:''}`
        var taillen = _global_gap - pr.length
        pr += _spacearr[(taillen > 0)?taillen:0]
        return pr
    }
    return new Proxy(G, {
        get: function(T, P, R){
            var Rt;
            var In = _v_hidden_Inject(F, 'get', arguments); 
            try{
                if (In !== _vDoDefault){
                    Rt = In
                }else{
                    Rt = Reflect.get(T, P, R)
                }
            }catch(e){
                if (P !== Symbol.unscopables){ _vLog(F, 'get', P, LS(G, M, 'get', P), '[GET ERROR]'); } // get 获取出错时，需要输出究竟是因为哪个参数报错的
                throw e;
            }
            if (P !== Symbol.unscopables){ _vLog(F, 'get', P, LS(G, M, 'get', myparselog(P)), myparselog(Rt)); }
            return Rt;
        },
        has: function(T, P){
            var Rt;
            var In = _v_hidden_Inject(F, 'has', arguments); 
            if (In !== _vDoDefault){
                Rt = In
            }else{
                Rt = Reflect.has(T, P) 
            }
            if (T !== _interceptor){ _vLog(F, 'has', P, LS(G, M, 'has', P), Rt); }
            return Rt;
        },
        getPrototypeOf: function(T){
            var Rt;
            var In = _v_hidden_Inject(F, 'getPrototypeOf', undefined, arguments); 
            if (In !== _vDoDefault){
                Rt = In
            }else{
                Rt = Reflect.getPrototypeOf(T)
            }
            _vLog(F, 'getPrototypeOf', undefined, LS(G, M, 'getPrototypeOf'), myparselog(T) );
            return Rt;
        },
        set: function(T, P, V, R){ 
            var Rt;
            var In = _v_hidden_Inject(F, 'set', arguments); 
            if (In !== _vDoDefault){
                Rt = In
            }else{
                Rt = Reflect.set(T, P, V, R)
            }
            if (P != '__cilame__'){_vLog(F, 'set', P, LS(G, M, 'set', myparselog(P)), myparselog(V) )}
            return Rt;
        },
        apply: function(T, A, L){
            var Rt;
            var In = _v_hidden_Inject(F, 'apply', arguments);
            if (In !== _vDoDefault){
                Rt = In
            } else{
                Rt = Reflect.apply(T, A, L) 
            }
            _vLog(F, 'apply', undefined, LS(G, M, 'apply', myparselog(L)), myparselog(Rt) );
            return Rt;
        },
        deleteProperty: function(T, P){
            var Rt;
            var In = _v_hidden_Inject(F, 'deleteProperty', arguments); 
            if (In !== _vDoDefault){
                Rt = In
            }else{
                Rt = Reflect.deleteProperty(T, P) 
            }
            _vLog(F, 'deleteProperty', P, LS(G, M, 'deleteProperty', P), Rt);
            return Rt;
        },
        setPrototypeOf: function(T, P){
            var Rt;
            var In = _v_hidden_Inject(F, 'setPrototypeOf', arguments); 
            if (In !== _vDoDefault){
                Rt = In
            }else{
                Rt = Reflect.setPrototypeOf(T, P) 
            }
            _vLog(F, 'setPrototypeOf', P, LS(G, M, 'setPrototypeOf'), T, P, Rt);
            return Rt;
        },
        ownKeys: function(T){ 
            var Rt;
            var In = _v_hidden_Inject(F, 'ownKeys', arguments); 
            if (In !== _vDoDefault){
                Rt = In
            }else{
                Rt = Reflect.ownKeys(T)
            }
            _vLog(F, 'ownKeys', undefined, LS(G, M, 'ownKeys'), myparselog(T), myparselog(Rt) );
            return Rt;
        },
        construct: function(T, L, N){
            var Rt;
            var In = _v_hidden_Inject(F, 'construct', arguments); 
            if (In !== _vDoDefault){
                Rt = In
            } else{
                Rt = Reflect.construct(T, L, N)
            }
            _vLog(F, 'construct', undefined, LS(G, M, 'construct', myparselog(L)), myparselog(Rt) );
            return Rt;
        },
        isExtensible: function(T){
            var Rt;
            var In = _v_hidden_Inject(F, 'isExtensible', arguments); 
            if (In !== _vDoDefault){
                Rt = In
            }else{
                Rt = Reflect.isExtensible(T) 
            }
            _vLog(F, 'isExtensible', undefined, LS(G, M, 'isExtensible'), Rt);
            return Rt;
        },
        defineProperty: function(T, P, A){
            var Rt;
            var In = _v_hidden_Inject(F, 'defineProperty', arguments); 
            if (In !== _vDoDefault){
                Rt = In
            }else{
                Rt = Reflect.defineProperty(T, P, A) 
            }
            _vLog(F, 'defineProperty', P, LS(G, M, 'defineProperty', P), T, A, Rt);
            return Rt;
        },
        preventExtensions: function(T){
            var Rt;
            var In = _v_hidden_Inject(F, 'preventExtensions', arguments); 
            if (In !== _vDoDefault){
                Rt = In
            }else{
                Rt = Reflect.preventExtensions(T) 
            }
            _vLog(F, 'preventExtensions', undefined, LS(G, M, 'preventExtensions'), Rt);
            return Rt;
        },
        getOwnPropertyDescriptor: function(T, P){ 
            var Rt;
            var In = _v_hidden_Inject(F, 'getOwnPropertyDescriptor',  arguments); 
            if (In !== _vDoDefault){
                Rt = In
            }else{
                Rt = Reflect.getOwnPropertyDescriptor(T, P) 
            }
            _vLog(F, 'getOwnPropertyDescriptor', P, LS(G, M, 'getOwnPropertyDescriptor', myparselog(P)), myparselog(T), Rt ); 
            return Rt;
        },
    })
}
_window._v_hidden_Inject = _window._v_hidden_Inject?_window._v_hidden_Inject:function(F, O, args){
    var r = _window._vInject(F, O, args)
    return (r !== _vDoDefault)?r:_vDoDefault
}
_vInject = function(F, O, args){
    if (F == 'XXX'){
        if (O == 'get'){
            // 被 _vPxy 代理的所有对象都会走这里，_vPxy 函数传入的第三个参数就是这里的 F ，操作就是 O ，操作所用的参数就是 args
            // 你可以在这个函数内尽情的修改获取某些对象的操作
            _print('==========')
            // return undefined
        }
    }
    return _vDoDefault // 返回默认操作，不返回这个值，所有的操作都将会变成 undefined，with 内的所有操作都将被拦截。
}

x = _vPxy({}, "XX", "XXX", 4)
x.asdf




'''
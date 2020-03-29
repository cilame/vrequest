print = console.log

var esprima = require('esprima');
var estraverse = require('estraverse')
var escodegen = require('escodegen')

function muti_process_defusion(code){
    var tree = esprima.parseScript(code)
    combine_static_array(tree);
    combine_object_array(tree);
    // combine_identy_function(tree); // 该参数在某些情况下使用起来不是很方便
    combine_binary_function(tree);
    combine_binary(tree);
    return escodegen.generate(tree);
}

// 合并对象的静态列表(这里后续需要考虑考虑重名的处理)
function combine_object_array(tree) {
    var STATIC_OBJECT = {};
    estraverse.replace(tree, {
        leave(node, parent) {
            // 初始化
            if (node.type === 'VariableDeclarator' &&
                node.init != null &&
                node.init.type === 'ObjectExpression'){
                STATIC_OBJECT[node.id.name] = {}
                for(var key in node.init.properties){
                    STATIC_OBJECT[node.id.name][node.init.properties[key].key.value] = node.init.properties[key].value
                }
            }
            // 赋值
            if (node.type === 'AssignmentExpression' &&
                node.left.type === 'MemberExpression' &&
                node.left.computed === true &&
                node.left.object.type === 'Identifier' &&
                node.left.object.name in STATIC_OBJECT &&
                node.right.type === 'Literal' &&
                typeof node.left.property.value !== 'number'){
                STATIC_OBJECT[node.left.object.name][node.left.property.value] = node.right
            }
            // 替换
            if (node.type === 'MemberExpression' &&
                node.object.type === 'Identifier' &&
                node.property.type === 'Literal' &&
                node.object.name in STATIC_OBJECT){
                return STATIC_OBJECT[node.object.name][node.property.value];
            }
        }
    });
}

// 合并参数的静态列表(这里后续需要考虑考虑重名的处理)
function combine_static_array(tree) {
    var STATIC_ARRAY = {};
    estraverse.replace(tree, {
        leave(node, parent) {
            // 初始化
            if (node.type === 'VariableDeclarator' &&
                node.init != null &&
                node.init.type === 'ArrayExpression' &&
                node.id.type === 'Identifier'){
                STATIC_ARRAY[node.id.name] = node.init.elements
            }
            // 赋值
            if (node.type === 'AssignmentExpression' &&
                node.left.type === 'MemberExpression' &&
                node.left.computed === true &&
                node.left.object.type === 'Identifier' &&
                node.left.object.name in STATIC_ARRAY &&
                node.right.type === 'Literal' &&
                typeof node.left.property.value === 'number'){
                STATIC_ARRAY[node.left.object.name][node.left.property.value] = node.right
            }
            // 替换
            if (node.type === 'MemberExpression' &&
                node.object.type === 'Identifier' &&
                node.property.type === 'Literal' &&
                node.object.name in STATIC_ARRAY){
                return STATIC_ARRAY[node.object.name][node.property.value];
            }
        }
    });
}

// 函数执行的寻找，从该节点的父节点中寻找函数，并修改当前函数执行的节点
function combine_identy_function(tree) {
    var cache_name;
    var cache_func;
    var CACHE_FUNCS = {};
    estraverse.replace(tree, {
        enter(node, parent){
            if (cache_name = _cache_func(node)){
                CACHE_FUNCS[cache_name[0]] = cache_name[1];
            }
            if (cache_func = _cache_func_rep(node, CACHE_FUNCS)){
                return cache_func;
            }


            if (node.type === 'ExpressionStatement' &&
                node.expression.type === 'CallExpression' && 
                node.expression.callee.type === 'Identifier' &&
                parent.body
                ) {
                for(var key in parent.body){
                    var _node;
                    if (_node = _catch_func(parent.body[key], node.expression.callee.name)){
                        node.expression.callee = _node
                        return node
                    }
                }
            }
            if (node.type === 'VariableDeclaration' && parent.body){
                for(var jkey in node.declarations){
                    if (node.declarations[jkey].type === 'VariableDeclarator' && 
                        node.declarations[jkey].init != null &&
                        node.declarations[jkey].init.type === 'CallExpression' &&
                        node.declarations[jkey].init.callee.type === 'Identifier' &&
                        parent.body){
                        var _node = _catch_func_parent(parent, node.declarations[jkey].init.callee.name);
                        if (_node){
                            node.declarations[jkey].init.callee = _node
                        }
                    }
                }
            }
        }
    });
}
function _catch_func(node, name) {
    if(node.type === 'VariableDeclaration'){
        for(var jkey in node.declarations){
            if (node.declarations[jkey].type === 'VariableDeclarator' && 
                node.declarations[jkey].init != null &&
                node.declarations[jkey].init.type === 'FunctionExpression' &&
                node.declarations[jkey].id.type === 'Identifier' && 
                node.declarations[jkey].id.name === name){
                return node.declarations[jkey].init
            }
        }
    }
    if (node.type === 'FunctionDeclaration'){
        if (node.id.type === 'Identifier' &&
            node.id.name === name){
            return node
        }
    }
}
function _catch_func_parent(parent, name) {
    for(var key in parent.body){
        var _node;
        if (_node = _catch_func(parent.body[key], name)){
            return _node
        }
    }
}
function _cache_func(node, name) {
    if(node.type === 'VariableDeclaration'){
        for(var jkey in node.declarations){
            if (node.declarations[jkey].type === 'VariableDeclarator' && 
                node.declarations[jkey].init != null &&
                node.declarations[jkey].init.type === 'FunctionExpression' &&
                node.declarations[jkey].id.type === 'Identifier'){
                return [node.declarations[jkey].id.name, node.declarations[jkey].init]
            }
        }
    }
    if (node.type === 'FunctionDeclaration'){
        if (node.id.type === 'Identifier'){
            return [node.id.name, node]
        }
    }
}
function _cache_func_rep(node, cachefunc) {
    if (node.type === 'CallExpression' && 
        node.callee.type === 'Identifier' &&
        node.callee.name in cachefunc){
        node.callee = cachefunc[node.callee.name];
        return node;
    }
}

// 合并简单的二元运算
function combine_binary(tree) {
    estraverse.replace(tree, {
        enter(node, parent){
            if (node.type === 'BinaryExpression' && node.left.type === 'Literal' && node.right.type === 'Literal') {
                return {
                    type: 'Literal',
                    value: eval(JSON.stringify(node.left.value) + node.operator + JSON.stringify(node.right.value))
                };
            }
        }
    });
};

// 合并简单二元运算的函数
function combine_binary_function(tree) {
    estraverse.replace(tree, {
        enter(node, parent){
            if (node.type === 'CallExpression' && 
                node.arguments.length === 2 && 
                (node.callee.type === 'FunctionExpression' || node.callee.type === 'FunctionDeclaration') &&
                node.callee.params.length === 2 &&
                node.callee.body.type === 'BlockStatement' && 
                node.callee.body.body.length === 1 &&
                node.callee.body.body[0].type === 'ReturnStatement' && 
                node.callee.body.body[0].argument.type === 'BinaryExpression' &&
                node.callee.params[0].type === 'Identifier' &&
                node.callee.params[1].type === 'Identifier' &&
                node.callee.body.body[0].argument.left.name  === node.callee.params[0].name &&
                node.callee.body.body[0].argument.right.name === node.callee.params[1].name) {
                rnode = {
                    type: 'BinaryExpression',
                    operator: node.callee.body.body[0].argument.operator,
                    left: node.arguments[0],
                    right: node.arguments[1],
                };
                if (rnode.type === 'BinaryExpression' && rnode.left.type === 'Literal' && rnode.right.type === 'Literal') {
                    return {
                        type: 'Literal',
                        value: eval(JSON.stringify(rnode.left.value) + rnode.operator + JSON.stringify(rnode.right.value))
                    };
                }else{
                    return rnode
                }
            }
        }
    });
}

// 遍历展示
function show(tree) {
    estraverse.traverse(tree, {
        enter(node, parent) {
            print(parent)
            print('---------------')
            print(node)
            print('===============')
        }
    });
}
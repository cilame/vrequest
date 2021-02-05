function FormatMember(path) {
    // _0x19882c['removeCookie']['toString']()
    //  |
    //  |
    //  |
    //  v
    // _0x19882c.removeCookie.toString()
    var curNode = path.node;
    if(!t.isStringLiteral(curNode.property))
        return;
    if(curNode.computed === undefined || !curNode.computed === true)
        return;
    if (!/[a-zA-Z_$][0-9a-zA-Z_$]*/.test(curNode.property.value))
        return;
    curNode.property = t.identifier(curNode.property.value);
    curNode.computed = false;
}

function TransCondition(path) {
    // a = m?11:22; 
    //  |
    //  |
    //  |
    //  v
    // m ? a = 11 : a = 22;
    let {test, consequent, alternate} = path.node;
    const ParentPath = path.parentPath;
    if (ParentPath.isAssignmentExpression()) {
        let {operator, left} = ParentPath.node;
        if (operator === "=") {
            consequent = t.AssignmentExpression("=", left, consequent)
            alternate = t.AssignmentExpression("=", left, alternate)
            ParentPath.replaceWith(t.conditionalExpression(test, consequent, alternate))
        }
    }
}
function ConditionToIf(path) {
    // m ? a = 11 : a = 22;
    //  |
    //  |
    //  |
    //  v
    // if (m) {
    //   a = 11;
    // } else {
    //   a = 22;
    // }
    let {expression} = path.node;
    if(!t.isConditionalExpression(expression)) return;
    let {test, consequent, alternate} = expression;
    path.replaceWith(t.ifStatement(
        test,
        t.blockStatement([t.expressionStatement(consequent),]),
        t.blockStatement([t.expressionStatement(alternate),])
    ));
}

function ConditionVarToIf(path) {
    // var m ? a = 11 : a = 22;
    //  |
    //  |
    //  |
    //  v
    // if (m) {
    //   var a = 11;
    // } else {
    //   var a = 22;
    // }
    let {id, init} = path.node;
    if (!t.isConditionalExpression(init)) return;
    const ParentPath = path.parentPath;
    const ParentNode = path.parent;
    if (!t.isVariableDeclaration(ParentNode)) return;
    if (t.isForStatement(ParentPath.parentPath)) return;
    let kind = ParentNode.kind;
    let {test, consequent, alternate} = init;
    ParentPath.replaceWith(t.ifStatement(
        test,
        t.blockStatement([t.variableDeclaration(kind, [t.variableDeclarator(id, consequent)]),]),
        t.blockStatement([t.variableDeclaration(kind, [t.variableDeclarator(id, alternate)]),])
    ));
}

function RemoveComma(path) {
    // a = 1, b = ddd(), c = null;
    //  |
    //  |
    //  |
    //  v
    // a = 1;
    // b = ddd();
    // c = null;
    let {expression} = path.node
    if (!t.isSequenceExpression(expression))
        return;
    let body = []
    expression.expressions.forEach(
        express => {
            body.push(t.expressionStatement(express))
        }
    )
    path.replaceInline(body)
}

function RemoveVarComma(path) {
    // var a = 1, b = ddd(), c = null;
    //   |
    //   |
    //   |
    //   v
    // var a = 1;
    // var b = ddd();
    // var c = null;
    let {kind, declarations} = path.node;
    if (declarations.length < 2) return;
    if (t.isForStatement(path.parentPath)) return;
    temp = [];
    declarations.forEach(
        VariableDeclarator => {
            temp.push(t.variableDeclaration(kind, [VariableDeclarator]))
        }
    )
    path.replaceInline(temp);
}

function MergeObj(path) {
    // var _0xb28de8 = {};
    // _0xb28de8["abcd"] = function(_0x22293f, _0x5a165e) {
    //     return _0x22293f == _0x5a165e;
    // };
    // _0xb28de8.dbca = function(_0xfbac1e, _0x23462f, _0x556555) {
    //     return _0xfbac1e(_0x23462f, _0x556555);
    // };
    // _0xb28de8.aaa = function(_0x57e640) {
    //     return _0x57e640();
    // };
    // _0xb28de8["bbb"] = "eee";
    // var _0x15e145 = _0xb28de8;
    //  |
    //  |
    //  |
    //  v
    // var _0xb28de8 = {
    //   "abcd": function (_0x22293f, _0x5a165e) {
    //     return _0x22293f == _0x5a165e;
    //   },
    //   "dbca": function (_0xfbac1e, _0x23462f, _0x556555) {
    //     return _0xfbac1e(_0x23462f, _0x556555);
    //   },
    //   "aaa": function (_0x57e640) {
    //     return _0x57e640();
    //   },
    //   "bbb": "eee"
    // };
    const {id, init} = path.node;
    if (!t.isObjectExpression(init)) // 判断是否是定义对象
        return;
    let name = id.name;
    let properties = init.properties;
    let scope = path.scope;
    let binding = scope.getBinding(name);
    if (!binding || binding.constantViolations.length > 0) { // 确认该对象没有被多次定义
        return;
    }
    let paths = binding.referencePaths;
    scope.traverse(scope.block, {
        AssignmentExpression: function(_path) {
            const left = _path.get("left");
            const right = _path.get("right");
            if (!left.isMemberExpression())
                return;
            const object = left.get("object");
            const property = left.get("property");
            if (object.isIdentifier({name: name}) && property.isStringLiteral() && _path.scope == scope) {
                properties.push(t.ObjectProperty(t.valueToNode(property.node.value), right.node));
                _path.remove();
            }
            if (object.isIdentifier({name: name}) && property.isIdentifier() && _path.scope == scope) {
                properties.push(t.ObjectProperty(t.valueToNode(property.node.name), right.node));
                _path.remove();
            }
        }
    })
    paths.map(function(refer_path) {
        let bindpath = refer_path.parentPath; 
        if (!t.isVariableDeclarator(bindpath.node)) return;
        let bindname = bindpath.node.id.name;
        bindpath.scope.rename(bindname, name, bindpath.scope.block);
        bindpath.remove();
    });
}

function CallToStr(path) {
    // var _0xb28de8 = {
    //     "abcd": function(_0x22293f, _0x5a165e) {
    //         return _0x22293f == _0x5a165e;
    //     },
    //     "dbca": function(_0xfbac1e, _0x23462f, _0x556555) {
    //         return _0xfbac1e(_0x23462f, _0x556555);
    //     },
    //     "aaa": function(_0x57e640) {
    //         return _0x57e640();
    //     },
    //     "bbb": "eee"
    // };
    // var aa = _0xb28de8["abcd"](123, 456);
    // var bb = _0xb28de8["dbca"](bcd, 11, 22);
    // var cc = _0xb28de8["aaa"](dcb);
    // var dd = _0xb28de8["bbb"];
    //   |
    //   |
    //   |
    //   v
    // var aa = 123 == 456;
    // var bb = bcd(11, 22);
    // var cc = dcb();
    // var dd = "eee";
    var node = path.node;
    if (!t.isObjectExpression(node.init)) // 判断是否使用对象
        return;
    var objPropertiesList = node.init.properties;
    if (objPropertiesList.length == 0)
        return;
    var objName = node.id.name;
    // 是否可删除该对象：发生替换时可删除，否则不删除
    var del_flag = false
    objPropertiesList.forEach(prop => {
        var key = prop.key.value;
        if(t.isFunctionExpression(prop.value)) {
            var retStmt = prop.value.body.body[0];
            var fnPath = path.getFunctionParent() || path.scope.path;
            fnPath.traverse({
                CallExpression: function (_path) {
                    var _node = _path.node.callee;
                    if (!t.isMemberExpression(_path.node.callee))
                        return;
                    if (!t.isIdentifier(_node.object) || _node.object.name !== objName)
                        return;
                    if (!(t.isStringLiteral(_node.property) || t.isIdentifier(_node.property)))
                        return;
                    if (!(_node.property.value == key || _node.property.name == key))
                        return;
                    var args = _path.node.arguments;
                    // 二元运算, 逻辑运算, 函数调用
                    if (t.isBinaryExpression(retStmt.argument) && args.length===2) {
                        _path.replaceWith(t.binaryExpression(retStmt.argument.operator, args[0], args[1]));
                    }
                    else if(t.isLogicalExpression(retStmt.argument) && args.length==2) {
                        _path.replaceWith(t.logicalExpression(retStmt.argument.operator, args[0], args[1]));
                    }
                    else if(t.isCallExpression(retStmt.argument) && t.isIdentifier(retStmt.argument.callee)) {
                        _path.replaceWith(t.callExpression(args[0], args.slice(1)))
                    }
                    del_flag = true;
                }
            })
        }
        else if (t.isStringLiteral(prop.value)){
            var retStmt = prop.value.value;
            var fnPath = path.getFunctionParent() || path.scope.path;
            fnPath.traverse({
                MemberExpression:function (_path) {
                    var _node = _path.node;
                    if (!t.isIdentifier(_node.object) || _node.object.name !== objName)
                        return;
                    if (!(t.isStringLiteral(_node.property) || t.isIdentifier(_node.property)))
                        return;
                    if (!(_node.property.value == key || _node.property.name == key))
                        return;
                    _path.replaceWith(t.stringLiteral(retStmt))
                    del_flag = true;
                }
            })
        }
    });
    if (del_flag) {
        // 如果发生替换，则删除该对象, 该处可能出问题，因为字典的内容未必会饱和使用
        path.remove();
    } 
}

function delExtra(path) {
    // ['\x49\x63\x4b\x72\x77\x70\x2f\x44\x6c\x67\x3d\x3d',0x123];
    //   |
    //   |
    //   |
    //   v
    // ["IcKrwp/Dlg==", 291];
    delete path.node.extra; 
}













function get_ob_enc(ast) {
    var first_idx = 0
    for (var i = 0; i < ast.program.body.length; i++) {
        if (ast.program.body[i].type != 'EmptyStatement'){
            first_idx = i;
            break
        }
    }
    var decrypt_code = ast.program.body.slice(first_idx, first_idx+3)
    var rest_code = ast.program.body.slice(first_idx+3)
    ast.program.body = decrypt_code
    var {code} = generator(ast, {
        compact: true
    })
    global_code = code
    decryptStr = decrypt_code[2].declarations[0].id.name
    var flag = true
    const visitor = {
        "ExpressionStatement"(path) {
            path.traverse({
                "StringLiteral"(_path) {
                    delete _path.node.extra
                },
                MemberExpression: FormatMember
            })
            var code = path.toString()
            if (flag && code.indexOf("atob") != -1) {
                atob_node = path.node
                flag = false
            }
        }
    }
    traverse(ast, visitor)
    ast.program.body = [atob_node]
    var {code} = generator(ast, {
        jsescOption: {
            minimal: true,
        }
    })
    const comment = "// atob函数，后面可能会判断其是否存在，勿删！"
    atob_code = comment + "\n!" + code + "\n"
    ast.program.body = rest_code
    return ast
}

function pas_ob_enc(ast) {
    eval(global_code)
    traverse(ast, {
        CallExpression: funToStr,
        StringLiteral: delExtra,
        NumericLiteral: delExtra,
    })
    return ast;
    function funToStr(path) {
        var node = path.node;
        if (!t.isIdentifier(node.callee, {name: decryptStr})) 
            return;
        let value = eval(path.toString())
        // console.log("还原前：" + path.toString(), "还原后：" + value);
        path.replaceWith(t.valueToNode(value));
    }
    function delExtra(path) {
        delete path.node.extra; 
    }
}

function ReplaceWhile(path) {
    var node = path.node;
    if (!(t.isBooleanLiteral(node.test) || t.isUnaryExpression(node.test)))
        return;
    if (!(node.test.prefix || node.test.value))
        return;
    if (!t.isBlockStatement(node.body))
        return;
    var body = node.body.body;
    if (!t.isSwitchStatement(body[0]) || !t.isMemberExpression(body[0].discriminant) || !t.isBreakStatement(body[1]))
        return;
    var swithStm = body[0];
    var arrName = swithStm.discriminant.object.name;
    var argName = swithStm.discriminant.property.argument.name
    let arr = [];
    let all_presibling = path.getAllPrevSiblings();
    all_presibling.forEach(pre_path => {
        const {declarations} = pre_path.node;
        let {id, init} = declarations[0]
        if (arrName == id.name) {
            arr = init.callee.object.value.split('|');
            pre_path.remove()
        }
        if (argName == id.name) {
            pre_path.remove()
        }
    })
    var caseList = swithStm.cases;
    var resultBody = [];
    arr.map(targetIdx => {
        var targetBody = caseList[targetIdx].consequent;
        if (t.isContinueStatement(targetBody[targetBody.length - 1]))
            targetBody.pop();
        resultBody = resultBody.concat(targetBody)
    });
    path.replaceInline(resultBody);
}






















function muti_process_defusion(jscode){
    var ast = parser.parse(jscode);

    // ob 解混淆处理部分
    // ast = get_ob_enc(ast)
    // ast = pas_ob_enc(ast)
    // traverse(ast, {VariableDeclarator: {exit: MergeObj},});     // 可能出问题（不可通用）
    // traverse(ast, {VariableDeclarator: {exit: CallToStr},});    // 可能出问题（不可通用）
    // traverse(ast, {WhileStatement: {exit: [ReplaceWhile]},});   // 反控制流平坦化

    // 通用解混淆部分
    traverse(ast, {StringLiteral: delExtra,})                   // 清理二进制显示内容
    traverse(ast, {NumericLiteral: delExtra,})                  // 清理二进制显示内容
    traverse(ast, {ConditionalExpression: TransCondition,});    // 三元表达式
    traverse(ast, {ExpressionStatement: ConditionToIf,});       // 三元表达式转换成if
    traverse(ast, {VariableDeclarator: ConditionVarToIf,});     // 赋值语句的 三元表达式转换成if
    traverse(ast, {ExpressionStatement: RemoveComma,});         // 逗号表达式转换
    traverse(ast, {VariableDeclaration: RemoveVarComma,});      // 赋值语句的 逗号表达式转换
    traverse(ast, {MemberExpression: FormatMember,});           // obj['func1']['func2']() --> obj.func1.func2()
    var { code } = generator(ast, { jsescOption: { minimal: true, } });
    return code;
}
// const fs = require('fs');
// var jscode = fs.readFileSync("./source.js", {
//     encoding: "utf-8"
// });
// code = muti_process_defusion(jscode);
// console.log(code);
// fs.writeFileSync('./code.js', code, {
//     encoding: "utf-8"
// })
"use strict";

CodeMirror.defineMode("text/conjure", function (config) {

    var isOperatorChar = /[+\-*=<>%^\/]/;

    var keywords = {
        "forall": true,
        "allDifferent": true,
        "allDiff": true,
        "alldifferent_except": true,
        "dim": true,
        "toSet": true,
        "toMSet": true,
        "toRelation": true,
        "maximising": true,
        "minimising": true,
        "forAll": true,
        "exists": true,
        "toInt": true,
        "sum": true,
        "be": true,
        "bijective": true,
        "bool": true,
        "by": true,
        "complete": true,
        "defined": true,
        "domain": true,
        "in": true,
        "or": true,
        "and": true,
        "false": true,
        "find": true,
        "from": true,
        "function": true,
        "given": true,
        "image": true,
        "indexed": true,
        "injective": true,
        "int": true,
        "intersect": true,
        "freq": true,
        "lambda": true,
        "language": true,
        "letting": true,
        "matrix": true,
        "maxNumParts": true,
        "maxOccur": true,
        "maxPartSize": true,
        "maxSize": true,
        "minNumParts": true,
        "minOccur": true,
        "minPartSize": true,
        "minSize": true,
        "mset": true,
        "numParts": true,
        "of": true,
        "partial": true,
        "partition": true,
        "partSize": true,
        "preImage": true,
        "quantifier": true,
        "range": true,
        "regular": true,
        "relation": true,
        "representation": true,
        "set": true,
        "size": true,
        "subset": true,
        "subsetEq": true,
        "such": true,
        "supset": true,
        "supsetEq": true,
        "surjective": true,
        "that": true,
        "together": true,
        "enum": true,
        "total": true,
        "true": true,
        "new": true,
        "type": true,
        "tuple": true,
        "union": true,
        "where": true,
        "branching": true,
        "on": true
    };  
    var punc = ":;,.(){}[]";

    function tokenBase(stream, state) {
        var ch = stream.next();
        if (ch == '"') {
            state.tokenize.push(tokenString);
            return tokenString(stream, state);
        }
        if (/[\d\.]/.test(ch)) {
            if (ch == ".") {
                stream.match(/^[0-9]+([eE][\-+]?[0-9]+)?/);
            } else if (ch == "0") {
                stream.match(/^[xX][0-9a-fA-F]+/) || stream.match(/^0[0-7]+/);
            } else {
                stream.match(/^[0-9]*\.?[0-9]*([eE][\-+]?[0-9]+)?/);
            }
            return "number";
        }
        if (ch == "/") {
            if (stream.eat("*")) {
                state.tokenize.push(tokenComment);
                return tokenComment(stream, state);
            }
        }
        if (ch == "$") {
            stream.skipToEnd();
            return "comment";
        }
        if (isOperatorChar.test(ch)) {
            stream.eatWhile(isOperatorChar);
            return "operator";
        }
        if (punc.indexOf(ch) > -1) {
            return "punctuation";
        }
        stream.eatWhile(/[\w\$_\xa1-\uffff]/);
        var cur = stream.current();
        
        if (keywords.propertyIsEnumerable(cur)) {
            return "keyword";
        }
        return "variable";
    }

    function tokenComment(stream, state) {
        var maybeEnd = false, ch;
        while (ch = stream.next()) {
            if (ch == "/" && maybeEnd) {
                state.tokenize.pop();
                break;
            }
            maybeEnd = (ch == "*");
        }
        return "comment";
    }

    function tokenUntilClosingParen() {
        var depth = 0;
        return function (stream, state, prev) {
            var inner = tokenBase(stream, state, prev);
            console.log("untilClosing", inner, stream.current());
            if (inner == "punctuation") {
                if (stream.current() == "(") {
                    ++depth;
                } else if (stream.current() == ")") {
                    if (depth == 0) {
                        stream.backUp(1)
                        state.tokenize.pop()
                        return state.tokenize[state.tokenize.length - 1](stream, state)
                    } else {
                        --depth;
                    }
                }
            }
            return inner;
        }
    }

    function tokenString(stream, state) {
        var escaped = false, next, end = false;
        while ((next = stream.next()) != null) {
            if (next == '(' && escaped) {
                state.tokenize.push(tokenUntilClosingParen());
                return "string";
            }
            if (next == '"' && !escaped) { end = true; break; }
            escaped = !escaped && next == "\\";
        }
        if (end || !escaped)
            state.tokenize.pop();
        return "string";
    }

    return {
        startState: function (basecolumn) {
            return {
                tokenize: []
            };
        },

        token: function (stream, state) {
            if (stream.eatSpace()) return null;
            var style = (state.tokenize[state.tokenize.length - 1] || tokenBase)(stream, state);
            console.log("token", style);
            return style;
        },

        blockCommentStart: "/*",
        blockCommentEnd: "*/",
        lineComment: "$"
    };
});


CodeMirror.defineMIME("text/conjure", "text/conjure");

// Jupyter.CodeCell.options_default.highlight_modes['magic_text/conjure'] = { 'reg': [/^%%conjure/] };

// Jupyter.notebook.get_cells().map(function (cell) {
//     if (cell.cell_type == 'code') { cell.auto_highlight(); }
// });



// // Register a new language
// monaco.languages.register({ id: 'mySpecialLanguage', mimetypes: ['text/conjure'] });

// // Register a tokens provider for the language
// monaco.languages.setMonarchTokensProvider('mySpecialLanguage', {
// 	tokenizer: {
// 		root: [
// 			[/\[error.*/, 'custom-error'],
// 			[/\[notice.*/, 'custom-notice'],
// 			[/\[info.*/, 'custom-info'],
// 			[/\[[a-zA-Z 0-9:]+\]/, 'custom-date']
// 		]
// 	}
// });

// // Define a new theme that contains only rules that match this language
// monaco.editor.defineTheme('myCoolTheme', {
// 	base: 'vs',
// 	inherit: false,
// 	rules: [
// 		{ token: 'custom-info', foreground: '808080' },
// 		{ token: 'custom-error', foreground: 'ff0000', fontStyle: 'bold' },
// 		{ token: 'custom-notice', foreground: 'FFA500' },
// 		{ token: 'custom-date', foreground: '008800' }
// 	],
// 	colors: {
// 		'editor.foreground': '#000000'
// 	}
// });

// // Register a completion item provider for the new language
// monaco.languages.registerCompletionItemProvider('mySpecialLanguage', {
// 	provideCompletionItems: () => {
// 		var suggestions = [
// 			{
// 				label: 'simpleText',
// 				kind: monaco.languages.CompletionItemKind.Text,
// 				insertText: 'simpleText'
// 			},
// 			{
// 				label: 'testing',
// 				kind: monaco.languages.CompletionItemKind.Keyword,
// 				insertText: 'testing(${1:condition})',
// 				insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet
// 			},
// 			{
// 				label: 'ifelse',
// 				kind: monaco.languages.CompletionItemKind.Snippet,
// 				insertText: ['if (${1:condition}) {', '\t$0', '} else {', '\t', '}'].join('\n'),
// 				insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
// 				documentation: 'If-Else Statement'
// 			}
// 		];
// 		return { suggestions: suggestions };
// 	}
// });

// monaco.editor.create(document.getElementsByClassName('monaco-editor'), {
// 	theme: 'myCoolTheme',
// 	language: 'mySpecialLanguage'
// });


require(['notebook/js/codecell'], function (codecell) {
    codecell.CodeCell.options_default.highlight_modes['magic_text/conjure'] = { 'reg': [/%?%conjure/] };
    Jupyter.notebook.events.one('kernel_ready.Kernel', function () {
        Jupyter.notebook.get_cells().map(function (cell) {
            if (cell.cell_type == 'code') { cell.auto_highlight(); }
        });
    });
});


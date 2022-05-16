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

require(['notebook/js/codecell'], function (codecell) {
    codecell.CodeCell.options_default.highlight_modes['magic_text/conjure'] = { 'reg': [/%?%conjure/] };
    Jupyter.notebook.events.one('kernel_ready.Kernel', function () {
        Jupyter.notebook.get_cells().map(function (cell) {
            if (cell.cell_type == 'code') { cell.auto_highlight(); }
        });
    });
});



// Register a new language
monaco.languages.register({ id: 'mySpecialLanguage' });

// Register a tokens provider for the language
monaco.languages.setMonarchTokensProvider('mySpecialLanguage', {
	tokenizer: {
		root: [
			[/\[error.*/, 'custom-error'],
			[/\[notice.*/, 'custom-notice'],
			[/\[info.*/, 'custom-info'],
			[/\[[a-zA-Z 0-9:]+\]/, 'custom-date']
		]
	}
});

// Define a new theme that contains only rules that match this language
monaco.editor.defineTheme('myCoolTheme', {
	base: 'vs',
	inherit: false,
	rules: [
		{ token: 'custom-info', foreground: '808080' },
		{ token: 'custom-error', foreground: 'ff0000', fontStyle: 'bold' },
		{ token: 'custom-notice', foreground: 'FFA500' },
		{ token: 'custom-date', foreground: '008800' }
	],
	colors: {
		'editor.foreground': '#000000'
	}
});

// Register a completion item provider for the new language
monaco.languages.registerCompletionItemProvider('mySpecialLanguage', {
	provideCompletionItems: () => {
		var suggestions = [
			{
				label: 'simpleText',
				kind: monaco.languages.CompletionItemKind.Text,
				insertText: 'simpleText'
			},
			{
				label: 'testing',
				kind: monaco.languages.CompletionItemKind.Keyword,
				insertText: 'testing(${1:condition})',
				insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet
			},
			{
				label: 'ifelse',
				kind: monaco.languages.CompletionItemKind.Snippet,
				insertText: ['if (${1:condition}) {', '\t$0', '} else {', '\t', '}'].join('\n'),
				insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
				documentation: 'If-Else Statement'
			}
		];
		return { suggestions: suggestions };
	}
});

monaco.editor.create(document.getElementsByClassName('code'), {
	theme: 'myCoolTheme',
	value: getCode(),
	language: 'mySpecialLanguage'
});

function getCode() {
	return [
		'[Sun Mar 7 16:02:00 2004] [notice] Apache/1.3.29 (Unix) configured -- resuming normal operations',
		'[Sun Mar 7 16:02:00 2004] [info] Server built: Feb 27 2004 13:56:37',
		'[Sun Mar 7 16:02:00 2004] [notice] Accept mutex: sysvsem (Default: sysvsem)',
		'[Sun Mar 7 16:05:49 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 16:45:56 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 17:13:50 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 17:21:44 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 17:23:53 2004] statistics: Use of uninitialized value in concatenation (.) or string at /home/httpd/twiki/lib/TWiki.pm line 528.',
		"[Sun Mar 7 17:23:53 2004] statistics: Can't create file /home/httpd/twiki/data/Main/WebStatistics.txt - Permission denied",
		'[Sun Mar 7 17:27:37 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 17:31:39 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 17:58:00 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 18:00:09 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 18:10:09 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 18:19:01 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 18:42:29 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 18:52:30 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 18:58:52 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 19:03:58 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 19:08:55 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 20:04:35 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 20:11:33 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 20:12:55 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 20:25:31 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 20:44:48 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 20:58:27 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 21:16:17 2004] [error] [client xx.xx.xx.xx] File does not exist: /home/httpd/twiki/view/Main/WebHome',
		'[Sun Mar 7 21:20:14 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 21:31:12 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 21:39:55 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Sun Mar 7 21:44:10 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 01:35:13 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 01:47:06 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 01:59:13 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 02:12:24 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 02:54:54 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 03:46:27 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 03:48:18 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 03:52:17 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 03:55:09 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 04:22:55 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 04:24:47 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 04:40:32 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 04:55:40 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 04:59:13 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 05:22:57 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 05:24:29 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'[Mon Mar 8 05:31:47 2004] [info] [client xx.xx.xx.xx] (104)Connection reset by peer: client stopped connection before send body completed',
		'<11>httpd[31628]: [error] [client xx.xx.xx.xx] File does not exist: /usr/local/installed/apache/htdocs/squirrelmail/_vti_inf.html in 29-Mar 15:18:20.50 from xx.xx.xx.xx',
		'<11>httpd[25859]: [error] [client xx.xx.xx.xx] File does not exist: /usr/local/installed/apache/htdocs/squirrelmail/_vti_bin/shtml.exe/_vti_rpc in 29-Mar 15:18:20.54 from xx.xx.xx.xx'
	].join('\n');
}

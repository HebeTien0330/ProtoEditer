'''
:@Author: tangchengqin
:@Date: 2025/1/13 15:25:12
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/13 15:25:12
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from pygments.lexer import RegexLexer, bygroups
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation

# protobuf 词法分析器
class ProtoLexer(RegexLexer):
    name = 'Protocol Buffers'
    aliases = ['proto']
    filenames = ['*.proto']

    tokens = {
        'root': [
            (r'\s+', Text),
            (r'//.*?$', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            (r'syntax\s*=\s*"proto[23]";', Keyword.Reserved),
            (r'package\s+(\w+(\.\w+)*)\s*;', bygroups(Keyword.Reserved, Name.Namespace)),
            (r'import\s+"([^"]+)"\s*;', bygroups(Keyword.Reserved, String)),
            (r'(message|enum|service|rpc|returns|option|repeated|required|optional)\b', Keyword.Reserved),
            (r'(double|float|int32|int64|uint32|uint64|sint32|sint64|fixed32|fixed64|sfixed32|sfixed64|bool|string|bytes)\b', Keyword.Type),
            (r'\b(true|false)\b', Keyword.Constant),
            (r'([a-zA-Z_]\w*)\s*=', bygroups(Name.Variable, Operator)),
            (r'([a-zA-Z_]\w*)\s*{', bygroups(Name.Class, Punctuation)),
            (r'}', Punctuation),
            (r'\b[0-9]+\b', Number.Integer),
            (r'"(\\\\|\\"|[^"])*"', String),
            (r"'(\\\\|\\'|[^'])*'", String),
            (r'[;,.]', Punctuation),
        ],
    }

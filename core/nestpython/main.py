def ncompile(code:str, *, indent_amount:int=1, cythonic:bool=False):

  import contextlib
  import re
  from collections.abc import Iterable
  from enum import Enum

  # ----------------- #
  #      TOKENS       #
  # ----------------- #

  def unpack(list):
    out = []
    for arg in list:
      match arg:
        case Iterable():
          out += unpack(arg)
        case _:
          out.append(arg)
    return out

  TokenTypes = Enum('TokenTypes', [
    'SYNTACTICAL', 'MULTILINE',
    'INDENTED', 'MAP', 'CYTHON',
    'STRING', 'APPENDSUB', 'SHORTHAND',
    'MACROS', 'ESCAPEMENT'
  ])

  id = 0

  class Token:

    def __init__(self, symb='', *types, setID=None):
      self.symb = symb
      self.types = unpack(types)
      if TokenTypes.SHORTHAND in self.types and TokenTypes.MAP not in self.types:
        self.types.append(TokenTypes.MAP)
      if setID is None:
        nonlocal id
        id += 1
      else:
        id = setID
      self.id = id

    # TOKENIZATION ALGORITHM

  def anonToken(symb, *types):
    return Token(symb, *types, setID=-1)

  def tokenize(string, tokens: list[Token], buffer):
    tokenized = []
    i = 0
    j = 0
    while i + j < len(string):
      for token in tokens:
        F = (i + j - buffer >= 0)
        if match := re.match(
            fr'[\s\S]{{{buffer}}}{token.symb}' if F else token.symb,
            string[i + j - buffer:] if F else string, re.M):
          match_string = match.group()[buffer:] if F else match.group()
          if string[i:i + j] != '':
            tokenized.append(anonToken(string[i:i + j]))
          tokenized.append(Token(match_string, token.types, setID=token.id))
          i += j + len(match_string)
          j = -1
          break
      j += 1
    if i < len(string):
      tokenized.append(anonToken(string[i:]))
    return tokenized

  # TOKEN DECLARATIONS

  def sclund(regex):
    return r'(?<![\w0-9])' + regex + r'_*(?![\w0-9])'

  macros = {}

  class Tokens(Enum):
    escape = Token(r'\\', TokenTypes.ESCAPEMENT)
    escapeEscaped = Token(r'\\\\', TokenTypes.ESCAPEMENT)
    multilineStringDouble = Token(r'(?<!\\)"""', TokenTypes.STRING)
    multilineStringSingle = Token(r"(?<!\\)'''", TokenTypes.STRING)
    stringDouble = Token(r'"', TokenTypes.STRING)
    stringSingle = Token(r"'", TokenTypes.STRING)
    dictIndentLeft = Token(r'-{', TokenTypes.MAP)
    dictIndentRight = Token(r'}-', TokenTypes.MAP)
    indentLeftNoColon = Token(r'~{', TokenTypes.INDENTED,
      TokenTypes.SYNTACTICAL)
    indentLeftDouble = Token(r'{{')
    indentSelfClose = Token(r'{\s*}', TokenTypes.INDENTED, TokenTypes.SYNTACTICAL)
    indentLeft = Token(r'{', TokenTypes.INDENTED, TokenTypes.SYNTACTICAL)
    indentRight = Token(r'}', TokenTypes.INDENTED, TokenTypes.SYNTACTICAL)
    newline = Token(r'\n', TokenTypes.INDENTED, TokenTypes.MULTILINE)
    returnShorthand = Token(r'=>', TokenTypes.SHORTHAND)
    nativeSemicolon = Token(r',,', TokenTypes.MAP)
    nativeAssignment = Token(r'<-', TokenTypes.MAP)
    incrementOperator = Token(r'\+\+', TokenTypes.MAP)
    decrementOperator = Token(r'--', TokenTypes.MAP)
    andShorthand = Token(r'&&', TokenTypes.SHORTHAND)
    orShorthand = Token(r'\|\|', TokenTypes.SHORTHAND)
    isShorthand = Token(r'=&', TokenTypes.SHORTHAND)
    isNotShorthand = Token(r'!=&', TokenTypes.SHORTHAND)
    cpdefShorthand = Token(r'~\$=', TokenTypes.SHORTHAND, TokenTypes.CYTHON)
    cdefShorthand = Token(r'\$=', TokenTypes.SHORTHAND, TokenTypes.CYTHON)
    assertShorthand = Token(r'\?!', TokenTypes.SHORTHAND)
    defShorthand = Token(r':=', TokenTypes.SHORTHAND)
    returntypeShorthand = Token(r'>:', TokenTypes.SHORTHAND)
    inShorthand = Token(r'->', TokenTypes.SHORTHAND)
    notInShorthand = Token(r'!>', TokenTypes.SHORTHAND)
    delShorthand = Token(r'~>', TokenTypes.SHORTHAND)
    lambdaShorthand = Token(r';=', TokenTypes.SHORTHAND)
    indentNewline = Token(r';', TokenTypes.INDENTED, TokenTypes.SYNTACTICAL)
    notShorthand = Token(r'!(?!=)', TokenTypes.SHORTHAND)
    andDeconflict = Token(sclund('and'), TokenTypes.APPENDSUB)
    orDeconflict = Token(sclund('or'), TokenTypes.APPENDSUB)
    assertDeconflict = Token(sclund('assert'), TokenTypes.APPENDSUB)
    cpdefDeconflict = Token(sclund('cpdef'), TokenTypes.APPENDSUB, TokenTypes.CYTHON)
    cdefDeconflict = Token(sclund('cdef'), TokenTypes.APPENDSUB, TokenTypes.CYTHON)
    notDeconflict = Token(sclund('not'), TokenTypes.APPENDSUB)
    isDeconflict = Token(sclund('is'), TokenTypes.APPENDSUB)
    defDeconflict = Token(sclund('def'), TokenTypes.APPENDSUB)
    lambdaDeconflict = Token(sclund('lambda'), TokenTypes.APPENDSUB)
    inDeconflict = Token(sclund('in'), TokenTypes.APPENDSUB)
    returnDeconflict = Token(sclund('return'), TokenTypes.APPENDSUB)
    caseDeconflict = Token(sclund('case'), TokenTypes.APPENDSUB)
    delDeconflict = Token(sclund('del'), TokenTypes.APPENDSUB)
    passDeconflict = Token(sclund('pass'), TokenTypes.APPENDSUB)
    comment = Token(r'\/\*[\s\S]*?\*\/', TokenTypes.INDENTED)
    lineComment = Token(r'\/\/.*', TokenTypes.INDENTED)
    lineStatement = Token(r'/\|.*?\|\\', TokenTypes.INDENTED)
    intDiv = Token(r'~/', TokenTypes.MAP)
    caseShorthand = Token(r'\?', TokenTypes.SHORTHAND)
    macroDefine = Token(r'#\s*[\w\n]+\s*#\s*<[\s\S]*>\s*#', TokenTypes.MACROS)
    macroUndefine = Token(r'#~\s*[\w\n]+\s*~#', TokenTypes.MACROS)
    macroIfdef = Token(r'#\?\s*[\w\n]*\s*\?#', TokenTypes.MACROS)
    macroAccess = Token(r'\$[\w\n]*', TokenTypes.MACROS)
    macro = Token('#', TokenTypes.SYNTACTICAL)

    # CONVERSION TOKEN MAPPING

  tokenMap = {
      Tokens.dictIndentLeft.value.id: '{',
      Tokens.dictIndentRight.value.id: '}',
      Tokens.nativeSemicolon.value.id: ';',
      Tokens.nativeAssignment.value.id: ':=',
      Tokens.andShorthand.value.id: 'and',
      Tokens.orShorthand.value.id: 'or',
      Tokens.notShorthand.value.id: 'not',
      Tokens.isShorthand.value.id: 'is',
      Tokens.isNotShorthand.value.id: 'is not',
      Tokens.defShorthand.value.id: 'def',
      Tokens.inShorthand.value.id: 'in',
      Tokens.caseShorthand.value.id: 'case',
      Tokens.notInShorthand.value.id: 'not in',
      Tokens.returnShorthand.value.id: 'return',
      Tokens.lambdaShorthand.value.id: 'lambda',
      Tokens.delShorthand.value.id: 'del',
      Tokens.incrementOperator.value.id: '+=1',
      Tokens.decrementOperator.value.id: '-=1',
      Tokens.cpdefShorthand.value.id: 'cpdef',
      Tokens.cdefShorthand.value.id: 'cdef',
      Tokens.assertShorthand.value.id: 'assert',
      Tokens.intDiv.value.id: '//',
      Tokens.returntypeShorthand.value.id: '->'
  }

  def isF(token, ptoken):
    with contextlib.suppress(TypeError):
      return (TokenTypes.STRING in token.types) and (ptoken.symb[~0].lower() == 'f' or
                                                     ptoken.symb[~1:].lower() == 'fr')

  def isR(token, ptoken):
    with contextlib.suppress(TypeError):
      return (TokenTypes.STRING in token.types) and (ptoken.symb[~0].lower() == 'r' or
                                                     ptoken.symb[~1:].lower() == 'rf')

  def isEscape(token):
    with contextlib.suppress(TypeError):
      return (token.id == Tokens.escape.value.id and not compilable())

  def isEscapedEscape(token):
    with contextlib.suppress(TypeError):
      return (token.id == Tokens.escapeEscaped.value.id and not compilable())

  def isNRawEscape(token):
    return isEscape(token) and not in_rstring

  def isNRawEscapedEscape(token):
    return isEscapedEscape(token) and not in_rstring

  compiled_code = ''
  indent_level = 0
  string_nesting = []
  def getStringType():
    return anonToken('') if len(string_nesting) == 0 else string_nesting[~0]
  fstring_nesting = 0
  in_multilineStringSingle = lambda: getStringType().id == Tokens.multilineStringSingle.value.id and in_string
  in_multilineStringDouble = lambda: getStringType().id == Tokens.multilineStringDouble.value.id and in_string
  in_stringSingle = lambda: getStringType().id == Tokens.stringSingle.value.id and in_string
  in_stringDouble = lambda: getStringType().id == Tokens.stringDouble.value.id and in_string
  in_fstring = False
  in_rstring = False
  in_multilineString = lambda: (in_multilineStringSingle() or
                                in_multilineStringDouble())
  in_string = False
  compilable = lambda: not in_string

  def string_compilable(token):
    match token.id:
      case Tokens.multilineStringSingle.value.id:
        return not in_multilineStringDouble()
      case Tokens.multilineStringDouble.value.id:
        return not in_multilineStringSingle()
      case Tokens.stringSingle.value.id:
        return not (in_multilineString() or in_stringDouble())
      case Tokens.stringDouble.value.id:
        return not (in_multilineString() or in_stringSingle())

  indent = ' ' * indent_amount
  buffer = 1
  tokens = tokenize(code, [t.value for t in Tokens if TokenTypes.CYTHON not in t.value.types or cythonic], buffer)
  compiling = True
  ptoken = Token()
  class breakout(Exception):
    pass

  def string_compile(token):
    nonlocal in_string
    if getStringType().id == token.id:
      string_nesting.pop()
    else:
      string_nesting.append(token)
    in_string = not in_string

  def compile(bufferToken):
    nonlocal compiled_code
    nonlocal indent_level 
    nonlocal in_multilineStringSingle
    nonlocal in_multilineStringDouble
    nonlocal in_stringSingle
    nonlocal in_stringDouble
    nonlocal in_fstring
    nonlocal in_rstring
    nonlocal fstring_nesting
    nonlocal in_multilineString
    nonlocal in_string
    nonlocal compilable
    nonlocal indent
    nonlocal tokens
    nonlocal buffer
    nonlocal compiling
    nonlocal ptoken
    nonlocal cythonic
    try:
     for n, token in enumerate(tokens):
      ptoken = tokens[n - 1] if n > 0 else bufferToken
      if compilable():
        match token.id:
          case Tokens.comment.value.id | Tokens.lineComment.value.id:
            continue
          case Tokens.lineStatement.value.id:
            compiled_code += '#' + token.symb[2:-2].rstrip() + '\n' + indent * indent_level
            continue
      if isNRawEscapedEscape(token):
        compiled_code += '\\'
      if (token.id == Tokens.indentLeftDouble.value.id 
          and not in_fstring):
        tokens = [Tokens.indentLeft.value]*2 + tokens[n + 1:]
        raise breakout
      if token.id == Tokens.indentSelfClose.value.id:
        if compilable():
          compiled_code = (compiled_code.rstrip()
                           + f':\n{indent * (indent_level+1)}\
pass\n{indent * indent_level}')
          continue
        else:
          tokens = ([Tokens.indentLeft.value] 
          + tokenize(token.symb[1:-1], [t.value for t in Tokens], buffer) 
          + [Tokens.indentRight.value]
          + tokens[n + 1:])
          raise breakout
      if TokenTypes.MACROS in token.types and compilable():
       match token.id:
        case Tokens.macroDefine.value.id:
          macro = token.symb.split('#', 2)[1].strip().replace('\n', '')
          sub = token.symb.split('#', 2)[2][:~0].strip()[1:-1]
          
          macros.update({macro: (sub, indent_level)})
          continue
        case Tokens.macroUndefine.value.id:
          macro = token.symb.split('#')[1][1:-1].strip().replace('\n', '')
          if macros[macro][1] == indent_level:
            macros.pop(macro)
          else:
            raise SyntaxError(
              f'nesting level {indent_level} does not \
              match macro\'s {macros[macro][1]}'
            )
        case Tokens.macroIfdef.value.id:
          macro = token.symb.split('#')[1][1:-1].strip().replace('\n', '')
          truth = False
          if macro in macros:
            truth = macros[macro][1] >= indent_level
          if compiled_code[~0] != ' ' and compiled_code[~0] != '\n':
            compiled_code += ' '
          compiled_code += str(truth) + ' '
          continue
        case Tokens.macroAccess.value.id:
          if compilable():
            macro = macros[token.symb[1:].replace('\n', '')][0]
            tokens = tokenize(macro, [t.value for t in Tokens], buffer) + tokens[n + 1:]
            raise breakout
          else:
            compiled_code += (token.symb if in_multilineString() 
                              else token.symb.replace('\n', ''))
      if TokenTypes.STRING in token.types and string_compilable(token):
        if not isNRawEscape(ptoken):
          string_compile(token)
        in_fstring = in_string and isF(token, ptoken)
        in_rstring = in_string and isR(token, ptoken)
      if compilable():
       if fstring_nesting == 0:
        match token.id:
          case Tokens.indentLeft.value.id | Tokens.indentLeftNoColon.value.id:
            indent_level += 1
            compiled_code = compiled_code.rstrip()
            compiled_code += ((':' if token.id == Tokens.indentLeft.value.id 
                              else (
                                f'\n{indent * (indent_level-1)}if True:'
                              )) + '\n' + indent * indent_level
                             )
          case Tokens.indentRight.value.id:
            indent_level -= 1
            for macro in list(macros):
              if macros[macro][1] > indent_level:
                macros.pop(macro)
            compiled_code += '\n' + indent * indent_level
          case Tokens.indentNewline.value.id:
            compiled_code += '\n' + indent * indent_level
       elif token.id == Tokens.indentRight.value.id:
        fstring_nesting -= 1
        in_fstring = True
        in_string = True

      elif in_fstring:
        match token.id:
          case Tokens.indentLeft.value.id:
            in_fstring = False
            in_string = False
            fstring_nesting += 1
            compiled_code += token.symb
          case Tokens.indentRight.value.id:
            if tokens[n+1].id == token.id:
              compiled_code += token.symb * 2
              tokens = tokens[n+2:]
              raise breakout
      if (not (TokenTypes.SYNTACTICAL in token.types and compilable())
          and not (TokenTypes.MULTILINE in token.types and not in_multilineString())):
        
        mtoken = tokenMap[token.id] if (TokenTypes.MAP in token.types
                                        and compilable()) else token.symb
        if compilable():
          if TokenTypes.APPENDSUB in token.types:
            mtoken += '_'
          if TokenTypes.SHORTHAND in token.types:
            mtoken += ' '
            if compiled_code != '':
              if compiled_code[~0] != ' ' and compiled_code[~0] != '\n':
                compiled_code += ' '
        compiled_code += (mtoken.lstrip() if
                          ((TokenTypes.INDENTED
                          in ptoken.types) 
                          or (TokenTypes.SHORTHAND in ptoken.types) 
                          and compilable()) else mtoken)
     compiled_code += '\n'
     compiling = False
    except breakout:
      pass
  while compiling:
    compile(ptoken)
  return compiled_code


def nexec(code:str, indent_amount:int=1, *, cythonic:bool=False):
  exec(ncompile(code, indent_amount=indent_amount, cythonic=cythonic))
